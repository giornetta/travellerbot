from random import Random
from typing import Dict, List

from psycopg2.extensions import  connection

from traveller import world
from traveller.character import Character
from traveller.common import Characteristics
from travellermap import api


class CharacterCreator:

    # This stores the characters being created
    # before they're actually saved into the db.
    characters: Dict[int, Character]  # TODO Could also use context?

    db: connection

    def __init__(self, db: connection):
        self.db = db

    @staticmethod
    def roll() -> Dict[str, int]:
        chars: Dict[str, int] = {}
        for c in Characteristics:
            chars[c.name] = Random().randint(1, 6) + Random().randint(1, 6)

        return chars

    @staticmethod
    def modifiers(chars: Dict[str, int]) -> Dict[str, int]:
        mods: Dict[str, int] = {}
        for c in chars.keys():
            mods[c] = chars[c] // 3 - 2

        return mods

    def homeworld_skills(self, sector: str, world_name: str) -> List[str]:
        worlds = api.data[sector]

        uwp: str = ""
        for w in worlds:
            if w[0] == world_name:
                uwp: str = w[1]
                break

        v = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
             '8': 8, '9': 9, 'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15}

        return world.homeworld_skills(v[uwp[6]], world.trade_codes(uwp))

    def alive_character_exists(self, user_id: int, adventure_id: str) -> bool:
        with self.db:
            with self.db.cursor() as cur:
                cur.execute('SELECT id FROM characters WHERE user_id = %s AND adventure_id = %s AND alive = TRUE',
                            (user_id, adventure_id))
                res = cur.fetchall()
                return len(res) == 1

    def sector(self, adventure_id: str) -> str:
        with self.db:
            with self.db.cursor() as cur:
                cur.execute('SELECT sector FROM adventures WHERE id = %s', (adventure_id, ))
                return cur.fetchone()[0]

    def world_selection(self, sector: str,
                        min_starport: str = 'X', max_starport: str = 'A',
                        min_size: int = 0, max_size: int = 10,
                        min_atm: int = 0, max_atm: int = 15,
                        min_hydro: int = 0, max_hydro: int = 10,
                        min_pop: int = 0, max_pop: int = 10,
                        min_gov: int = 0, max_gov: int = 15,
                        min_law: int = 0, max_law: int = 10,
                        min_tech: int = 0, max_tech: int = 15) -> List[str]:
        worlds = []
        for w in api.data[sector]:
            sv = {'X': 0, 'E': 1, 'D': 2, 'C': 3, 'B': 4, 'A': 5}

            if sv[w[1][0]] < sv[min_starport] or sv[w[1][0]] > sv[max_starport]:
                continue

            v = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
                 '8': 8, '9': 9, 'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15}

            if v[w[1][1]] < min_size or v[w[1][1]] > max_size or \
               v[w[1][2]] < min_atm or v[w[1][2]] > max_atm or \
               v[w[1][3]] < min_hydro or v[w[1][3]] > max_hydro or \
               v[w[1][4]] < min_pop or v[w[1][4]] > max_pop or \
               v[w[1][5]] < min_gov or v[w[1][5]] > max_gov or \
               v[w[1][6]] < min_law or v[w[1][6]] > max_law or \
               v[w[1][8]] < min_tech or v[w[1][8]] > max_tech:
                continue

            worlds.append(w[0])

        print(worlds)

        return worlds


