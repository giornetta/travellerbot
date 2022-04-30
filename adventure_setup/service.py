import string
import random
from typing import Optional, Tuple

import psycopg2
import psycopg2.errors
from psycopg2.extensions import connection

from character_creation.service import CharacterCreator


class SetupController:
    db: connection
    character_creator: CharacterCreator

    def __init__(self, db: connection, character_creator: CharacterCreator):
        self.db = db

    def join_adventure(self, user_id: int, code: str) -> Optional[Tuple[str, bool]]:
        res: Optional[Tuple[str, bool]] = None
        with self.db:
            with self.db.cursor() as cur:
                try:
                    cur.execute('INSERT INTO users(id, active_adventure) VALUES(%s, %s)'
                                'ON CONFLICT(id) DO UPDATE SET active_adventure = %s;', (user_id, code, code))
                    cur.execute('SELECT title, referee_id FROM adventures WHERE id = %s;', (code, ))
                    title, referee_id = cur.fetchone()
                    res = title, referee_id == user_id
                except (psycopg2.errors.ForeignKeyViolation, psycopg2.errors.InFailedSqlTransaction) as e:
                    self.db.rollback()

        return res

    def create_adventure(self, referee: int, adventure_name: str, sector: str, world: str, terms: int, survival_kills: bool) -> Optional[str]:
        adventure_id = ''.join(random.choices(string.ascii_letters + string.digits, k=6)).upper()
        created = False

        while not created:
            with self.db:
                with self.db.cursor() as cur:
                    try:
                        cur.execute('INSERT INTO users(id) VALUES(%s) ON CONFLICT DO NOTHING;', (referee, ))
                        cur.execute('INSERT INTO adventures VALUES(%s, %s, %s, %s, %s, %s, %s);',
                                    (adventure_id, adventure_name, sector, world, terms, survival_kills, referee))
                        cur.execute('UPDATE users SET active_adventure = %s WHERE id = %s;', (adventure_id, referee))
                        created = True
                    except psycopg2.errors.UniqueViolation:
                        adventure_id = ''.join(random.choices(string.ascii_letters + string.digits, k=6)).upper()

        return adventure_id
