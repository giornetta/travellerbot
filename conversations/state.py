from enum import Enum, auto


class ConversationState(Enum):
    ADVENTURE_SETUP = auto()
    CHARACTER_CREATION = auto()
    IDLE = auto()
