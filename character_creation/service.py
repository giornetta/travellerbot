from psycopg2.extensions import connection

from traveller.character import Character
from traveller.characteristic import Characteristic


class CharacterCreator:
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
                cur.execute('SELECT sector FROM adventures WHERE id = %s', (adventure_id,))
                return cur.fetchone()[0]

    def create_character(self, user_id: int, adventure_id: str, c: Character):
        with self.db:
            with self.db.cursor() as cur:
                cur.execute('INSERT INTO characters(user_id, adventure_id, char_name, sex, age, '
                            'strength, dexterity, endurance, intelligence, education, social_standing, credits, society) '
                            'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) '
                            'ON CONFLICT DO NOTHING RETURNING id;', (
                                user_id, adventure_id,
                                c.name, c.sex, c.age,
                                c.stats[Characteristic.STR], c.stats[Characteristic.DEX], c.stats[Characteristic.END],
                                c.stats[Characteristic.INT], c.stats[Characteristic.EDU], c.stats[Characteristic.SOC],
                                c.credits, c.society
                            ))
                char_id = cur.fetchone()[0]
                for eq, qt in c.inventory:
                    cur.execute('INSERT INTO inventories VALUES(%s, %s, %s);', (char_id, eq.id, qt))
                for skill in c.skills:
                    cur.execute('INSERT INTO skill_sets VALUES(%s, %s, %s);', (char_id, skill.name, skill.level))
