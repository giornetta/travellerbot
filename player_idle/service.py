from typing import List, Tuple

from psycopg2.extensions import cursor
from psycopg2.extensions import connection

import traveller.queries as q
from traveller.skill import skills


class PlayerIdle:
    db: connection

    def __init__(self, db: connection):
        self.db = db

    def info_world(self, user_id: int) -> str:
        with self.db:
            with self.db.cursor() as cur:
                adv_id = self.get_adv_id(cur, user_id)
                return q.info_world(cur, adv_id)

    def info_adventure(self, user_id: int) -> str:
        with self.db:
            with self.db.cursor() as cur:
                adv_id = self.get_adv_id(cur, user_id)
                return q.info_adventure(cur, adv_id)

    def info_map(self, user_id: int) -> str:
        with self.db:
            with self.db.cursor() as cur:
                adv_id = self.get_adv_id(cur, user_id)
                return q.info_map(cur, adv_id, )

    def info_myself(self, user_id: int) -> str:
        with self.db:
            with self.db.cursor() as cur:
                adv_id = self.get_adv_id(cur, user_id)
                name = self.get_name(cur, user_id, adv_id)
                return q.info_character(cur, adv_id, name)

    def info_scene(self, user_id: int) -> str:
        with self.db:
            with self.db.cursor() as cur:
                adv_id = self.get_adv_id(cur, user_id)
                cur.execute('SELECT scene_id FROM adventures WHERE id = %s', (adv_id,))
                scene_id = cur.fetchone()[0]
                if not scene_id:
                    return '❌ No active scene'
                cur.execute('SELECT scene_name FROM scenes WHERE id=%s', (scene_id,))
                scene_name = cur.fetchone()[0]
                text = f'<b>Scene name</b>:{scene_name}\n\n'
                text = text + q.info_npcs(cur, scene_id)
                return text

    def get_items(self, user_id: int) -> List[List[str]]:
        with self.db:
            with self.db.cursor() as cur:
                adv_id = self.get_adv_id(cur, user_id)
                return q.get_items(cur, adv_id, user_id)

    def get_adv_id(self, cur: cursor, user_id: int) -> str:
        cur.execute('SELECT active_adventure FROM users WHERE id = %s;', (user_id,))
        return cur.fetchone()[0]

    def get_name(self, cur: cursor, user_id: int, adv_id: str) -> str:
        cur.execute('SELECT char_name FROM characters WHERE user_id=%s AND adventure_id=%s AND alive = TRUE;',
                    (user_id, adv_id))
        return cur.fetchone()[0]

    def is_item(self, item: str) -> Tuple[bool, int]:
        return q.is_item(item)

    def remove_item(self, user_id: int, item_id: int):
        with self.db:
            with self.db.cursor() as cur:
                adv_id = self.get_adv_id(cur, user_id)
                cur.execute('SELECT id FROM characters WHERE user_id=%s AND adventure_id=%s AND alive = TRUE;',
                            (user_id, adv_id))
                char_id = cur.fetchone()[0]
                q.remove_item(cur, 1, char_id, item_id)

    def skill_levels(self, user_id: int) -> List[str]:
        with self.db:
            with self.db.cursor() as cur:
                adv_id = self.get_adv_id(cur, user_id)

                cur.execute('SELECT s.skill_name, s.level '
                            'FROM skill_sets AS s, characters AS c '
                            'WHERE s.character_id = c.id AND c.adventure_id = %s AND c.user_id = %s AND c.alive = TRUE;',
                            (adv_id, user_id))

                skillset: List[str] = []
                tuples = cur.fetchall()
                for name, lvl in tuples:
                    skillset.append(name)

                for name, passive in skills.items():
                    if not passive and name not in skillset:
                        skillset.append(name)

                for i in range(len(tuples)):
                    skillset[i] = f'{tuples[i][0]}-{tuples[i][1]}'

                return skillset



