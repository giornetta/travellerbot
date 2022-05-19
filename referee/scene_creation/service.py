import psycopg2
from psycopg2.extensions import connection

from traveller.characteristic import Characteristic
from traveller.scene import Scene


class SceneCreationService:

    conn: connection

    def __init__(self, conn: connection):
        self.conn = conn

    def scene_already_exists(self, name: str, adventure_id: str) -> bool:
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute('SELECT * FROM scenes WHERE scene_name = %s AND adventure_id = %s', (name, adventure_id))
                return cur.fetchone() is not None

    def create_scene(self, scene: Scene, adventure_id: str) -> bool:
        with self.conn:
            with self.conn.cursor() as cur:
                try:
                    cur.execute('INSERT INTO scenes(scene_name, adventure_id) VALUES(%s, %s) ON CONFLICT DO NOTHING RETURNING id;', (scene.name, adventure_id))
                    scene_id = cur.fetchone()

                    for npc in scene.npcs:
                        cur.execute('INSERT INTO npcs(npc_name, strength, dexterity, endurance, intelligence, education,'
                                    ' social_standing, career, rank, armor, weapon, ally, scene) '
                                    'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) '
                                    'ON CONFLICT(id) DO NOTHING;',
                                    (npc.name,
                                     npc.stats[Characteristic.STR], npc.stats[Characteristic.DEX], npc.stats[Characteristic.END],
                                     npc.stats[Characteristic.INT], npc.stats[Characteristic.EDU], npc.stats[Characteristic.SOC],
                                     npc.career, npc.rank, npc.armor, npc.weapon, npc.ally, scene_id))

                    return True
                except psycopg2.Error:
                    self.conn.rollback()
                    return False

