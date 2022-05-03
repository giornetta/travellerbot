import json
import random
from re import finditer

from psycopg2.extensions import connection
from PIL import Image
import requests
from typing import List, Dict
import traveller.equipment as eq

from referee.command_parser import CommandParser
from traveller.common import Characteristics as Ch


class RefereeCommands:
    db: connection
    referee_id: int
    cp: CommandParser

    def __init__(self, db: connection, referee_id: int):
        self.db = db
        self.referee_id = referee_id
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

    # TODO tuesday we will integrate it in telegram, right now I'm just doing queries

    def info(self, info: str) -> (bool, str):
        with self.db:
            with self.db.cursor() as cur:
                cur.execute('SELECT active_adventure FROM users WHERE id = %s;', (self.referee_id,))
                adv_id = cur.fetchone()[0]
                if info == 'world':
                    cur.execute('SELECT planet, sector FROM adventures WHERE id = %s;', (adv_id,))
                    world, sector = cur.fetchone()
                    with open('data/map.json') as d:
                        data = json.load(d)
                        uwp = data[sector][1]
                    # TODO send info
                    return True, 'Put here nice and clear result'
                elif info == 'map':
                    cur.execute('SELECT sector FROM adventures WHERE id = %s;', (adv_id,))
                    sector = cur.fetchone()[0]
                    url = 'https://travellermap.com/api/poster?sector=' + sector
                    map = Image.open(requests.get(url, stream=True).raw)
                    # TODO send info
                    return True
                elif info == 'scene':
                    pass  # TODO
                elif info == 'adventure':
                    cur.execute(
                        'SELECT title,sector,planet,max_terms,survival_fail_kills FROM adventures WHERE id = %s;'
                        , (adv_id,))
                    title, sector, planet, max_terms, survival_fail_kills = cur.fetchone()
                    # TODO send info
                    return True
                else:
                    cur.execute('SELECT * FROM characters WHERE char_name = %s AND adventure_id = %s;', (info, adv_id))
                    cur.fetchone()  # Returns None if empty
                    # TODO send info
                    return True

    def set(self, name: str, cmd: List[str], value: str) -> (bool, str):
        with self.db:
            with self.db.cursor() as cur:
                cur.execute('SELECT active_adventure FROM users WHERE id = %s;', (self.referee_id,))
                adv_id = cur.fetchone()[0]
                cur.execute('SELECT id FROM characters WHERE char_name = %s AND adventure_id = %s and alive = TRUE;',
                            (name, adv_id))
                char_id_tuple = cur.fetchone()
                if not char_id_tuple:
                    return False, 'No one has this name'
                char_id = char_id_tuple[0]
            if cmd[0] == 'stat':
                cur.execute('UPDATE characters SET %s = %s WHERE id = %s;', (cmd[1], value, char_id))
                return True
            if cmd[0] == 'status':
                cur.execute('UPDATE characters SET %s = %s WHERE id = %s;',
                            (cmd[1], value == 1, char_id))  # If status is non-existent it does nothing
                return True
            if cmd[0] == 'cr' or 'credits':
                cur.execute('UPDATE characters SET %s = %s WHERE id = %s;', (cmd[1], value, char_id))
                return True
            if cmd[0] == 'inv' or 'inventory' or 'equipment':
                if cmd[1] == 'rm' or 'remove':  # Change name of equipments or parse command?
                    # From now on it will be Eqtype.Eqname.EventualLevel and it will be case-insensitive
                    for i in range(2, len(cmd)):
                        command = cmd[i]
                        splitted = command.split('.', 3)
                        c = splitted[0]
                        eq_name = splitted[1]
                        if eq_name == 'Computer':
                            level = int(splitted[2])
                            for e in eq.equipments:
                                if eq.equipments[e].technology_level == 7:
                                    break
                            e = e + level
                            cur.execute('DELETE FROM inventories WHERE character_id = %s '
                                        'AND equipment_id = %s;', (e, char_id))
                        for e in eq.equipments:
                            if self.is_coherent(c, e):
                                if eq_name.upper() == eq.equipments[i].name:
                                    cur.execute('DELETE FROM inventories WHERE character_id = %s '
                                                'AND equipment_id = %s;', (e, char_id))
                    return True
                if cmd[1] == 'add':
                    for i in range(2, len(cmd) - 1):
                        command = cmd[i]
                        splitted = command.split('.', 3)
                        c = splitted[0]
                        eq_name = splitted[1]
                        if eq_name == 'Computer':
                            level = int(splitted[2])
                            for e in eq.equipments:
                                if eq.equipments[e].technology_level == 7:
                                    break
                            e = e + level
                        else:
                            for e in eq.equipments:
                                if self.is_coherent(c, e):
                                    if eq_name.upper() == eq.equipments[i].name:
                                        break
                cur.execute('SELECT amount FROM inventories WHERE equipment_id = %s and character_id = %s;',
                            (e, char_id))
                amount = cur.fetchone()
                if amount:
                    cur.execute('UPDATE inventories '
                                'SET character_id = %s,equipment_id = %s,amount = %s,damage = 0;',
                                (char_id, e, amount[0] + value))
                else:
                    cur.execute('INSERT INTO inventories(character_id, equipment_id, amount, damage) '
                                'VALUES(%s, %s, %s, %s);', (char_id, e, value, 0))

    def shop(self, cmd: List[str]) -> (bool, str):
        with self.db:
            with self.db.cursor() as cur:
                cur.execute('SELECT active_adventure FROM users WHERE id = %s;', (self.referee_id,))
                adv_id = cur.fetchone()[0]
                if cmd[-1] == 'close':
                    cur.execute('DELETE FROM shop WHERE adventure_id = %s;', (adv_id,))
                    return True
                for c in cmd:  # Check to see if existing shop?
                    for e in eq.equipments:
                        if self.is_coherent(c, e):
                            cur.execute(
                                'INSERT INTO shop(adventure_id, equipment_id) VALUES(%s,%s) ON CONFLICT DO NOTHING;',
                                (adv_id, e))
                    return True

    def rest(self, cmd: str) -> (bool, str):
        with self.db:
            with self.db.cursor() as cur:
                cur.execute('SELECT active_adventure FROM users WHERE id = %s;', (self.referee_id,))
                adv_id = cur.fetchone()[0]
                if cmd == 'short':
                    cur.execute('UPDATE characters SET is_fatigued = FALSE WHERE adventure_id = %s AND alive = TRUE;',
                                (adv_id,))
                    return True
                if cmd == 'long':
                    cur.execute('UPDATE characters SET is_fatigued = FALSE WHERE adventure_id = %s AND alive = TRUE;',
                                (adv_id,))
                    cur.execute('UPDATE characters SET str_mod = 0, dex_mod = 0, end_mod = 0, '
                                'int_mod = 0, edu_mod = 0, soc_mod = 0')
                    return True
            return False

    def combat(self, combat: str, end: str) -> (bool, str):
        with self.db:
            with self.db.cursor() as cur:
                cur.execute('SELECT active_adventure FROM users WHERE id = %s;', (self.referee_id,))
                adv_id = cur.fetchone()[0]
            if end:
                cur.execute('UPDATE adventures SET combat_id = NULL WHERE id = %s;', (adv_id,))
                return True
            else:
                cur.execute('UPDATE adventures SET combat_id = %s WHERE id = %s;',
                            (combat, adv_id))  # check if no exists?
                return True

    def travel(self, world: str) -> (bool, str):
        with self.db:
            with self.db.cursor() as cur:
                cur.execute('SELECT active_adventure FROM users WHERE id = %s;', (self.referee_id,))
                adv_id = cur.fetchone()[0]
                cur.execute('UPDATE adventures SET planet = %s WHERE id = %s;', (world, adv_id))
                return True

    def age(self, drug_users: List[str], drug_droppers: List[str]) -> (bool, str):
        with self.db:
            with self.db.cursor() as cur:
                cur.execute('SELECT active_adventure FROM users WHERE id = %s;', (self.referee_id,))
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

    def scene(self, new: str, name: str) -> (bool, str):
        if new != 'new':
            return False
        with self.db:
            with self.db.cursor() as cur:
                cur.execute('SELECT active_adventure FROM users WHERE id = %s;', (self.referee_id,))
                adv_id = cur.fetchone()[0]
        # discuss about scenes in database

    def exit(self) -> (bool, str):
        with self.db:
            with self.db.cursor() as cur:
                cur.execute('UPDATE users SET active_adventure = NULL WHERE id = %s', (self.referee_id,))

    def is_coherent(self, c: str, i: int):
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
        roll = max(random.randint(1, 6) + random.randint(1, 6) - ((age - 18) // 4), -6)
        dmg: Dict[Ch, int]
        dmg[Ch.STR] = dmg[Ch.DEX] = dmg[Ch.END] = dmg[Ch.INT] = dmg[Ch.EDU] = dmg[Ch.SOC] = 0
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
        cur.execute('UPDATE characters SET '
                    'endurance = endurance-%s, strength = strength-%s,'
                    'dexterity = dexterity-%s, intelligence = intelligence-%s,'
                    'education = education-%s, social_standing = social_standing - %s '
                    'WHERE char_name = %s AND adventure_id = %s AND alive = TRUE; ',
                    (dmg[Ch.END], dmg[Ch.STR], dmg[Ch.DEX], dmg[Ch.INT], dmg[Ch.EDU], dmg[Ch.SOC],
                     name, adv_id))
        cur.execute('SELECT endurance, strength, dexterity, intelligence, education, social_standing '
                    'FROM characters WHERE char_name = %s and adventure_id = %s and alive = TRUE;',
                    (name, adv_id))
        new_end, new_str, new_dex, new_int, new_edu, new_soc = cur.fetchone()
        if new_end <= 0:
            cur.execute('UPDATE characters SET endurance = 1 '
                        'WHERE char_name = %s AND adventure_id = %s AND alive = TRUE;')
            self.remove_credits(cur, name, adv_id)
        if new_str <= 0:
            cur.execute('UPDATE characters SET strength = 1 '
                        'WHERE char_name = %s AND adventure_id = %s AND alive = TRUE;')
            self.remove_credits(cur, name, adv_id)
        if new_dex <= 0:
            cur.execute('UPDATE characters SET dexterity = 1 '
                        'WHERE char_name = %s AND adventure_id = %s AND alive = TRUE;')
            self.remove_credits(cur, name, adv_id)
        if new_int <= 0:
            cur.execute('UPDATE characters SET intelligence = 1 '
                        'WHERE char_name = %s AND adventure_id = %s AND alive = TRUE;')
            self.remove_credits(cur, name, adv_id)
        if new_edu <= 0:
            cur.execute('UPDATE characters SET education = 1 '
                        'WHERE char_name = %s AND adventure_id = %s AND alive = TRUE;')
            self.remove_credits(cur, name, adv_id)
        if new_soc <= 0:
            cur.execute('UPDATE characters SET social_standing = 1 '
                        'WHERE char_name = %s AND adventure_id = %s AND alive = TRUE;')
            self.remove_credits(cur, name, adv_id)
        cur.execute('SELECT credits FROM characters '
                    'WHERE char_name = %s AND adventure_id = %s AND alive = TRUE;')
        credits_remaining = cur.fetchone()[0]
        if credits_remaining < 0:
            pass  # DIES

    def remove_credits(self, cur, name, adv_id):
        removed = random.randint(1, 6) * 10000
        cur.execute('UPDATE characters SET credits = credits - %s '
                    'WHERE char_name = %s AND adventure_id = %s AND alive = TRUE;', (removed, name, adv_id))
