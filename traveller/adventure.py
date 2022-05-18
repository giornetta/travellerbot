from __future__ import annotations

from typing import Tuple


class Adventure:
    id: str
    title: str
    sector: str
    world: str  # TODO for now the name is enough
    terms: int
    survival_kills: bool
    referee_id: int

    @classmethod
    def from_db(cls, t: Tuple[str, str, str, str, int, bool, int]) -> Adventure:
        a = Adventure()
        a.id = t[0]
        a.title = t[1]
        a.sector = t[2]
        a.world = t[3]
        a.terms = t[4]
        a.survival_kills = t[5]
        a.referee_id = t[6]
        return a
