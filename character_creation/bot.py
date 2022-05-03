from typing import Callable

from telegram import Update
from telegram.ext import ConversationHandler, MessageHandler, Filters, CallbackContext

from cache.userdata import user_data
from character_creation import kb
from character_creation.service import CharacterCreator
from traveller.characteristic import Characteristic
from traveller.skill import education_skills
from traveller.world import *
from traveller.world import Attribute, starport_values
from travellermap import api


class State(Enum):
    MIN_STARPORT = auto()
    MAX_STARPORT = auto()
    MIN_SIZE = auto()
    MAX_SIZE = auto()
    MIN_ATM = auto()
    MAX_ATM = auto()
    MIN_HYDRO = auto()
    MAX_HYDRO = auto()
    MIN_POP = auto()
    MAX_POP = auto()
    MIN_GOV = auto()
    MAX_GOV = auto()
    MIN_LAW = auto()
    MAX_LAW = auto()
    MIN_TECH = auto()
    MAX_TECH = auto()
    WORLD = auto()
    HOMEWORLD_SKILL = auto()
    EDUCATION_SKILL = auto()
    CAREER = auto()


filter_starport = Filters.regex('^(X|E|D|C|B|A|Ignore)$')
filter_10 = Filters.regex('^([0-9]|10|Ignore)$')
filter_15 = Filters.regex('^([0-9]|1[0-5]|Ignore)$')


class CharacterCreationConversation:
    service: CharacterCreator

    def __init__(self, service: CharacterCreator):
        self.service = service

    def handlers(self) -> List[ConversationHandler]:
        return [ConversationHandler(
            entry_points=[MessageHandler(filter_starport, self._handle_min_starport)],
            states={
                State.MIN_STARPORT: [MessageHandler(filter_starport, self._handle_min_starport)],
                State.MAX_STARPORT: [MessageHandler(filter_starport, self._handle_max_starport)],
                State.MIN_SIZE: [MessageHandler(filter_10, self._handle_min(Attribute.SIZE))],
                State.MAX_SIZE: [MessageHandler(filter_10, self._handle_max(Attribute.SIZE))],
                State.MIN_ATM: [MessageHandler(filter_15, self._handle_min(Attribute.ATM))],
                State.MAX_ATM: [MessageHandler(filter_15, self._handle_max(Attribute.ATM))],
                State.MIN_HYDRO: [MessageHandler(filter_10, self._handle_min(Attribute.HYDRO))],
                State.MAX_HYDRO: [MessageHandler(filter_10, self._handle_max(Attribute.HYDRO))],
                State.MIN_POP: [MessageHandler(filter_10, self._handle_min(Attribute.POP))],
                State.MAX_POP: [MessageHandler(filter_10, self._handle_max(Attribute.POP))],
                State.MIN_GOV: [MessageHandler(filter_15, self._handle_min(Attribute.GOV))],
                State.MAX_GOV: [MessageHandler(filter_15, self._handle_max(Attribute.GOV))],
                State.MIN_LAW: [MessageHandler(filter_10, self._handle_min(Attribute.LAW))],
                State.MAX_LAW: [MessageHandler(filter_10, self._handle_max(Attribute.LAW))],
                State.MIN_TECH: [MessageHandler(filter_15, self._handle_min_tech)],
                State.MAX_TECH: [MessageHandler(filter_15, self._handle_max_tech)],
                State.WORLD: [MessageHandler(Filters.text, self._handle_world)],
                State.HOMEWORLD_SKILL: [MessageHandler(Filters.text, self._handle_homeworld_skill)],
                State.EDUCATION_SKILL: [MessageHandler(Filters.text, self._handle_education_skill)],
                State.CAREER: [MessageHandler(Filters.text, self._handle_career)]
            },
            fallbacks=[]
        )]

    def _handle_min_starport(self, update: Update, context: CallbackContext) -> State:
        user_id = update.message.from_user.id
        user_data[user_id].init_filters()

        if update.message.text == 'Ignore':
            kb.ask_min.reply_text(update, params=Attribute.SIZE.full_name, keys=num_keys(0, Attribute.SIZE.max))
            return State.MIN_SIZE

        user_data[user_id].filters[Attribute.STARPORT].min = starport_values[update.message.text]

        vals = ['X', 'E', 'D', 'C', 'B', 'A', 'Ignore']
        kl = [vals[i] for i in range(vals.index(update.message.text), len(vals))]
        keys = [kl[i: i + 3] for i in range(0, len(kl), 3)]

        kb.ask_max.reply_text(update, params=Attribute.STARPORT.full_name, keys=keys)

        return State.MAX_STARPORT

    def _handle_max_starport(self, update: Update, context: CallbackContext) -> State:
        user_id = update.message.from_user.id
        val = update.message.text
        vals = ['X', 'E', 'D', 'C', 'B', 'A', 'Ignore']

        if val != 'Ignore':
            user_data[user_id].filters[Attribute.STARPORT].max = max(user_data[user_id].filters[Attribute.STARPORT].min, starport_values[val])

        kb.ask_min.reply_text(update, params=Attribute.SIZE.full_name, keys=num_keys(0, Attribute.SIZE.max))
        return State.MIN_SIZE

    def _handle_min(self, attr: Attribute) -> Callable[[Update, CallbackContext], State]:
        def min_cb(update: Update, context: CallbackContext) -> State:
            user_id = update.message.from_user.id

            if update.message.text == 'Ignore':
                next_index = list(Attribute).index(attr) + 1
                next_attr: Attribute = list(Attribute)[next_index]

                kb.ask_min.reply_text(update, params=next_attr.full_name, keys=num_keys(0, next_attr.max))

                return State[f'MIN_{next_attr.name}']

            val = int(update.message.text)
            user_data[user_id].filters[attr].min = val

            kb.ask_max.reply_text(update, params=attr.full_name, keys=num_keys(val, attr.max))

            return State[f'MAX_{attr.name}']

        return min_cb

    def _handle_max(self, attr: Attribute) -> Callable[[Update, CallbackContext], State]:
        def max_cb(update: Update, context: CallbackContext) -> State:
            user_id = update.message.from_user.id

            if update.message.text != 'Ignore':
                user_data[user_id].filters[attr].max = max(user_data[user_id].filters[attr].min, int(update.message.text))

            next_index = list(Attribute).index(attr) + 1
            next_attr = list(Attribute)[next_index]

            kb.ask_min.reply_text(update, params=next_attr.full_name, keys=num_keys(0, next_attr.max))
            return State[f'MIN_{next_attr.name}']

        return max_cb

    def _handle_min_tech(self, update: Update, context: CallbackContext):
        user_id = update.message.from_user.id

        if update.message.text == 'Ignore':
            return self._world_selection(update)

        val = int(update.message.text)
        user_data[user_id].filters[Attribute.TECH].min = val

        kb.ask_max.reply_text(update, params=Attribute.TECH.full_name, keys=num_keys(val, Attribute.TECH.max))

        return State.MAX_TECH

    def _handle_max_tech(self, update: Update, context: CallbackContext) -> State:
        user_id = update.message.from_user.id

        if update.message.text != 'Ignore':
            user_data[user_id].filters[Attribute.TECH].max = max(user_data[user_id].filters[Attribute.TECH].min, int(update.message.text))

        return self._world_selection(update)

    def _world_selection(self, update: Update):
        user_id = update.message.from_user.id

        worlds = api.world_filter(user_data[user_id].adventure.sector, user_data[user_id].filters)

        if len(worlds) == 0:
            kb.no_world_found.reply_text(update)
            kb.ask_min.reply_text(update, params=Attribute.STARPORT.full_name, keys=[['X', 'E', 'D'], ['C', 'B', 'A'], ['Ignore']])
            return State.MIN_STARPORT

        kb.choose_world.reply_text(update, params=user_data[user_id].adventure.sector, keys=single_keys(worlds))

        return State.WORLD

    def _handle_world(self, update: Update, context: CallbackContext):
        user_id = update.message.from_user.id

        homeworld = api.world(user_data[user_id].adventure.sector, update.message.text)
        if not homeworld:
            return State.WORLD

        user_data[user_id].character.homeworld = homeworld
        skills = 3 + user_data[user_id].character.modifiers[Characteristic.EDU]
        user_data[user_id].homeworld_skills_left = min(skills, min(2, len(homeworld.homeworld_skills)))
        user_data[user_id].education_skills_left = max(0, skills - user_data[user_id].homeworld_skills_left)

        kb.ask_homeworld_skill.reply_text(update, keys=single_keys(homeworld.homeworld_skills))
        return State.HOMEWORLD_SKILL

    def _handle_homeworld_skill(self, update: Update, context: CallbackContext):
        user_id = update.message.from_user.id

        skill = update.message.text
        if skill not in user_data[user_id].character.homeworld.homeworld_skills or skill in user_data[user_id].character.skill_names:
            return State.HOMEWORLD_SKILL

        user_data[user_id].character.acquire_skill(skill)
        user_data[user_id].homeworld_skills_left -= 1

        if user_data[user_id].homeworld_skills_left > 0:
            skills_left = user_data[user_id].character.homeworld.homeworld_skills
            skills_left.remove(skill)
            kb.ask_homeworld_skill.reply_text(update, keys=single_keys(skills_left))
            return State.HOMEWORLD_SKILL
        elif user_data[user_id].education_skills_left > 0:
            kb.ask_education_skill.reply_text(update, keys=single_keys(education_skills))
            return State.EDUCATION_SKILL
        else:
            kb.career.reply_text(update)  # TODO add careers list

    def _handle_education_skill(self, update: Update, context: CallbackContext) -> State:
        user_id = update.message.from_user.id

        skill = update.message.text
        if skill not in education_skills or skill in user_data[user_id].character.skill_names:
            return State.EDUCATION_SKILL

        user_data[user_id].character.acquire_skill(skill)
        user_data[user_id].education_skills_left -= 1

        if user_data[user_id].education_skills_left > 0:
            skills_left = education_skills.copy()
            skills_left.remove(skill)
            kb.ask_education_skill.reply_text(update, keys=single_keys(skills_left))
            return State.EDUCATION_SKILL
        else:
            kb.career.reply_text(update)  # TODO add careers list
            return State.CAREER

    def _handle_career(self, update: Update, context: CallbackContext) -> State:
        update.message.reply_text('Yoo')
        return State.CAREER


def num_keys(start: int, end: int) -> List[List[str]]:
    kl = [str(i) for i in range(start, end + 1)]
    kl.append('Ignore')

    return [kl[i: i + 3] for i in range(0, len(kl), 3)]


def single_keys(l: List[str]) -> List[List[str]]:
    return [l[i: i + 1] for i in range(0, len(l), 1)]