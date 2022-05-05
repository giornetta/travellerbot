from random import randint
from typing import List
from enum import Enum, auto
from dataclasses import dataclass
import re

from telegram import Update
from telegram.ext import ConversationHandler, MessageHandler, Filters, CallbackContext

from psycopg2.extensions import connection

from bot.state import ConversationState
from scene_creation import kb

from cache.userdata import user_data

import traveller.equipment as eq
import traveller.career as career


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
    def __init__(self, db: connection):
        self.db = db

    def handlers(self) -> List[ConversationHandler]:
        return [
            ConversationHandler(
                entry_points=[MessageHandler(Filters.regex(r'^/scene +new +[\w]+$'), self._ask_first_npc)],
                states={
                    State.NPC: [MessageHandler(Filters.text('Add'), self._ask_characteristics_generation),
                                MessageHandler(Filters.text('End'), self._handle_end)
                                ],
                    State.CH_GEN: [MessageHandler(Filters.regex('^(Manually|Let me choose)$'), self._handle_manual_gen),
                                   MessageHandler(Filters.regex('^(Random|Generate Again)$'), self._handle_random_gen),
                                   MessageHandler(Filters.regex(r'^(Accept|(\d+ ){5}\d+)$'), self._ask_career)
                                   ],
                    State.RANK: [MessageHandler(Filters.text, self._ask_rank)],
                    State.ARMOR: [MessageHandler(Filters.regex(r'^[0-6]$'), self._ask_armor)],
                    State.WEAPON: [MessageHandler(Filters.text, self._ask_weapon)],
                    State.NAME: [MessageHandler(Filters.text, self._ask_name)],
                    State.ALLY: [MessageHandler(Filters.text, self._ask_ally)],
                    State.NPC_END: [MessageHandler(Filters.regex('^(Ally|Enemy)$'), self._handle_npc_registration)],
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

    def _ask_first_npc(self, update: Update, context: CallbackContext) -> State:
        scene_name = update.message.text.split(' ')[2]
        user_data[update.message.from_user.id].scene_name = scene_name
        with self.db:
            with self.db.cursor() as cur:
                cur.execute('INSERT INTO scene(scene_name) VALUES(%s) ON CONFLICT DO NOTHING;', (scene_name,))
        kb.next_npc.reply_text(update)
        return State.NPC

    def _ask_next_npc(self, update: Update, context: CallbackContext) -> State:
        kb.next_npc.reply_text(update)
        return State.NPC

    def _handle_end(self, update: Update, context: CallbackContext) -> State:
        return State.END

    def _ask_characteristics_generation(self, update: Update, context: CallbackContext) -> State:
        kb.ch_gen.reply_text(update)
        user_data[update.message.from_user.id].npc = Npc()
        return State.CH_GEN

    def _handle_manual_gen(self, update: Update, context: CallbackContext) -> State:
        kb.ch_manual_gen.reply_text(update)
        return State.CH_GEN

    def _handle_random_gen(self, update: Update, context: CallbackContext) -> State:
        npc = user_data[update.message.from_user.id].npc
        npc.STR = randint(1, 6)
        npc.DEX = randint(1, 6)
        npc.END = randint(1, 6)
        npc.INT = randint(1, 6)
        npc.EDU = randint(1, 6)
        npc.SOC = randint(1, 6)
        kb.ch_random_gen.reply_text(update, params=(npc.STR, npc.DEX, npc.END,
                                                    npc.INT, npc.EDU, npc.SOC))
        return State.CH_GEN

    def _ask_career(self, update: Update, context: CallbackContext) -> State:
        npc = user_data[update.message.from_user.id].npc
        if update.message.text != 'Accept':
            v = update.message.text.split(' ')
            for val in v:
                if int(val) <= 1:
                    update.message.reply_text('Values not admissible.')
                    return State.CH_GEN
            npc.STR = int(v[0])
            npc.DEX = int(v[1])
            npc.END = int(v[2])
            npc.INT = int(v[3])
            npc.EDU = int(v[4])
            npc.SOC = int(v[5])

        kb.career.reply_text(update, keys=[[c.name] for c in career.careers])
        return State.RANK

    def _ask_rank(self, update: Update, context: CallbackContext) -> State:
        npc = user_data[update.message.from_user.id].npc
        for c in career.careers:
            if c.name == update.message.text:
                npc.career = c
                break
        kb.rank.reply_text(update, keys=[[1, 2, 3], [4, 5, 6], [0]])
        return State.ARMOR

    def _ask_armor(self, update: Update, context: CallbackContext) -> State:
        npc = user_data[update.message.from_user.id].npc
        if not re.match(r'^\d+$', update.message.text):
            return State.RANK
        npc.rank = int(update.message.text)
        if npc.rank > 6:
            return State.RANK
        keys = []
        for _id in eq.equipments:
            if isinstance(eq.equipments[_id], eq.Armor):
                keys.append([eq.equipments[_id].name])
                pass

        kb.armor.reply_text(update, keys=keys)
        return State.WEAPON

    def _ask_weapon(self, update: Update, context: CallbackContext) -> State:
        npc = user_data[update.message.from_user.id].npc
        npc.armor = eq.get_equipment_by_name(update.message.text)
        if not npc.armor:
            return State.ARMOR
        keys = []
        for _id in eq.equipments:
            if isinstance(eq.equipments[_id], eq.Weapon):
                keys.append([eq.equipments[_id].name])
                pass

        kb.weapon.reply_text(update, keys=keys)
        return State.NAME

    def _ask_name(self, update: Update, context: CallbackContext) -> State:
        npc = user_data[update.message.from_user.id].npc
        npc.armor = eq.get_equipment_by_name(update.message.text)
        if not npc.armor:
            return State.WEAPON
        kb.name.reply_text(update)
        return State.ALLY

    def _ask_ally(self, update: Update, context: CallbackContext) -> State:
        npc = user_data[update.message.from_user.id].npc
        npc.name = update.message.text
        if not re.match(r'^\w+$', npc.name):
            return State.NAME
        kb.ally.reply_text(update)
        return State.NPC_END

    def _handle_npc_registration(self, update: Update, context: CallbackContext) -> State:
        npc = user_data[update.message.from_user.id].npc
        scene_name = user_data[update.message.from_user.id].scene_name
        npc.ally = update.message.text == 'Ally'
        # TODO register npc to self.db
        with self.db:
            with self.db.cursor() as cur:
                cur.execute('INSERT INTO npcs(npc_name, strength, dexterity, endurance, intelligence, education,'
                            ' social_standing, career, rank, armor, weapon, ally, scene) '
                            'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) '
                            'ON CONFLICT(id) DO NOTHING;', (npc.name, npc.STR, npc.DEX, npc.END, npc.INT,
                                                            npc.EDU, npc.SOC, npc.career, npc.rank, npc.armor,
                                                            npc.weapon, npc.ally, scene_name))
        return State.NEXT
