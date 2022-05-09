from __future__ import annotations

from enum import Enum
from random import Random

from traveller import dice
from traveller.career import Career, CareerType, ReEnlistmentOutcome, careers, drifter
from traveller.characteristic import Characteristic
from traveller.world import World

from psycopg2.extensions import connection

from traveller.equipment import Equipment, Armor, Weapon, equipments

from typing import Dict, List, Optional, Union, cast, Tuple
from traveller.skill import Skill, skills


# This represents the Sex of a Character.
# It will be used to determine appropriate noble/work titles.
class Sex(Enum):
    M: str = 'M'
    F: str = 'F'


# This represents the current Stance of a Character,
# and will be mainly used during combat to determine damage or movement modifiers.
class Stance(Enum):
    Prone: int = 0
    Crouched: int = 1
    Standing: int = 2


class NobleTitle(Enum):
    Lord: Dict[Sex, int] = {}


class Character:
    # Information
    name: str
    age: int = 18
    sex: Sex

    # Statistics
    stats: Dict[Characteristic, int] = {}

    # Homeworld
    homeworld: World

    # Possessions
    credits: int = 0
    debt: int = 0
    injury_crisis_debt: int = 0
    ship_shares: int = 0

    equipped_armor: Armor = None
    equipped_reflec: Armor = None
    drawn_weapon: Weapon = None
    inventory: List[Tuple[Equipment, int]] = []

    # Statuses
    took_drugs: bool = False
    drugs_terms: int = 0

    stance: Stance = Stance.Standing
    rads: int = 0
    is_fatigued: bool = False
    stims_taken: int = 0

    # Careers
    society: bool = False
    retired: bool = False
    lose_benefits = False
    benefit_rolls: int
    cash_rolls: int
    available_careers: List[str] = list(careers.keys())
    careers: List[Career] = []

    # Skills
    skills: List[Skill] = []


    def equip_armor(self, armor_name: str):
        for item, qt in self.inventory:
            if item.name is armor_name and isinstance(item, Armor):
                self.equipped_armor = cast(Armor, item)

    def roll_stats(self):
        for c in Characteristic:
            v = dice.roll(2)
            self.stats[c] = v

    def modifier(self, c: Characteristic) -> int:
        return self.stats[c] // 3 - 1  # TODO -2??? Who knows...

    @property
    def skill_names(self):
        return [s.name for s in self.skills]

    @property
    def career(self) -> Career:
        return self.careers[-1]

    @property
    def terms(self) -> int:
        t: int = 0
        for c in self.careers:
            t += c.terms

        return t

    @property
    def career_names(self) -> List[str]:
        return [c.career_type.name for c in self.careers]

    @property
    def available_education_skills(self) -> List[str]:
        education_skills = [
            'Admin', 'Advocate', 'Animals', 'Carousing', 'Comms', 'Computer', 'Electronics', 'Engineering',
            'Life Sciences', 'Linguistics', 'Mechanics', 'Medicine', 'Physical Sciences', 'Social Sciences', 'Space Sciences'
        ]

        for s in self.skills:
            try:
                education_skills.remove(s.name)
            except ValueError:
                pass

        return education_skills

    def acquire_skill(self, skill: Skill, upgrade=False) -> Optional[Skill]:
        acquired: Optional[Skill] = None

        if skill.name in skills:
            try:
                i = [s.name for s in self.skills].index(skill.name)

                if upgrade:
                    self.skills[i].level += 1
                    acquired = self.skills[i]
                elif self.skills[i].level < skill.level:
                    self.skills[i].level = skill.level
                    acquired = self.skills[i]
            except ValueError:
                self.skills.append(skill)
                acquired = skill

        return acquired

    def qualify(self, ct: CareerType, drafted=False) -> (bool, Optional[List[str]]):
        acquired_skills: Optional[List[Skill]] = None
        qualified: bool

        if drafted:
            qualified = True
        else:
            if ct.name in self.available_careers:
                self.available_careers.remove(ct.name)
            v = dice.roll(2) + self.modifier(ct.qualification[0]) - 2 * len(self.careers)
            qualified = v >= ct.qualification[1]

        can_join: bool = ct == drifter or drafted or ct.name not in self.career_names

        if qualified and can_join:
            self.careers.append(Career(ct, drafted))

            # If it's the first career, acquire every skill in service skills at lev 0
            if len(self.careers) == 1:
                acquired_skills = []

                for s in ct.skill_and_training[1].values():
                    skill = Skill(s, 0)
                    if self.acquire_skill(skill):
                        acquired_skills.append(skill)

        return qualified, acquired_skills

    def survival_roll(self) -> bool:
        c = self.careers[-1]

        v = dice.roll(2) + self.modifier(c.career_type.survival[0])
        return v >= c.career_type.survival[1]

    def mishaps_roll(self) -> Tuple[str, int]:
        char: Characteristic
        message: str

        mishaps = dice.roll()
        if mishaps == 1:
            char = Random().choice(Characteristic.physical())
            d = dice.roll()
            self.stats[char] -= d
            message = 'You were severely injured during service and thus have been medically discharged.'
        elif mishaps == 2:
            message = 'You were honorably discharged from the service.'
        elif mishaps == 3:
            self.debt += 10_000
            message = 'You were honorably discharged from the service after a long legal battle. Legal issues create a debt of Cr10,000.'
        elif mishaps == 4:
            # TODO Lose career benefits
            self.lose_benefits = True
            message = 'You were dishonorably discharged from the service, you lost all benefits.'
        elif mishaps == 5:
            char = Random().choice(Characteristic.physical())
            d = dice.roll()
            self.stats[char] -= 1
            message = 'You were dishonorably discharged from the service after serving 4 years in prison for a crime. You lose all benefits.'
            # TODO AGE PRISON
        else:  # mishaps == 6
            injury = dice.roll()
            if injury == 1:
                char = Random().choice(Characteristic.physical())
                d = dice.roll()
                self.stats[char] -= d

                for c in Characteristic.physical():
                    if c != char:
                        self.stats[c] -= 2
                message = 'You were nearly killed during service and thus have been medically discharged.'
            elif injury == 2:
                char = Random().choice(Characteristic.physical())
                d = dice.roll()
                self.stats[char] -= d
                message = 'You were severely injured during service and thus have been medically discharged.'
            elif injury == 3:
                char = Random().choice([Characteristic.STR, Characteristic.DEX])
                self.stats[char] -= 2
                message = 'You were nearly killed during service and thus have been medically discharged.'
            elif injury == 4:
                char = Random().choice(Characteristic.physical())
                self.stats[char] -= 2
                message = 'You were scarred and injured during service and thus have been medically discharged.'
            elif injury == 5:
                char = Random().choice(Characteristic.physical())
                self.stats[char] -= 1
                message = 'You were injured during service and thus have been medically discharged.'
            else:
                message = 'You were lightly injured during service and thus have been medically discharged.'

        crisis_debt: int = 0
        for c in Characteristic:
            self.stats[c] = max(self.stats[c], 0)

            if self.stats[c] == 0:
                v = 10_000 * dice.roll()
                crisis_debt += v
                self.injury_crisis_debt += v
                self.stats[c] = 1

        return message, crisis_debt

    def draft(self) -> CareerType:
        draft_careers: List[str] = ['Aerospace Defense', 'Marine', 'Maritime Defense', 'Navy', 'Scout', 'Surface Defense']
        c = Random().choice(draft_careers)

        return careers[c]

    @property
    def drafted(self) -> bool:
        return self.careers[-1].drafted

    def commission_roll(self) -> Tuple[Optional[bool], Optional[Skill]]:
        if self.career.rank == 0 and self.career.career_type.commission:
            v = dice.roll(2) + self.modifier(self.career.career_type.commission[0])
            if v >= self.career.career_type.commission[1]:
                self.career.rank += 1

                # Ranks
                acquired_skill: Optional[Skill] = None
                s = self.career.career_type.ranks.get(self.career.rank)
                if s:
                    acquired_skill = self.acquire_skill(Skill(s, 1), upgrade=False)
                return True, acquired_skill
            return False, None
        return None, None

    def advancement_roll(self) -> Tuple[Optional[bool], Optional[str]]:
        if self.career.rank >= 1 and self.career.career_type.advancement:
            v = dice.roll(2) + self.modifier(self.career.career_type.advancement[0])
            if v >= self.career.career_type.advancement[1]:
                self.career.rank += 1

                # Ranks
                acquired_skill: Optional[Skill] = None
                s = self.career.career_type.ranks.get(self.career.rank)
                if s:
                    acquired_skill = self.acquire_skill(Skill(s, 1), upgrade=False)
                return True, acquired_skill
            return False, None
        return None, None

    def skills_and_training(self, table_name: str) -> Union[Characteristic, Skill]:
        index = ['Personal Development', 'Service Skills', 'Specialist Skills', 'Advanced Education'].index(table_name)

        upgrade: Union[Characteristic, str, Skill] = Random().choice(list(self.career.career_type.skill_and_training[index].values()))
        if isinstance(upgrade, Characteristic):
            self.stats[upgrade] += 1
        else:
            upgrade = self.acquire_skill(Skill(upgrade, 0), upgrade=True)

        return upgrade

    def use_drugs(self, use: bool) -> Optional[Tuple[bool, int]]:
        if use:
            self.took_drugs = True
            self.drugs_terms += 1
            self.debt += 2500
        elif self.drugs_terms > 0:
            self.took_drugs = False
            success, crisis = self.aging_roll()
            self.drugs_terms = 0
            return success, crisis

        return None

    def increase_age(self) -> Tuple[bool, int]:
        self.age += 4

        if self.age >= 34 and not self.took_drugs:
            return self.aging_roll()

        return True, 0

    def aging_roll(self) -> Tuple[bool, int]:  # TODO Return something
        v = dice.roll(2) - self.terms + self.drugs_terms

        """
        –6 Reduce three physical characteristics by 2, reduce one mental characteristic by 1
        –5 Reduce three physical characteristics by 2.
        –4 Reduce two physical characteristics by 2, reduce one physical characteristic by 1
        –3 Reduce one physical characteristic by 2, reduce two physical characteristic by 1
        –2 Reduce three physical characteristics by 1
        –1 Reduce two physical characteristics by 1
        0 Reduce one physical characteristic by 1
        1+ No effect
        """
        if v >= 1:
            return True, 0

        if -2 <= v <= 0:
            chars = Characteristic.physical()
            for i in range(abs(v) + 1):
                c = Random().choice(chars)
                self.stats[c] -= 1
                chars.remove(c)
        if v == -3 or v == -4:
            chars = Characteristic.physical()
            n = abs(v) - 2
            for i in range(n):
                c = Random().choice(chars)
                self.stats[c] -= 2
                chars.remove(c)
            for i in range(3 - n):
                c = Random().choice(chars)
                self.stats[c] -= 1
                chars.remove(c)
        if v == -5 or v == -6:
            for c in Characteristic.physical():
                self.stats[c] -= 2

            if v == -6:
                c = Random().choice(Characteristic.mental())
                self.stats[c] -= 1

        crisis: int = 0
        for c in Characteristic:  # TODO Replicated check_crisis
            self.stats[c] = max(self.stats[c], 0)

            if self.stats[c] == 0:
                v = 10_000 * dice.roll()
                crisis += v
                self.injury_crisis_debt += v
                self.stats[c] = 1

        return False, crisis

    def reenlistment_roll(self, adventure_terms: int) -> ReEnlistmentOutcome:
        v = dice.roll(2)

        if v == 12:
            return ReEnlistmentOutcome.FORCED_CONTINUE

        if self.terms >= adventure_terms >= 0:
            self.retire()
            return ReEnlistmentOutcome.MUST_RETIRE

        if v >= self.career.career_type.re_enlistment:
            return ReEnlistmentOutcome.SUCCESS

        return ReEnlistmentOutcome.FAIL

    def continue_career(self):
        self.career.terms += 1

    def retire(self):
        self.retired = True

    def compute_benefit_rolls(self, failed_survival: bool):
        if self.lose_benefits:
            self.benefit_rolls = 0
            self.lose_benefits = False
        else:
            self.benefit_rolls = self.career.terms + max(0, self.career.rank - 3)
            if failed_survival:
                self.benefit_rolls -= 1

        self.cash_rolls = 3

    def roll_benefit(self, cash: bool) -> Union[int, Weapon, Characteristic, str, Skill]:
        self.benefit_rolls -= 1
        if cash:
            v = dice.roll()
            if "Gambling" in self.skill_names or self.retired:
                v += 1

            creds = self.career.career_type.cash[v]
            self.credits += creds
            self.cash_rolls -= 1
            return creds

        v = dice.roll()
        if self.career.rank >= 5:
            v += 1

        benefit: Union[str, int, Characteristic] = self.career.career_type.material_benefits[v]
        if isinstance(benefit, Characteristic):
            self.stats[benefit] += 1
            return benefit

        if isinstance(benefit, int):
            if benefit == -1:
                benefit = dice.roll()

            self.ship_shares += benefit
            return benefit

        if isinstance(benefit, str):
            if benefit == 'Society':
                self.society = True
                return benefit

            weapon_id: int
            if benefit == 'LightWeapon':
                weapon_id = Random().choice([109, 116, 118])
            elif benefit == 'HeavyWeapon':
                weapon_id = Random().choice([110, 111, 113, 114, 117])
            elif benefit == 'Rifle':
                weapon_id = Random().choice([124, 127, 132, 133, 134, 135])
            elif benefit == 'Pistol':
                weapon_id = Random().choice([121, 122, 129, 130, 131, 136])
            elif benefit == 'Shotgun':
                weapon_id = Random().choice([123, 125])
            elif benefit == 'AssaultWeapon':
                weapon_id = Random().choice([126, 128])
            elif benefit == 'Sword':
                weapon_id = Random().choice([112])
            else:  # benefit =='Bow':
                weapon_id = Random().choice([119, 120])

            for eq, qt in self.inventory:
                if eq.id == weapon_id:
                    skill = 'Melee Combat' if benefit in ['LightWeapon', 'HeavyWeapon', 'Sword'] else 'Gun Combat'
                    return self.acquire_skill(Skill(skill, 0), upgrade=True)

            self.inventory.append((equipments[weapon_id], 1))
            return cast(Weapon, equipments[weapon_id])

    def write(self, user_id, adventure_id, db: connection):
        with db:
            with db.cursor() as cur:
                cur.execute('INSERT INTO characters '
                            'VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                            'ON CONFLICT DO NOTHING RETURNING id;', (
                                self.name, self.sex.value, True, user_id, adventure_id,
                                self.stats[Characteristic.STR],
                                self.stats[Characteristic.DEX],
                                self.stats[Characteristic.END],
                                self.stats[Characteristic.INT],
                                self.stats[Characteristic.EDU],
                                self.stats[Characteristic.SOC],
                                self.credits, None, None, None, self.stance, self.rads,
                                self.is_fatigued, self.stims_taken
                            ))
                char_id = cur.fetchone()[0]
                for eq, qt in self.inventory:
                    cur.execute('INSERT INTO inventories VALUES(%s, %s, %s, 0);', (char_id, eq.id, qt))
                for skill in self.skills:
                    cur.execute('INSERT INTO skill_sets VALUES(%s, %s, %s);', (char_id, skill.name, skill.level))

    @property
    def stats_tuple(self) -> Tuple[int, int, int, int, int, int]:
        return (
            self.stats[Characteristic.STR],
            self.stats[Characteristic.END],
            self.stats[Characteristic.DEX],
            self.stats[Characteristic.INT],
            self.stats[Characteristic.EDU],
            self.stats[Characteristic.SOC]
        )