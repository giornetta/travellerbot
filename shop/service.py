from typing import List, Optional, Tuple

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
                cur.execute('SELECT active_adventure FROM users WHERE id = %s', (user_id,))
                adv_id = cur.fetchone()[0]
                cur.execute('SELECT just_created FROM characters WHERE user_id = %s AND adventure_id = %s AND alive = TRUE;', (user_id, adv_id))
                just_created = cur.fetchone()[0]

                keys: List[str] = []
                if just_created:
                    for k in eq.categories.keys():
                        keys.append(k.title().replace('_', ' '))
                    return keys

                keys = q.categories_from_shop(cur, adv_id, user_id)

                return keys

    def tl(self, user_id: int) -> Optional[int]:
        with self.db:
            with self.db.cursor() as cur:
                cur.execute('SELECT active_adventure FROM users WHERE id = %s', (user_id,))
                adv_id = cur.fetchone()[0]
                cur.execute('SELECT tl FROM shop WHERE adventure_id = %s', (adv_id,))

                res = cur.fetchone()
                if res:
                    return res[0]

                return None

    def character_credits(self, user_id: int) -> int:
        with self.db:
            with self.db.cursor() as cur:
                cur.execute('SELECT active_adventure FROM users WHERE id = %s', (user_id,))
                adv_id = cur.fetchone()[0]
                cur.execute('SELECT credits FROM characters WHERE adventure_id = %s AND alive = TRUE AND user_id = %s', (adv_id, user_id))
                return cur.fetchone()[0]

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
