from enum import Enum, auto


class ConversationState(Enum):
    ADVENTURE_SETUP = auto()
    AFTER_SETUP = auto()
    CHARACTER_CREATION = auto()
    REFEREE_IDLE = auto()
    PLAYER_IDLE = auto()
    SCENE_CREATION = auto()
