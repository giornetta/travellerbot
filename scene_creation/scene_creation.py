from typing import List
from enum import Enum, auto

from telegram import Update
from telegram.ext import ConversationHandler, MessageHandler, Filters, CallbackContext

from conversations.state import ConversationState
from scene_creation import kb

import traveller.equipment as eq


class State(Enum):
    NPC = auto(),
    END = auto(),
    CH_GEN = auto(),
    RANK = auto(),
    ARMOR = auto(),
    WEAPON = auto(),
    NAME = auto(),
    ALLY = auto(),
    NEXT = auto(),
    NPC_END = auto()


class SceneCreationConversation:
    def __init__(self):
        pass

    def handlers(self) -> List[ConversationHandler]:
        return [
            ConversationHandler(
                entry_points=[MessageHandler(Filters.regex(r'^/scene +new +[\w]+$'), self._ask_next_npc)],
                states={
                    State.NPC: [MessageHandler(Filters.text('Add'), self._ask_characteristics_generation),
                                MessageHandler(Filters.text('End'), self._handle_end)
                                ],
                    State.CH_GEN: [MessageHandler(Filters.text('(Manually|Let me choose)'), self._handle_manual_gen),
                                   MessageHandler(Filters.text('(Random|Generate Again)'), self._handle_random_gen),
                                   MessageHandler(Filters.text('Accept'), self._ask_career)
                                   ],
                    State.RANK: [MessageHandler(Filters.text, self._ask_rank)],
                    State.ARMOR: [MessageHandler(Filters.text, self._ask_armor)],
                    State.WEAPON: [MessageHandler(Filters.text, self._ask_weapon)],
                    State.NAME: [MessageHandler(Filters.text, self._ask_name)],
                    State.ALLY: [MessageHandler(Filters.text, self._ask_ally)],
                    State.NPC_END: [MessageHandler(Filters.text, self._handle_npc_registration)],
                    State.NEXT: [MessageHandler(Filters.text, self._ask_next_npc)],
                },
                fallbacks=[],
                map_to_parent={
                    State.END: ConversationState.REFEREE_IDLE
                },
                name='create_scene',
                persistent=True
            )
        ]

    def _ask_next_npc(self, update: Update, context: CallbackContext) -> State:
        kb.next_npc.reply_text(update)
        return State.NPC

    def _handle_end(self, update: Update, context: CallbackContext) -> State:
        return State.END

    def _ask_characteristics_generation(self, update: Update, context: CallbackContext) -> State:
        kb.ch_gen.reply_text(update)
        return State.CH_GEN

    def _handle_manual_gen(self, update: Update, context: CallbackContext) -> State:
        kb.ch_manual_gen.reply_text(update)
        return State.CH_GEN

    def _handle_random_gen(self, update: Update, context: CallbackContext) -> State:
        kb.ch_random_gen.reply_text(update, params=(1, 2, 3, 4, 5, 6))
        return State.CH_GEN

    def _ask_career(self, update: Update, context: CallbackContext) -> State:
        kb.career.reply_text(update, params=(1, 2, 3, 4, 5, 6))
        return State.RANK

    def _ask_rank(self, update: Update, context: CallbackContext) -> State:
        kb.rank.reply_text(update)
        return State.ARMOR

    def _ask_armor(self, update: Update, context: CallbackContext) -> State:
        keys = []
        for _id in eq.equipments:
            if isinstance(eq.equipments[_id], eq.Armor):
                keys.append([eq.equipments[_id].name])
                pass

        kb.armor.reply_text(update, keys=keys)
        return State.WEAPON

    def _ask_weapon(self, update: Update, context: CallbackContext) -> State:
        keys = []
        for _id in eq.equipments:
            if isinstance(eq.equipments[_id], eq.Weapon):
                keys.append([eq.equipments[_id].name])
                pass

        kb.weapon.reply_text(update, keys=keys)
        return State.NAME

    def _ask_name(self, update: Update, context: CallbackContext) -> State:
        kb.name.reply_text(update)
        return State.ALLY

    def _ask_ally(self, update: Update, context: CallbackContext) -> State:
        kb.ally.reply_text(update)
        return State.NPC_END

    def _handle_npc_registration(self, update: Update, context: CallbackContext) -> State:
        return State.NEXT
