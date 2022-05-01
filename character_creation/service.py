from typing import Dict

from psycopg2.extensions import  connection

from traveller.character import Character


class CharacterCreator:

    # This stores the characters being created
    # before they're actually saved into the db.
    characters: Dict[int, Character]  # TODO Could also use CallbackContext?

    db: connection

    def __init__(self, db: connection):
        self.db = db

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