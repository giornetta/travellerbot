from random import Random
from typing import Dict

from psycopg2.extensions import  connection

from traveller.character import Character
from traveller.common import Characteristics


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
            chars[c.name] = Random().randint(1, 6)

        return chars

    def alive_character_exists(self, user_id: int, adventure_id: str) -> bool:
        with self.db:
            with self.db.cursor() as cur:
                cur.execute('SELECT id FROM characters WHERE user_id = %s AND adventure_id = %s AND alive = TRUE',
                            (user_id, adventure_id))
                res = cur.fetchall()
                return len(res) == 1

    def sector(self, adventure_id) -> str:
        with self.db:
            with self.db.cursor() as cur:
                cur.execute('SELECT sector FROM adventures WHERE id = %s', (adventure_id, ))
                return cur.fetchone()[0]
