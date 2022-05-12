import json
import random

from psycopg2.extensions import connection
from typing import List, Dict, Tuple
import traveller.equipment as eq

from referee.command_parser import CommandParser
from traveller.characteristic import Characteristic as Ch
from travellermap import api


def calculate_age_damage(stats: Tuple, age) -> (Tuple, int):
    roll = max(random.randint(1, 6) + random.randint(1, 6) - ((age - 18) // 4), -6)
    dmg: Dict[Ch, int]
    dmg[Ch.STR] = dmg[Ch.DEX] = dmg[Ch.END] = dmg[Ch.INT] = dmg[Ch.EDU] = dmg[Ch.SOC] = 0
    stre = stats[0]
    dext = stats[1]
    endu = stats[2]
    inte = stats[3]
    educ = stats[4]
    soci = stats[5]
    if roll == -6:
        dmg[Ch.STR] = dmg[Ch.DEX] = dmg[Ch.END] = 2
        dmg[random.choice([Ch.INT, Ch.EDU, Ch.SOC])] = 1
    elif roll == -5:
        dmg[Ch.STR] = dmg[Ch.DEX] = dmg[Ch.END] = 2
    elif roll == -4:
        dmg[Ch.STR] = dmg[Ch.DEX] = dmg[Ch.END] = 2
        dmg[random.choice([Ch.STR, Ch.DEX, Ch.END])] = 1
    elif roll == -3:
        dmg[Ch.STR] = dmg[Ch.DEX] = dmg[Ch.END] = 1
        dmg[random.choice([Ch.STR, Ch.DEX, Ch.END])] = 2
    elif roll == -2:
        dmg[Ch.STR] = dmg[Ch.DEX] = dmg[Ch.END] = 1
    elif roll == -1:
        dmg[Ch.STR] = dmg[Ch.DEX] = dmg[Ch.END] = 1
        dmg[random.choice([Ch.STR, Ch.DEX, Ch.END])] = 0
    elif roll == 0:
        dmg[random.choice([Ch.STR, Ch.DEX, Ch.END])] = 1
    endu -= dmg[Ch.END]
    stre -= dmg[Ch.STR]
    dext -= dmg[Ch.DEX]
    inte -= dmg[Ch.INT]
    educ -= dmg[Ch.EDU]
    soci -= dmg[Ch.SOC]
    debt = 0
    new_stats = [stre, dext, endu, inte, educ, soci]
    for i in range(6):
        if new_stats[i] <= 0:
            new_stats[i] = 1
            debt += random.randint(1, 6) * 10000
    return tuple(new_stats), debt


class RefereeCommands:
    db: connection
    cp: CommandParser

    def __init__(self, db: connection):
        self.db = db
        self.cp = CommandParser()
        self.cp['info'] = self.info
        self.cp['set'] = self.set
        self.cp['shop'] = self.shop
        self.cp['rest'] = self.rest
        self.cp['combat'] = self.combat
        self.cp['travel'] = self.travel
        self.cp['age'] = self.age
        self.cp['scene'] = self.scene
        self.cp['exit'] = self.exit

    # TODO this needs to be integrated with telegram

    def info(self, info: str, referee_id: int) -> (bool, str):
        with self.db:
            with self.db.cursor() as cur:
                cur.execute('SELECT active_adventure FROM users WHERE id = %s;', (referee_id,))
                adv_id = cur.fetchone()[0]
                if info == 'scene':
                    cur.execute('SELECT scene_id FROM adventures WHERE id=%s;', (adv_id,))
                    scene_id = cur.fetchone()
                    if scene_id:
                        scene_id = scene_id[0]
                        cur.execute('SELECT scene_name FROM scenes WHERE id=%s;', (scene_id,))
                        scene_name = cur.fetchone()
                        if scene_name:
                            scene_name = scene_name[0]
                            return True, 'The active scene is ' + scene_name
                        else:
                            return False, 'No active scene'
                    else:
                        return False, 'No active scene'
                elif info == 'world':
                    cur.execute('SELECT planet, sector FROM adventures WHERE id = %s;', (adv_id,))
                    world, sector = cur.fetchone()
                    with open('data/map.json') as d:
                        data = json.load(d)
                        for planet in data[sector]:
                            if planet[0] == world:
                                uwp = planet[1]
                                break
                    return True, \
                           'Name:' + world + \
                           'Starport: ' + uwp[0] + \
                           '\nWorld Size: ' + uwp[1] + \
                           '\nAtmosphere: ' + uwp[2] + \
                           '\nHydrographics: ' + uwp[3] + \
                           '\nPopulation: ' + uwp[4] + \
                           '\nGovernment: ' + uwp[5] + \
                           '\nLaw level: ' + uwp[6] + \
                           '\nTechnology level: ' + uwp[8]

                elif info == 'map':
                    cur.execute('SELECT sector,planet FROM adventures WHERE id = %s;', (adv_id,))
                    sector, world_name = cur.fetchone()
                    world = api.world(sector, world_name)
                    url = f'https://travellermap.com/api/jumpmap?sector={sector.replace(" ", "%20")}&hex={world.hexc}'
                    return True, url
                elif info == 'adventure':
                    cur.execute('SELECT id,title,sector,planet,max_terms,survival_fail_kills '
                                'FROM adventures WHERE id = %s;'
                                , (adv_id,))
                    id, title, sector, world, max_terms, survival_fail_kills = cur.fetchone()
                    text = 'Code: ' + id + \
                           '\nTitle: ' + title + \
                           '\nSector: ' + sector + \
                           '\nWorld: ' + world + \
                           '\nMax terms: ' + str(max_terms) + \
                           '\nFailing a survival roll ' + \
                           ('kills' if survival_fail_kills else 'doesn\'t kill') + \
                           '\nAdventurers:'
                    cur.execute('SELECT char_name FROM characters WHERE adventure_id=%s AND alive = TRUE;',
                                (adv_id,))
                    names = cur.fetchall()
                    for name in names:
                        text = text + '\n' + name[0]
                    return True, text
                else:
                    cur.execute('SELECT id,sex, age, strength, dexterity, endurance, '
                                'intelligence, education, social_standing, '
                                'str_mod, dex_mod, end_mod, int_mod, edu_mod, soc_mod, credits, '
                                'equipped_armor, drawn_weapon, stance, rads, wounded, fatigued, stims_taken '
                                'FROM characters WHERE char_name = %s AND adventure_id = %s;', (info, adv_id))
                    player_info = cur.fetchone()
                    if not player_info:
                        return False, 'No one has this name'
                    character_id, sex, age, strength, dexterity, endurance, intelligence, education, social_standing, \
                    str_mod, dex_mod, end_mod, int_mod, edu_mod, soc_mod, credits_holded, \
                    equipped_armor, drawn_weapon, stance, rads, wounded, fatigued, stims_taken = player_info
                    stance_mod = ['prone', 'crouched', 'standing']
                    cur.execute('SELECT equipment_id, amount FROM inventories '
                                'WHERE character_id = %s;', (character_id,))
                    inventory = cur.fetchall()
                    text = f'Name: {info}\nSex: {sex}\nAge:{age}' \
                           f'\nCharacteristics:{strength},{dexterity},{endurance},' \
                           f'{intelligence},{education},{social_standing}' \
                           f'\nModifiers: {str_mod},{dex_mod},{end_mod},{int_mod},{edu_mod},{soc_mod}' \
                           f'\nCredits: {credits_holded}' \
                           f'\nStance: {stance_mod[stance]}' \
                           f'\nRads: {rads}' \
                           f'\nWounded: {wounded}' \
                           f'\nFatigued: {fatigued}'
                    if equipped_armor:
                        text = text + f'\nEquipped armor: {eq.equipments[equipped_armor].name}'
                    if drawn_weapon:
                        text = text + f'\nDrawn weapon: {eq.equipments[drawn_weapon].name}'
                    text = text + f'\nInventory:'
                    for eq_id in inventory:
                        text = text + '\n'
                        text = text + eq.equipments[eq_id[0]].name
                        if self.is_coherent('Computer', eq_id[0]) or self.is_coherent('Software', eq_id[0]):
                            level = eq.equipments[eq_id[0]].technology_level
                            text = text + f'LVL{level}'
                        text = text + ': '
                        text = text + str(eq_id[1])
                    return True, text

    def set(self, name: str, cmd: List[str], value: str, referee_id: int) -> (bool, str):
        with self.db:
            with self.db.cursor() as cur:
                cur.execute('SELECT active_adventure FROM users WHERE id = %s;', (referee_id,))
                adv_id = cur.fetchone()[0]
                cur.execute('SELECT id FROM characters WHERE char_name = %s AND adventure_id = %s and alive = TRUE;',
                            (name, adv_id))
                char_id_tuple = cur.fetchone()
                if not char_id_tuple:
                    return False, 'No one has this name'
                char_id = char_id_tuple[0]
                if cmd[0] == 'strength' or cmd[0] == 'str':
                    cur.execute('UPDATE characters SET strength = %s WHERE id = %s;', (value, char_id))
                    return True, 'Updated with success'
                if cmd[0] == 'dexterity' or cmd[0] == 'dex':
                    cur.execute('UPDATE characters SET dexterity = %s WHERE id = %s;', (value, char_id))
                    return True, 'Updated with success'
                if cmd[0] == 'endurance' or cmd[0] == 'end':
                    cur.execute('UPDATE characters SET endurance = %s WHERE id = %s;', (value, char_id))
                    return True, 'Updated with success'
                if cmd[0] == 'intelligence' or cmd[0] == 'int':
                    cur.execute('UPDATE characters SET intelligence = %s WHERE id = %s;', (value, char_id))
                    return True, 'Updated with success'
                if cmd[0] == 'education' or cmd[0] == 'edu':
                    cur.execute('UPDATE characters SET education = %s WHERE id = %s;', (value, char_id))
                    return True, 'Updated with success'
                if cmd[0] == 'social_standing' or cmd[0] == 'soc':
                    cur.execute('UPDATE characters SET social_standing = %s WHERE id = %s;', (value, char_id))
                    return True, 'Updated with success'
                if cmd[0] == 'mod_str' or cmd[0] == 'modifier_str' \
                        or cmd[0] == 'mod_strength' or cmd[0] == 'modifier_strength':
                    cur.execute('UPDATE characters SET str_mod = %s WHERE id = %s;', (value, char_id))
                    return True, 'Updated with success'
                if cmd[0] == 'mod_dex' or cmd[0] == 'modifier_dex' \
                        or cmd[0] == 'mod_dexterity' or cmd[0] == 'modifier_dexterity':
                    cur.execute('UPDATE characters SET dex_mod = %s WHERE id = %s;', (value, char_id))
                    return True, 'Updated with success'
                if cmd[0] == 'mod_end' or cmd[0] == 'modifier_end' \
                        or cmd[0] == 'mod_endurance' or cmd[0] == 'modifier_endurance':
                    cur.execute('UPDATE characters SET end_mod = %s WHERE id = %s;', (value, char_id))
                    return True, 'Updated with success'
                if cmd[0] == 'mod_int' or cmd[0] == 'modifier_int' \
                        or cmd[0] == 'mod_intelligence' or cmd[0] == 'modifier_intelligence':
                    cur.execute('UPDATE characters SET int_mod = %s WHERE id = %s;', (value, char_id))
                    return True, 'Updated with success'
                if cmd[0] == 'mod_edu' or cmd[0] == 'modifier_edu' \
                        or cmd[0] == 'mod_education' or cmd[0] == 'modifier_education':
                    cur.execute('UPDATE characters SET edu_mod = %s WHERE id = %s;', (value, char_id))
                    return True, 'Updated with success'
                if cmd[0] == 'mod_soc' or cmd[0] == 'modifier_soc' \
                        or cmd[0] == 'mod_social_standing' or cmd[0] == 'modifier_social_standing':
                    cur.execute('UPDATE characters SET soc_mod = %s WHERE id = %s;', (value, char_id))
                    return True, 'Updated with success'
                if cmd[0] == 'mod' or cmd[0] == 'modifier':
                    if cmd[1] == 'str' or cmd[1] == 'strength':
                        cur.execute('UPDATE characters SET str_mod = %s WHERE id = %s;', (value, char_id))
                        return True, 'Updated with success'
                    if cmd[1] == 'dex' or cmd[1] == 'dexterity':
                        cur.execute('UPDATE characters SET dex_mod = %s WHERE id = %s;', (value, char_id))
                        return True, 'Updated with success'
                    if cmd[1] == 'end' or cmd[1] == 'endurance':
                        cur.execute('UPDATE characters SET end_mod = %s WHERE id = %s;', (value, char_id))
                        return True, 'Updated with success'
                    if cmd[1] == 'int' or cmd[1] == 'intelligence':
                        cur.execute('UPDATE characters SET int_mod = %s WHERE id = %s;', (value, char_id))
                        return True, 'Updated with success'
                    if cmd[1] == 'edu' or cmd[1] == 'education':
                        cur.execute('UPDATE characters SET edu_mod = %s WHERE id = %s;', (value, char_id))
                        return True, 'Updated with success'
                    if cmd[1] == 'soc' or cmd[1] == 'social_standing':
                        cur.execute('UPDATE characters SET soc_mod = %s WHERE id = %s;', (value, char_id))
                        return True, 'Updated with success'
                if cmd[0] == 'status':
                    if cmd[1] == 'wounded':
                        cur.execute('UPDATE characters SET wounded = %s WHERE id = %s;',
                                    (value == 1, char_id))
                    if cmd[1] == 'fatigued':
                        cur.execute('UPDATE characters SET fatigued = %s WHERE id = %s;',
                                    (value == 1, char_id))
                        return True, 'Updated with success'
                    return False, 'No such status exists'
                if cmd[0] == 'cr' or cmd[0] == 'credits':
                    cur.execute('UPDATE characters SET credits = %s WHERE id = %s;', (value, char_id))
                    return True, 'Updated with success'
                if cmd[0] == 'inv' or cmd[0] == 'inventory' or cmd[0] == 'equipment':
                    if cmd[1] == 'rm' or cmd[1] == 'remove':
                        # From now on it will be Eqtype:Eqname:EventualLevel and it will be case-insensitive
                        for i in range(2, len(cmd)):
                            command = cmd[i]
                            splitted = command.split(':', 3)
                            c = splitted[0]
                            eq_name = splitted[1]
                            if c == 'Computer' or c == 'Software':
                                level = int(splitted[2])
                                for e in eq.equipments:
                                    if eq.equipments[e].name.replace(" ", "").upper() == eq_name.upper() \
                                            and eq.equipments[e].technology_level == level:
                                        break
                            else:
                                for e in eq.equipments:
                                    if self.is_coherent(c, e):
                                        if eq_name.upper() == eq.equipments[e].name.replace(" ", "").upper():
                                            break
                            cur.execute('UPDATE inventories '
                                        'SET amount = amount - %s '
                                        'WHERE character_id=%s AND equipment_id =%s '
                                        'RETURNING amount',
                                        (value, char_id, e))
                            amount = cur.fetchone()
                            if amount and amount[0] == 0:
                                cur.execute('DELETE FROM inventories WHERE character_id=%s AND equipment_id =%s',
                                            (char_id, e))

                        return True, 'Updated with success'
                    if cmd[1] == 'add':
                        for i in range(2, len(cmd)):
                            command = cmd[i]
                            splitted = command.split(':', 3)
                            c = splitted[0]
                            eq_name = splitted[1]
                            if c.upper() == 'Computer'.upper() or c.upper() == 'Software'.upper():
                                level = int(splitted[2])
                                for e in eq.equipments:
                                    print(eq.equipments[e].technology_level)
                                    if eq.equipments[e].name.replace(" ", "").upper() == eq_name.upper() \
                                            and eq.equipments[e].technology_level == level:
                                        break
                            else:
                                for e in eq.equipments:
                                    if self.is_coherent(c, e):
                                        if eq_name.upper() == eq.equipments[e].name.replace(" ", "").upper():
                                            break
                            cur.execute('SELECT amount FROM inventories WHERE equipment_id = %s and character_id = %s;',
                                        (e, char_id))
                            amount = cur.fetchone()
                            if amount:
                                cur.execute('UPDATE inventories '
                                            'SET amount = %s '
                                            'WHERE character_id = %s AND equipment_id = %s',
                                            (amount[0] + value, char_id, e))
                            else:
                                cur.execute('INSERT INTO inventories(character_id, equipment_id, amount, damage) '
                                            'VALUES(%s, %s, %s, %s);', (char_id, e, value, 0))
                        return True, 'Updated with success'
                return False, 'Cannot set'

    def shop(self, cmd: List[str], referee_id: int) -> (bool, str):
        with self.db:
            with self.db.cursor() as cur:
                cur.execute('SELECT active_adventure FROM users WHERE id = %s;', (referee_id,))
                adv_id = cur.fetchone()[0]
                if cmd[-1] == 'close':
                    cur.execute('DELETE FROM shop WHERE adventure_id = %s;', (adv_id,))
                    return True, 'Shop closed successfully'
                for c in cmd:  # Check to see if existing shop?
                    for e in eq.equipments:
                        if self.is_coherent(c, e):
                            cur.execute(
                                'INSERT INTO shop(adventure_id, equipment_id) VALUES(%s,%s) ON CONFLICT DO NOTHING;',
                                (adv_id, e))
                    return True, 'Shop opened successfully'

    def rest(self, cmd: str, referee_id: int) -> (bool, str):
        with self.db:
            with self.db.cursor() as cur:
                cur.execute('SELECT active_adventure FROM users WHERE id = %s;', (referee_id,))
                adv_id = cur.fetchone()[0]
                if cmd == 'short':
                    cur.execute('UPDATE characters SET fatigued = FALSE WHERE adventure_id = %s AND alive = TRUE;',
                                (adv_id,))
                    return True, 'The party rested shorty'
                if cmd == 'long':
                    cur.execute('UPDATE characters SET fatigued = FALSE WHERE adventure_id = %s AND alive = TRUE;',
                                (adv_id,))
                    cur.execute('UPDATE characters SET str_mod = 0, dex_mod = 0, end_mod = 0, '
                                'int_mod = 0, edu_mod = 0, soc_mod = 0')
                    return True, 'The party rested for a long time'
            return False, 'insert either "short" or "long"'

    def combat(self, combat: str, end: str, referee_id: int) -> (bool, str):
        with self.db:
            with self.db.cursor() as cur:
                cur.execute('SELECT active_adventure FROM users WHERE id = %s;', (referee_id,))
                adv_id = cur.fetchone()[0]
            if end:
                cur.execute('UPDATE adventures SET scene_id = NULL WHERE id = %s;', (adv_id,))
                return True, 'Scene set with success'
            else:
                cur.execute('UPDATE adventures SET scene_id = %s WHERE id = %s;',
                            (combat, adv_id))  # check if it doesn't exist?
                return True, 'Scene set with success'

    def travel(self, world: str, referee_id: int) -> (bool, str):
        with self.db:
            with self.db.cursor() as cur:
                cur.execute('SELECT active_adventure FROM users WHERE id = %s;', (referee_id,))
                adv_id = cur.fetchone()[0]
                cur.execute('UPDATE adventures SET planet = %s WHERE id = %s;', (world, adv_id))
                return True, 'The adventurers traveled successfully'

    def age(self, drug_users: List[str], drug_droppers: List[str], referee_id: int) -> (bool, str):
        with self.db:
            with self.db.cursor() as cur:
                cur.execute('SELECT active_adventure FROM users WHERE id = %s;', (referee_id,))
                adv_id = cur.fetchone()[0]
                cur.execute('SELECT char_name FROM characters WHERE adventure_id = %s', (adv_id,))
                characters = cur.fetchall()
                for t in characters:
                    name = t[0]
                    if name not in drug_users:
                        cur.execute('UPDATE characters SET age = age + 4 '
                                    'WHERE char_name = %s AND adventure_id = %s AND alive = TRUE '
                                    'RETURNING age;',
                                    (name, adv_id))
                        age = cur.fetchone()[0]
                        if age > 34:
                            self.age_damage(age, cur, name, adv_id)
                for name in drug_droppers:
                    self.age_damage(age, cur, name, adv_id)
                    return True, 'The party aged'
        return False, 'Something went wrong'

    def scene(self, cmd: str, name: str, referee_id: int) -> (bool, str):
        if cmd == 'new':
            return True, 'What\'s the name of the scene?'
        elif cmd == 'start':
            if name:
                with self.db:
                    with self.db.cursor() as cur:
                        cur.execute('SELECT active_adventure FROM users WHERE id = %s;', (referee_id,))
                        adv_id = cur.fetchone()[0]
                        cur.execute('SELECT id FROM scenes WHERE scene_name=%s;', (name,))
                        scene_id = cur.fetchone()
                        if scene_id:
                            scene_id = scene_id[0]
                            cur.execute('UPDATE adventures SET scene_id = %s WHERE id=%s;', (scene_id, adv_id))
                            return True, 'Combat started'
                        return False, 'No scene with this name'
            else:
                return False, 'Start combat with /scene start scene_name'
        elif cmd == 'end' or cmd == 'finish':
            with self.db:
                with self.db.cursor() as cur:
                    cur.execute('SELECT active_adventure FROM users WHERE id = %s;', (referee_id,))
                    adv_id = cur.fetchone()[0]
                    cur.execute('UPDATE adventures SET scene_id = NULL WHERE id=%s;', (adv_id,))
                    return True, 'Combat finished'
        elif cmd == 'remove' or cmd == 'rmv':
            if name:
                with self.db:
                    with self.db.cursor() as cur:
                        cur.execute('SELECT active_adventure FROM users WHERE id = %s;', (referee_id,))
                        adv_id = cur.fetchone()[0]
                        cur.execute('SELECT id FROM scenes WHERE scene_name=%s;', (name,))
                        scene_id = cur.fetchone()
                        if scene_id:
                            scene_id = scene_id[0]
                            cur.execute('DELETE FROM scenes WHERE scene_name=%s AND adventure_id=%s;',
                                        (scene_id, adv_id))
                            return True, 'Scene removed'
                        return False, 'No scene with this name'
            else:
                return False, 'Remove scene with /scene remove scene_name'
        else:
            return False, 'Use /scene {new|start|end|remove} [name]'

    def exit(self, referee_id: int) -> (bool, str):
        with self.db:
            with self.db.cursor() as cur:
                cur.execute('UPDATE users SET active_adventure = NULL WHERE id = %s', (referee_id,))
                return True, 'Exit with success'

    def is_coherent(self, c: str, i: int) -> bool:
        e = eq.equipments[i]
        return c.upper() == 'Armor'.upper() and isinstance(e, eq.Armor) or \
               c.upper() == "Communicator".upper() and isinstance(e, eq.Communicator) or \
               c.upper() == "Computer".upper() and isinstance(e, eq.Computer) or \
               c.upper() == "Software".upper() and isinstance(e, eq.Software) or \
               c.upper() == "Drug".upper() and isinstance(e, eq.Drug) or \
               c.upper() == "Explosive".upper() and isinstance(e, eq.Explosive) or \
               c.upper() == "PersonalDevice".upper() and isinstance(e, eq.PersonalDevice) or \
               c.upper() == "SensoryAid".upper() and isinstance(e, eq.SensoryAid) or \
               c.upper() == "Shelter".upper() and isinstance(e, eq.Shelter) or \
               c.upper() == "SurvivalEquipment".upper() and isinstance(e, eq.SurvivalEquipment) or \
               c.upper() == "Tool".upper() and isinstance(e, eq.Tool) or \
               c.upper() == "MeleeWeapon".upper() and isinstance(e, eq.MeleeWeapon) or \
               c.upper() == "RangedWeapon".upper() and isinstance(e, eq.RangedWeapon) or \
               c.upper() == "RangedAmmunition".upper() and isinstance(e, eq.RangedAmmunition) or \
               c.upper() == "WeaponAccessory".upper() and isinstance(e, eq.WeaponAccessory) or \
               c.upper() == "Grenade".upper() and isinstance(e, eq.Grenade) or \
               c.upper() == "HeavyWeapon".upper() and isinstance(e, eq.HeavyWeapon) or \
               c.upper() == "HeavyWeaponAmmunition".upper() and isinstance(e, eq.HeavyWeaponAmmunition)

    def age_damage(self, age, cur, name, adv_id):
        cur.execute('SELECT strength,dexterity,endurance,intelligence,education,social_standing FROM characters '
                    'WHERE char_name = %s AND adventure_id = %s AND alive = TRUE; ',
                    (name, adv_id))
        new_stats, debt = calculate_age_damage(cur.fetchone(), age)
        cur.execute('UPDATE characters SET strength = %s, dexterity = %s, '
                    'endurance = %s ,intelligence = %s,'
                    'education = %s,social_standing = %s, '
                    'credits = credits - %s '
                    'WHERE char_name = %s AND adventure_id = %s AND alive = TRUE;',
                    (*new_stats, debt, name, adv_id))
        cur.execute('SELECT credits FROM characters '
                    'WHERE char_name = %s AND adventure_id = %s AND alive = TRUE;',
                    (name, adv_id))
        credits_remaining = cur.fetchone()[0]
        if credits_remaining < 0:
            pass  # DIES
