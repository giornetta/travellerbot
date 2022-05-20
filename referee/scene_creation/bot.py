from typing import List
from enum import Enum, auto

from telegram import Update
from telegram.ext import ConversationHandler, MessageHandler, Filters, CallbackContext

from referee.scene_creation.service import SceneCreationService
from referee.state import RefereeState
from referee.scene_creation import kb

from cache.userdata import user_data

import traveller.equipment as eq
import traveller.career as career
from traveller.characteristic import Characteristic
from traveller.scene import Scene


class State(Enum):
    SCENE_NAME = auto()
    NPC = auto()
    END = auto()
    CH_GEN = auto()
    CAREER = auto()
    RANK = auto()
    ARMOR = auto()
    WEAPON = auto()
    NAME = auto()
    ALLY = auto()
    NEXT = auto()
    NPC_END = auto()


class SceneCreationConversation:

    scene_creator: SceneCreationService

    def __init__(self, scene_creator: SceneCreationService):
        self.scene_creator = scene_creator

    def handlers(self) -> List[ConversationHandler]:
        return [
            ConversationHandler(
                entry_points=[MessageHandler(Filters.text, self._handle_scene_name)],
                states={
                    State.SCENE_NAME: [MessageHandler(Filters.regex(r'^[\dA-Za-z]+$'), self._handle_scene_name)],
                    State.NPC: [MessageHandler(Filters.text('Add'), self._ask_characteristics_generation),
                                MessageHandler(Filters.text('End'), self._handle_end)
                                ],
                    State.CH_GEN: [MessageHandler(Filters.regex('^(Manually|Let me choose)$'), self._handle_manual_gen),
                                   MessageHandler(Filters.regex('^(Random|Generate Again)$'), self._handle_random_gen),
                                   MessageHandler(Filters.regex(r'^(Accept|(\d+ ){5}\d+)$'), self._ask_career)
                                   ],
                    State.CAREER: [MessageHandler(Filters.text, self._handle_career)],
                    State.RANK: [MessageHandler(Filters.regex(r'^[0-6]$'), self._handle_rank)],
                    State.ARMOR: [MessageHandler(Filters.text, self._handle_armor)],
                    State.WEAPON: [MessageHandler(Filters.text, self._handle_weapon)],
                    State.NAME: [MessageHandler(Filters.regex('^[A-Za-z]+$'), self._handle_name)],
                    State.ALLY: [MessageHandler(Filters.regex('^(Ally|Enemy)$'), self._handle_ally)]
                },
                fallbacks=[],
                map_to_parent={
                    State.END: RefereeState.COMMANDS
                },
                name='create_scene',
                persistent=True
            )
        ]

    def _handle_scene_name(self, update: Update, context: CallbackContext) -> State:
        user = user_data[update.message.from_user.id]

        if len(update.message.text) > 32:
            kb.name_too_long.reply_text(update)
            return State.SCENE_NAME

        if self.scene_creator.scene_already_exists(update.message.text, user.adventure.id):
            kb.scene_already_exists.reply_text(update)
            return State.SCENE_NAME

        user.scene = Scene(update.message.text)

        kb.next_npc.reply_text(update)
        return State.NPC

    def _handle_end(self, update: Update, context: CallbackContext) -> State:
        user = user_data[update.message.from_user.id]
        self.scene_creator.create_scene(user.scene, user.adventure.id)

        kb.end.reply_text(update)
        return State.END

    def _ask_characteristics_generation(self, update: Update, context: CallbackContext) -> State:
        user = user_data[update.message.from_user.id]
        user.scene.add_npc()

        kb.ch_gen.reply_text(update)
        return State.CH_GEN

    def _handle_manual_gen(self, update: Update, context: CallbackContext) -> State:
        kb.ch_manual_gen.reply_text(update)
        return State.CH_GEN

    def _handle_random_gen(self, update: Update, context: CallbackContext) -> State:
        user = user_data[update.message.from_user.id]

        user.scene.npc.roll_characteristics()
        kb.ch_random_gen.reply_text(update, params=user.scene.npc.stats_tuple)
        return State.CH_GEN

    def _ask_career(self, update: Update, context: CallbackContext) -> State:
        user = user_data[update.message.from_user.id]

        if update.message.text != 'Accept':
            v = update.message.text.split(' ')
            for val in v:
                if not val.isdigit() or val == '0':
                    kb.invalid_stats.reply_text(update)
                    return State.CH_GEN

            stats = {
                Characteristic.STR: int(v[0]),
                Characteristic.DEX: int(v[1]),
                Characteristic.END: int(v[2]),
                Characteristic.INT: int(v[3]),
                Characteristic.EDU: int(v[4]),
                Characteristic.SOC: int(v[5])
            }
            user.scene.npc.stats = stats

        kb.career.reply_text(update, keys=[[c] for c in career.careers]) # TODO single_keys
        return State.CAREER

    def _handle_career(self, update: Update, context: CallbackContext) -> State:
        user = user_data[update.message.from_user.id]

        c = update.message.text
        if c not in career.careers:
            return State.CAREER

        user.scene.npc.career = c

        kb.rank.reply_text(update)
        return State.RANK

    def _handle_rank(self, update: Update, context: CallbackContext) -> State:
        user = user_data[update.message.from_user.id]

        user.scene.npc.rank = int(update.message.text)

        keys = []
        for _id in eq.equipments:
            if isinstance(eq.equipments[_id], eq.Armor):
                keys.append([eq.equipments[_id].name])

        kb.armor.reply_text(update, keys=keys)
        return State.ARMOR

    def _handle_armor(self, update: Update, context: CallbackContext) -> State:
        user = user_data[update.message.from_user.id]

        armor_id = eq.get_equipment_by_name(update.message.text).id
        if not armor_id:
            return State.ARMOR

        user.scene.npc.armor = armor_id

        keys = []
        for _id in eq.equipments:
            if isinstance(eq.equipments[_id], eq.Weapon):
                keys.append([eq.equipments[_id].name])

        kb.weapon.reply_text(update, keys=keys)
        return State.WEAPON

    def _handle_weapon(self, update: Update, context: CallbackContext) -> State:
        user = user_data[update.message.from_user.id]

        weapon_id = eq.get_equipment_by_name(update.message.text).id
        if not weapon_id:
            return State.WEAPON

        user.scene.npc.weapon = weapon_id

        kb.name.reply_text(update)
        return State.NAME

    def _handle_name(self, update: Update, context: CallbackContext) -> State:
        user = user_data[update.message.from_user.id]

        if len(update.message.text) > 32:
            kb.name_too_long.reply_text(update)
            return State.NAME

        user.scene.npc.name = update.message.text

        kb.ally.reply_text(update)
        return State.ALLY

    def _handle_ally(self, update: Update, context: CallbackContext) -> State:
        user = user_data[update.message.from_user.id]

        user.scene.npc.ally = update.message.text == 'Ally'

        kb.next_npc.reply_text(update)
        return State.NPC
