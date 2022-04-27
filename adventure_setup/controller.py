import curses.ascii
import string
import random
from typing import Optional

import psycopg2
import psycopg2.errors
from psycopg2.extensions import connection


class SetupController:
    db: connection

    def __init__(self, db: connection):
        self.db = db

    def join_adventure(self, user_id: int, code: str) -> Optional[str]:
        title: Optional[str] = None
        with self.db:
            with self.db.cursor() as cur:
                try:
                    cur.execute('INSERT INTO users(id, active_adventure) VALUES(%s, %s)'
                                'ON CONFLICT(id) DO UPDATE SET active_adventure = %s;', (user_id, code, code))
                    cur.execute('SELECT title FROM adventures WHERE id = %s;', (code, ))
                    title = cur.fetchone()[0]
                except (psycopg2.errors.ForeignKeyViolation, psycopg2.errors.InFailedSqlTransaction) as e:
                    self.db.rollback()

        return title

    def create_adventure(self, referee: int, adventure_name: str, sector: str, world: str, terms: int, survival_kills: bool) -> Optional[str]:
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=6)).upper()  # TODO loop until it's unique

        with self.db:
            with self.db.cursor() as cur:
                cur.execute('INSERT INTO users(id) VALUES(%s) ON CONFLICT DO NOTHING;', (referee, ))
                cur.execute('INSERT INTO adventures VALUES(%s, %s, %s, %s, %s, %s, %s);',
                            (code, adventure_name, sector, world, terms, survival_kills, referee))
                cur.execute('UPDATE users SET active_adventure = %s WHERE id = %s;', (code, referee))

        return code
