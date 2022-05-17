import json
import random

import psycopg2
from psycopg2 import IntegrityError
from psycopg2.extensions import cursor
from psycopg2.extensions import connection
from typing import List, Dict, Optional, Tuple
import traveller.equipment as eq

from referee.command_parser import CommandParser
from traveller.characteristic import Characteristic as Ch, Characteristic
from travellermap import api
import traveller.queries as q


def calculate_age_damage(stats: Tuple, age) -> (Tuple, int):
    roll = max(random.randint(1, 6) + random.randint(1, 6) - ((age - 18) // 4), -6)
    dmg: Dict[Ch, int] = dict.fromkeys(Ch, 0)

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


def modify(cur: cursor, value: int, char_id: int, add: bool, stat: str):
    if add:
        cur.execute(f'UPDATE characters SET {stat} = {stat} {"+" if value > 0 else ""}%s WHERE id = %s;', (value, char_id))
    else:
        cur.execute(f'UPDATE characters SET {stat} = %s WHERE id = %s;', (value, char_id))


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
                    return True, q.info_world(cur, adv_id)
                elif info == 'map':
                    return True, q.info_map(cur, adv_id)
                elif info == 'adventure':
                    return True, q.info_adventure(cur, adv_id)
                else:
                    return True, q.info_character(cur, adv_id, info)

    def set(self, name: str, cmd: List[Optional[str]], value: str, referee_id: int) -> (bool, str):
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
                cmd = [s.upper() for s in cmd]
                if len(cmd) < 2:
                    cmd.extend([''] * (2 - len(cmd)))
                add = False
                if value[0] == '+' or value[0] == '-':
                    add = True
                if cmd[0] == 'STANCE':
                    stance = ['PRONE', 'CROUCHED', 'STANDING']
                    value = stance.index(value.upper()) if value.upper() in stance else value
                    if value not in range(3):
                        return False, 'Cannot set stance'
                    cur.execute('UPDATE characters SET stance = %s WHERE id = %s', (value, char_id))
                    return True, 'Updated stance with success'
                try:
                    value = int(value)
                except ValueError:
                    return False, 'Value is not valid'
                if cmd[0] == 'RADS' or cmd[0] == 'RADIATIONS':
                    modify(cur, value, char_id, add, 'rads')
                    return True, 'Updated radiations with success'
                if cmd[0] == 'STAT' or cmd[0] == 'MOD':
                    try:
                        char = Characteristic[cmd[1]]
                    except KeyError:
                        return False, 'No such characteristic'
                    stat = char.value.lower() if cmd[0] == 'STAT' else char.name.lower() + '_mod'
                    modify(cur, value, char_id, add, stat)
                    return True, 'Updated characteristic with success'
                if cmd[0] == 'STATUS':
                    if cmd[1] in ['WOUNDED', 'FATIGUED']:
                        cur.execute(f'UPDATE characters SET {cmd[1].lower()} = %s WHERE id = %s;',
                                    (value == 1, char_id))
                        return True, 'Updated status with success'
                    return False, 'No such status exists'
                if cmd[0] == 'CR' or cmd[0] == 'CREDITS':
                    modify(cur, value, char_id, add, 'credits')
                    return True, 'Updated credits with success'
                if cmd[0] == 'INV' or cmd[0] == 'INVENTORY' or cmd[0] == 'EQUIPMENT':
                    if cmd[1] == 'RM' or cmd[1] == 'REMOVE':
                        if value <= 0:
                            return False, 'Insert positive number'
                        # From now on it will be Eqtype:Eqname:EventualLevel and it will be case-insensitive
                        for i in range(2, len(cmd)):
                            command = cmd[i]
                            is_item, e = q.is_item(command)
                            if not is_item:
                                return False, 'No such item exists'
                            q.remove_item(cur, value, char_id, e)
                        return True, 'Item removed with success'
                    if cmd[1] == 'ADD':
                        if value <= 0:
                            return False, 'Insert positive number'
                        for i in range(2, len(cmd)):
                            command = cmd[i]
                            found, e = q.is_item(command)
                            if not found:
                                return False, 'No such item exists'
                            cur.execute('SELECT amount FROM inventories WHERE equipment_id = %s and character_id = %s;', (e, char_id))
                            amount = cur.fetchone()
                            if amount:
                                cur.execute('UPDATE inventories '
                                            'SET amount = %s '
                                            'WHERE character_id = %s AND equipment_id = %s',
                                            (amount[0] + value, char_id, e))
                            else:
                                cur.execute('INSERT INTO inventories(character_id, equipment_id, amount, damage) '
                                            'VALUES(%s, %s, %s, %s);', (char_id, e, value, 0))
                        return True, 'Item added with success'
                return False, 'Invalid command format'

    def shop(self, cmd: List[str], referee_id: int) -> (bool, str):
        with self.db:
            with self.db.cursor() as cur:
                cur.execute('SELECT active_adventure FROM users WHERE id = %s;', (referee_id,))
                adv_id = cur.fetchone()[0]
                if cmd[-1].upper() == 'CLOSE':
                    cur.execute('DELETE FROM shop WHERE adventure_id = %s;', (adv_id,))
                    return True, 'Shop closed successfully'
                for c in cmd:  # Check to see if existing shop?
                    for e in eq.equipments:
                        if q.is_coherent(c, e):
                            cur.execute(
                                'INSERT INTO shop(adventure_id, equipment_id) VALUES(%s,%s) ON CONFLICT DO NOTHING;',
                                (adv_id, e))
                    return True, 'Shop opened successfully'

    def rest(self, cmd: str, referee_id: int) -> (bool, str):
        with self.db:
            with self.db.cursor() as cur:
                cur.execute('SELECT active_adventure FROM users WHERE id = %s;', (referee_id,))
                adv_id = cur.fetchone()[0]
                if cmd.upper() == 'SHORT':
                    cur.execute('UPDATE characters SET fatigued = FALSE WHERE adventure_id = %s AND alive = TRUE;',
                                (adv_id,))
                    return True, 'The party rested shorty'
                if cmd.upper() == 'LONG':
                    cur.execute('UPDATE characters SET fatigued = FALSE WHERE adventure_id = %s AND alive = TRUE;',
                                (adv_id,))
                    cur.execute('UPDATE characters SET str_mod = 0, dex_mod = 0, end_mod = 0, '
                                'int_mod = 0, edu_mod = 0, soc_mod = 0')
                    return True, 'The party rested for a long time'
            return False, 'Insert either "short" or "long"'

    def combat(self, combat: str, end: str, referee_id: int) -> (bool, str):
        with self.db:
            with self.db.cursor() as cur:
                cur.execute('SELECT active_adventure FROM users WHERE id = %s;', (referee_id,))
                adv_id = cur.fetchone()[0]
            if end:
                cur.execute('UPDATE adventures SET scene_id = NULL WHERE id = %s;', (adv_id,))
                return True, 'Scene set with success'
            else:
                try:
                    cur.execute('UPDATE adventures SET scene_id = %s WHERE id = %s;',
                                (combat, adv_id))
                except IntegrityError:
                    return False, 'No scene has this name'
                return True, 'Scene set with success'

    def travel(self, name: str, referee_id: int) -> (bool, str):
        with self.db:
            with self.db.cursor() as cur:
                cur.execute('SELECT active_adventure FROM users WHERE id = %s;', (referee_id,))
                adv_id = cur.fetchone()[0]
                with open('data/map.json') as d:
                    data = json.load(d)
                    for sector in data:
                        for world in data[sector]:
                            if world[0] == name:
                                cur.execute('UPDATE adventures SET planet = %s WHERE id = %s;', (name, adv_id))
                                return True, 'The adventurers traveled successfully'
                    else:
                        return False, 'No world with this name'

    def age(self, drug_users: List[str], drug_droppers: List[str], referee_id: int) -> (bool, str):
        try:
            with self.db:
                with self.db.cursor() as cur:
                    cur.execute('SELECT active_adventure FROM users WHERE id = %s;', (referee_id,))
                    adv_id = cur.fetchone()[0]
                    cur.execute('SELECT char_name FROM characters WHERE adventure_id = %s AND alive = TRUE', (adv_id,))
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
        except psycopg2.Error:
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
            pass  # TODO death
