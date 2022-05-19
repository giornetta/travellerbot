from typing import List, Tuple

from psycopg2.extensions import cursor
from psycopg2.extensions import connection
import traveller.equipment as eq
import traveller.queries as q


class Shop:
    db: connection

    def __init__(self, db: connection):
        self.db = db

    def categories_from_shop(self, user_id: int) -> List[str]:
        with self.db:
            with self.db.cursor() as cur:
                cur.execute('SELECT just_created FROM characters WHERE user_id = %s AND alive = TRUE;', (user_id,))
                just_created = cur.fetchone()
                if just_created:
                    keys = list(eq.categories.keys())
                    for i in range(len(keys)):
                        keys[i] = keys[i].title()
                    return keys
                cur.execute('SELECT active_adventure FROM users WHERE id = %s;', (user_id,))
                adv_id = cur.fetchone()[0]
                categories = q.categories_from_shop(cur, adv_id, user_id)
                keys = []
                for c in categories:
                    keys.append(f'{c[0]}:{c[1]}')
                return keys

    def add(self, user_id: int, e: int) -> Tuple[bool, int]:
        with self.db:
            with self.db.cursor() as cur:
                cur.execute('SELECT active_adventure FROM users WHERE id = %s', (user_id,))
                adv_id = cur.fetchone()[0]
                cur.execute('SELECT id FROM characters WHERE adventure_id = %s AND user_id = %s AND alive = TRUE',
                            (adv_id, user_id))
                char_id = cur.fetchone()[0]
                print(e)
                bought, credits_remaining = q.enough_money(cur, char_id, e)
                if bought:
                    q.add_item(cur, char_id, 1, e)
                return bought, credits_remaining

    def set_created(self, user_id: int):
        with self.db:
            with self.db.cursor() as cur:
                cur.execute('SELECT active_adventure FROM users WHERE id = %s;', (user_id,))
                adv_id = cur.fetchone()[0]
                cur.execute('UPDATE characters SET just_created = FALSE '
                            'WHERE user_id = %s AND alive = TRUE and adventure_id = %s;',
                            (user_id, adv_id))
