from typing import List, Tuple

from psycopg2.extensions import cursor
from psycopg2.extensions import connection
import traveller.equipment as eq
import traveller.queries as q


class Shop:
    db: connection

    def __init__(self, db: connection):
        self.db = db

    def items_from_shop(self, user_id: int) -> List[int]:
        with self.db:
            with self.db.cursor() as cur:
                cur.execute('SELECT just_created FROM characters WHERE user_id = %s AND alive = TRUE;')
                just_created = cur.fetchone()[0]
                if just_created:
                    return list(range(len(eq.equipments)))
                cur.execute('SELECT active_adventure FROM users WHERE id = %s;', (user_id,))
                adv_id = cur.fetchone()[0]
                return q.items_from_shop(cur, adv_id, user_id)

    def set_created(self, user_id: int):
        with self.db:
            with self.db.cursor() as cur:
                cur.execute('SELECT active_adventure FROM users WHERE id = %s;', (user_id,))
                adv_id = cur.fetchone()[0]
                cur.execute('UPDATE SET just_created = FALSE FROM characters WHERE user_id = %s '
                            'AND alive = TRUE and adventure_id = %s',
                            (user_id, adv_id))

