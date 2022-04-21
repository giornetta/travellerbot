import string
import random
from typing import Dict


class SetupController:

    adventures: Dict[str, str]

    def __init__(self):
        self.adventures = {}

    def join_adventure(self, user_id: int, code: str) -> str:
        return self.adventures[code]

    def create_adventure(self, referee: int, adventure_name: str, sector: str, world: str, terms: int, survival_kills: bool) -> str:
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=6)).upper()
        self.adventures[code] = adventure_name
        return code
