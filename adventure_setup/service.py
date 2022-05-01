import string
import random
from typing import Optional, Tuple

import psycopg2
import psycopg2.errors
from psycopg2.extensions import connection

from traveller.adventure import Adventure


class AdventureSetupService:
    db: connection

    def __init__(self, db: connection):
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

    def create_adventure(self, referee_id: int, adv: Adventure) -> Optional[str]:
        adventure_id = ''.join(random.choices(string.ascii_letters + string.digits, k=6)).upper()
        created = False

        if adv.terms < 0:
            adv.terms = -1

        while not created:
            with self.db:
                with self.db.cursor() as cur:
                    try:
                        cur.execute('INSERT INTO users(id) VALUES(%s) ON CONFLICT DO NOTHING;', (referee_id, ))
                        cur.execute('INSERT INTO adventures VALUES(%s, %s, %s, %s, %s, %s, %s);',
                                    (adventure_id, adv.title, adv.sector, adv.world, adv.terms, adv.survival_kills, referee_id))
                        cur.execute('UPDATE users SET active_adventure = %s WHERE id = %s;', (adventure_id, referee_id))
                        created = True
                    except psycopg2.errors.UniqueViolation:
                        adventure_id = ''.join(random.choices(string.ascii_letters + string.digits, k=6)).upper()

        return adventure_id
