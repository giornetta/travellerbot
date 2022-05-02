import json
from re import finditer

from psycopg2.extensions import connection
from PIL import Image
import requests
from typing import List


class RefereeCommands:
    db: connection
    referee_id: int

    def __init__(self, db: connection, referee_id: int):
        self.db = db
        self.referee_id = referee_id

    # TODO tuesday we will integrate it in telegram, right now I'm just doing queries

    def info(self, info: str):
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
                    return True
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

    def set(self, name: str, cmd: List[str], value: str):
        with self.db:
            with self.db.cursor() as cur:
                cur.execute('SELECT active_adventure FROM users WHERE id = %s;', (self.referee_id,))
                adv_id = cur.fetchone()[0]
                cur.execute('SELECT id FROM characters WHERE char_name = %s AND adventure_id = %s and alive = TRUE;',
                            (name, adv_id))
                char_id = cur.fetchone()[0]  # TODO exception
            if cmd[0] == 'stat':
                cur.execute('UPDATE characters SET %s = %s WHERE id = %s;', (cmd[1], value, char_id))
                cur.execute('UPDATE characters SET %s = %s WHERE id = %s;',
                            (cmd[1] + '_mod', -2 + (int(value) // 3), char_id))
                return True
            if cmd[0] == 'status':
                cur.execute('UPDATE characters SET %s = %s WHERE id = %s;',
                            (cmd[1], value == 1, char_id))  # Do I need to check the status name?
                return True
            if cmd[0] == 'cr' or 'credits':
                cur.execute('UPDATE characters SET %s = %s WHERE id = %s;', (cmd[1], value, char_id))
                return True
            if cmd[0] == 'inv' or 'inventory' or 'equipment':
                if cmd[1] == 'rm' or 'remove':  # Change name of equipments or parse command?
                    with open('data/equipment.json') as d:
                        data = json.load(d)
                        for i in range(2, len(cmd)):
                            for eq_type in data:
                                for eq in eq_type:
                                    if eq['name'] == cmd[i]:
                                        eq_id = eq['id']
                        cur.execute('DELETE FROM inventories WHERE character_id = %s AND equipment_id = %s;',
                                    (eq_id, char_id))
                    return True
                if cmd[1] == 'add':
                    with open('data/equipment.json') as d:
                        data = json.load(d)
                        for i in range(2, len(cmd) - 1):
                            for eq_type in data:
                                for eq in eq_type:
                                    if eq['name'] == cmd[2]:
                                        eq_id = eq['id']
                        cur.execute('SELECT amount FROM inventories WHERE equipment_id = %s and character_id = %s;',
                                    (eq_id, char_id))
                        amount = cur.fetchone()
                        if amount:
                            cur.execute('UPDATE inventories '
                                        'SET character_id = %s,equipment_id = %s,amount = %s,damage = 0;',
                                        (char_id, eq_id, amount + value))
                        else:
                            cur.execute('INSERT INTO inventories(character_id, equipment_id, amount, damage) '
                                        'VALUES(%s, %s, %s, %s);', (char_id, eq_id, value, 0))

    def shop(self, cmd: List[str]):
        with self.db:
            with self.db.cursor() as cur:
                cur.execute('SELECT active_adventure FROM users WHERE id = %s;', (self.referee_id,))
                adv_id = cur.fetchone()[0]
                if cmd[-1] == 'close':
                    cur.execute('DELETE FROM shop WHERE adventure_id = %s;', (adv_id,))
                    return True
                with open('data/equipment.json') as d:
                    data = json.load(d)
                    for i in range(1, len(cmd)):  # Check to see if existing shop?
                        cur.execute(
                            'INSERT INTO shop(adventure_id, equipment_id) VALUES(%s,%s) ON CONFLICT DO NOTHING;',
                            (adv_id, cmd[i]))
                return True

    def rest(self, cmd: str):
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
                    return True
                    # Discuss how to deal with damage: we have to take account of "maximum health" and "current health"
            return False

    def combat(self, combat: str, end: str):
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

    def travel(self, world: str):
        with self.db:
            with self.db.cursor() as cur:
                cur.execute('SELECT active_adventure FROM users WHERE id = %s;', (self.referee_id,))
                adv_id = cur.fetchone()[0]
                cur.execute('UPDATE adventures SET planet = %s WHERE id = %s;', (world, adv_id))
                return True

    def age(self, drug_user: List[str], char: List[str]):
        with self.db:
            with self.db.cursor() as cur:
                cur.execute('SELECT active_adventure FROM users WHERE id = %s;', (self.referee_id,))
                adv_id = cur.fetchone()[0]
                for name in char:
                    cur.execute('SELECT age FROM characters '
                                'WHERE char_name = %s AND adventure_id = %s AND alive = TRUE;',
                                (name, adv_id))
                    age = cur.fetchone()[0]
                    cur.execute('UPDATE characters SET age = %s '
                                'WHERE char_name = %s AND adventure_id = %s AND alive = TRUE;',
                                (age + 4, name, adv_id))
                    if age > 30:
                        pass  # TODO age damage

    def scene(self, new: str, name: str):
        if new != 'new':
            return False
        with self.db:
            with self.db.cursor() as cur:
                cur.execute('SELECT active_adventure FROM users WHERE id = %s;', (self.referee_id,))
                adv_id = cur.fetchone()[0]
        # discuss about scenes in database

    def exit(self):
        with self.db:
            with self.db.cursor() as cur:
                cur.execute('UPDATE users SET active_adventure = NULL WHERE id = %s', (self.referee_id,))
