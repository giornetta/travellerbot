import string
import random
from typing import List, Optional

import psycopg2
import psycopg2.errors
from psycopg2.extensions import connection

from traveller.adventure import Adventure


class AdventureSetupService:
    db: connection

    def __init__(self, db: connection):
        self.db = db

    def adventures(self, user_id) -> List[str]:
        adventures: List[str] = []
        with self.db:
            with self.db.cursor() as cur:
                cur.execute('SELECT title, id FROM adventures WHERE referee_id = %s', (user_id, ))
                for adv in cur.fetchall():
                    adventures.append(f'{adv[1]}: {adv[0]}')

                cur.execute('SELECT a.title, a.id FROM adventures a JOIN characters c on a.id = c.adventure_id WHERE c.user_id = %s', (user_id, ))
                for adv in cur.fetchall():
                    adventures.append(f'{adv[1]}: {adv[0]}')

                return adventures

    def join_adventure(self, user_id: int, code: str) -> Optional[Adventure]:
        adv: Optional[Adventure] = None
        with self.db:
            with self.db.cursor() as cur:
                try:
                    cur.execute('INSERT INTO users(id, active_adventure) VALUES(%s, %s)'
                                'ON CONFLICT(id) DO UPDATE SET active_adventure = %s;', (user_id, code, code))
                    cur.execute('SELECT id, title, sector, planet, max_terms, survival_fail_kills, referee_id FROM adventures WHERE id = %s;', (code, ))
                    adv_id, title, sector, world, terms, survival_kills, referee_id = cur.fetchone()
                    adv = Adventure.from_db((adv_id, title, sector, world, terms, survival_kills, referee_id))
                except (psycopg2.errors.ForeignKeyViolation, psycopg2.errors.InFailedSqlTransaction):
                    self.db.rollback()

        return adv

    def create_adventure(self, referee_id: int, adv: Adventure) -> Optional[str]:
        adventure_id = ''.join(random.choices(string.ascii_letters, k=6)).upper()
        created = False

        if adv.terms < 0:
            adv.terms = -1

        while not created:
            with self.db:
                with self.db.cursor() as cur:
                    try:
                        cur.execute('INSERT INTO users(id) VALUES(%s) ON CONFLICT DO NOTHING;', (referee_id, ))
                        cur.execute('INSERT INTO adventures(id, title, sector, planet, max_terms, survival_fail_kills, referee_id) VALUES(%s, %s, %s, %s, %s, %s, %s);',
                                    (adventure_id, adv.title, adv.sector, adv.world,
                                     adv.terms, adv.survival_kills, referee_id))
                        cur.execute('UPDATE users SET active_adventure = %s WHERE id = %s;', (adventure_id, referee_id))
                        created = True
                    except psycopg2.errors.UniqueViolation:
                        adventure_id = ''.join(random.choices(string.ascii_letters, k=6)).upper()

        return adventure_id
