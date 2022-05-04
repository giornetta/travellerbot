import json
import random
from re import finditer

from psycopg2.extensions import connection
from PIL import Image
import requests
from typing import List, Dict, Tuple
import traveller.equipment as eq

from referee.command_parser import CommandParser
from traveller.common import Characteristics as Ch


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

    # TODO this needs to be integrated with telegram

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
                        for planet in data[sector]:
                            if planet[0] == world:
                                uwp = planet[1]
                                break
                    return True, \
                           'The Starport level is: ' + uwp[0] + \
                           'The World Size level is: ' + uwp[1] + \
                           'The Atmosphere level is: ' + uwp[2] + \
                           'The Hydrographics level is: ' + uwp[3] + \
                           'The Population level is: ' + uwp[4] + \
                           'The Government level is: ' + uwp[5] + \
                           'The Law Level is: ' + uwp[6] + \
                           'The Technology level is: ' + uwp[8]

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
                    title, sector, world, max_terms, survival_fail_kills = cur.fetchone()
                    return True, \
                           'The title of the adventure is: ' + title + \
                           '\nThe current sector is: ' + sector + \
                           '\nThe current world is: ' + world + \
                           '\nThe max terms an adventurer can do is: ' + str(max_terms) + \
                           '\nIn this adventure failing a survival roll ' + \
                           'kills' if survival_fail_kills else 'Doesn\'t kill'
                else:
                    cur.execute('SELECT sex, age, strength, dexterity, endurance, '
                                'intelligence, education, social_standing, '
                                'str_mod, dex_mod, end_mod, int_mod, edu_mod, soc_mod, credits, '
                                'equipped_armor, drawn_weapon, stance, rads, wounded, fatigued, stims_taken '
                                'FROM characters WHERE char_name = %s AND adventure_id = %s;', (info, adv_id))
                    player_info = cur.fetchone()
                    if not player_info:
                        return False, 'No one has this name'
                    sex, age, strength, dexterity, endurance, intelligence, education, social_standing, \
                    str_mod, dex_mod, end_mod, int_mod, edu_mod, soc_mod, credits_holded, \
                    equipped_armor, drawn_weapon, stance, rads, wounded, fatigued, stims_taken = player_info
                    stance_mod = ['prone', 'crouched', 'standing']
                    return True, \
                           info + 'is ' + ('Male, he is ' if sex == 'M' else 'Female, she is ') + age + \
                           '\nCharacteristics: ' + str(strength) + ',' + str(dexterity) + ',' + \
                           str(endurance) + ',' + str(intelligence) + ',' + \
                           str(education) + ',' + str(social_standing) + \
                           '\nModifiers: ' + str(str_mod) + ',' + str(dex_mod) + ',' + \
                           str(end_mod) + ',' + str(int_mod) + ',' + \
                           str(edu_mod) + ',' + str(soc_mod) + \
                           '\n Credits remaining: ' + str(credits_holded) + \
                           ('\n Equipped armor is:' + eq.equipments[equipped_armor].name if equipped_armor else '') + \
                           ('\n Drawn weapon is:' + eq.equipments[drawn_weapon].name if drawn_weapon else '') + \
                           '\nThe actual stance is: ' + stance_mod[stance] + \
                           '\nThe rads count is: ' + str(rads) + \
                           ('\nThe player is wounded' if wounded else '') + \
                           ('\nThe player is fatigued' if fatigued else '') + \
                           ('\nThe player has taken' + str(stims_taken) + 'stims' if stims_taken > 0 else '')

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
                if cmd[1] == 'wounded' or cmd[1] == 'fatigued':
                    cur.execute('UPDATE characters SET %s = %s WHERE id = %s;',
                                (cmd[1], value == 1, char_id))  # If status is non-existent it does nothing
                    return True
                return False, 'No such status exists'
            if cmd[0] == 'cr' or cmd[0] == 'credits':
                cur.execute('UPDATE characters SET credits = %s WHERE id = %s;', (value, char_id))
                return True
            if cmd[0] == 'inv' or cmd[0] == 'inventory' or cmd[0] == 'equipment':
                if cmd[1] == 'rm' or cmd[1] == 'remove':
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
                            e = e + level - 7
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
                            e = e + level - 7
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

    def shop(self, cmd: List[str]) -> (bool, str):  # TODO add closing shop
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
                    cur.execute('UPDATE characters SET fatigued = FALSE WHERE adventure_id = %s AND alive = TRUE;',
                                (adv_id,))
                    return True
                if cmd == 'long':
                    cur.execute('UPDATE characters SET fatigued = FALSE WHERE adventure_id = %s AND alive = TRUE;',
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
                cur.execute('UPDATE adventures SET scene_id = NULL WHERE id = %s;', (adv_id,))
                return True
            else:
                cur.execute('UPDATE adventures SET scene_id = %s WHERE id = %s;',
                            (combat, adv_id))  # check if it doesn't exist?
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
