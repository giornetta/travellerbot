from typing import Callable, Optional

import telegram
from telegram import ReplyKeyboardRemove, Update
from telegram.ext import ConversationHandler, MessageHandler, Filters, CallbackContext

from bot.state import ConversationState
from cache.userdata import user_data
from character_creation import kb
from character_creation.service import CharacterCreator
from keyboards.keyboards import single_keys
from traveller import career
from traveller.career import CareerType, ReEnlistmentOutcome, careers
from traveller.character import Character
from traveller.characteristic import Characteristic
from traveller.equipment import Weapon
from traveller.skill import Skill
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
    DRAFT_OR_DRIFTER = auto()
    CAREER_SKILL = auto()
    COMMISSION = auto()
    ADVANCEMENT = auto()
    SKILLS_AND_TRAINING = auto()
    SECOND_SKILLS_AND_TRAINING = auto()
    DRUGS = auto()
    RETIRE = auto()
    CONTINUE = auto()
    BENEFITS = auto()
    UNDO_DAMAGE = auto()
    NAME = auto()
    SEX = auto()
    END = auto()


filter_min_10 = Filters.regex('^([0-9]|10|Ignore)$')
filter_max_10 = Filters.regex('^([0-9]|10)$')

filter_min_15 = Filters.regex('^([0-9]|1[0-5]|Ignore)$')
filter_max_15 = Filters.regex('^([0-9]|1[0-5])$')

filter_skills_and_training = Filters.regex(
    '^(Personal Development|Service Skills|Specialist Skills|Advanced Education)$')


class CharacterCreationConversation:
    service: CharacterCreator

    def __init__(self, service: CharacterCreator):
        self.service = service

    def handlers(self) -> List[ConversationHandler]:
        return [ConversationHandler(
            entry_points=[MessageHandler(Filters.regex('^(X|E|D|C|B|A|Ignore)$'), self._handle_min_starport)],
            states={
                State.MIN_STARPORT: [
                    MessageHandler(Filters.regex('^(X|E|D|C|B|A|Ignore)$'), self._handle_min_starport)],
                State.MAX_STARPORT: [MessageHandler(Filters.regex('^(X|E|D|C|B|A)$'), self._handle_max_starport)],
                State.MIN_SIZE: [MessageHandler(filter_min_10, self._handle_min(Attribute.SIZE))],
                State.MAX_SIZE: [MessageHandler(filter_max_10, self._handle_max(Attribute.SIZE))],
                State.MIN_ATM: [MessageHandler(filter_min_15, self._handle_min(Attribute.ATM))],
                State.MAX_ATM: [MessageHandler(filter_max_15, self._handle_max(Attribute.ATM))],
                State.MIN_HYDRO: [MessageHandler(filter_min_10, self._handle_min(Attribute.HYDRO))],
                State.MAX_HYDRO: [MessageHandler(filter_max_10, self._handle_max(Attribute.HYDRO))],
                State.MIN_POP: [MessageHandler(filter_min_10, self._handle_min(Attribute.POP))],
                State.MAX_POP: [MessageHandler(filter_max_10, self._handle_max(Attribute.POP))],
                State.MIN_GOV: [MessageHandler(filter_min_15, self._handle_min(Attribute.GOV))],
                State.MAX_GOV: [MessageHandler(filter_max_15, self._handle_max(Attribute.GOV))],
                State.MIN_LAW: [MessageHandler(filter_min_10, self._handle_min(Attribute.LAW))],
                State.MAX_LAW: [MessageHandler(filter_max_10, self._handle_max(Attribute.LAW))],
                State.MIN_TECH: [MessageHandler(filter_min_15, self._handle_min_tech)],
                State.MAX_TECH: [MessageHandler(filter_max_15, self._handle_max_tech)],
                State.WORLD: [MessageHandler(Filters.text, self._handle_world)],
                State.HOMEWORLD_SKILL: [MessageHandler(Filters.text, self._handle_homeworld_skill)],
                State.EDUCATION_SKILL: [MessageHandler(Filters.text, self._handle_education_skill)],
                State.CAREER: [MessageHandler(Filters.text, self._handle_career)],
                State.DRAFT_OR_DRIFTER: [
                    MessageHandler(Filters.regex('^(Drifter|Draft)$'), self._handle_draft_or_drifter)],
                State.CAREER_SKILL: [MessageHandler(Filters.text, self._handle_career_skill)],
                State.COMMISSION: [MessageHandler(filter_skills_and_training, self._handle_commission_table)],
                State.ADVANCEMENT: [MessageHandler(filter_skills_and_training, self._handle_advancement_table)],
                State.SKILLS_AND_TRAINING: [
                    MessageHandler(filter_skills_and_training, self._handle_skills_and_training)],
                State.SECOND_SKILLS_AND_TRAINING: [
                    MessageHandler(filter_skills_and_training, self._handle_second_skills_and_training)],
                State.DRUGS: [MessageHandler(Filters.regex('^(Yes|No)$'), self._handle_drugs)],
                State.RETIRE: [MessageHandler(Filters.regex('^(Yes|No)$'), self._handle_retire)],
                State.CONTINUE: [MessageHandler(Filters.regex('^(Yes|No)$'), self._handle_continue)],
                State.BENEFITS: [MessageHandler(Filters.regex('(Cash|Material)$'), self._handle_benefits)],
                State.NAME: [MessageHandler(Filters.regex("^[A-Za-z]+$"), self._handle_name)],
                State.SEX: [MessageHandler(Filters.regex("^(M|F)$"), self._handle_sex)],
                State.UNDO_DAMAGE: [MessageHandler(Filters.text, self._handle_undo_damage)]
            },
            fallbacks=[],
            map_to_parent={
                State.END: ConversationState.PLAYER_IDLE,
            },
            name='create_character',
            persistent=True,
        )]

    def _handle_min_starport(self, update: Update, context: CallbackContext) -> State:
        user = user_data[update.message.from_user.id]
        user.init_filters()

        if update.message.text == 'Ignore':
            kb.ask_min.reply_text(update, params=Attribute.SIZE.full_name,
                                  keys=num_keys(0, Attribute.SIZE.max, ignore=True))
            return State.MIN_SIZE

        user.filters[Attribute.STARPORT].min = starport_values[update.message.text]

        vals = ['X', 'E', 'D', 'C', 'B', 'A']
        kl = [vals[i] for i in range(vals.index(update.message.text), len(vals))]
        keys = [kl[i: i + 3] for i in range(0, len(kl), 3)]

        kb.ask_max.reply_text(update, params=Attribute.STARPORT.full_name, keys=keys)
        return State.MAX_STARPORT

    def _handle_max_starport(self, update: Update, context: CallbackContext) -> State:
        user = user_data[update.message.from_user.id]

        val = update.message.text
        user.filters[Attribute.STARPORT].max = max(user.filters[Attribute.STARPORT].min, starport_values[val])

        kb.ask_min.reply_text(update, params=Attribute.SIZE.full_name,
                              keys=num_keys(0, Attribute.SIZE.max, ignore=True))
        return State.MIN_SIZE

    def _handle_min(self, attr: Attribute) -> Callable[[Update, CallbackContext], State]:
        def min_cb(update: Update, context: CallbackContext) -> State:
            user = user_data[update.message.from_user.id]

            if update.message.text == 'Ignore':
                next_index = list(Attribute).index(attr) + 1
                next_attr: Attribute = list(Attribute)[next_index]

                kb.ask_min.reply_text(update, params=next_attr.full_name, keys=num_keys(0, next_attr.max, ignore=True))
                return State[f'MIN_{next_attr.name}']

            val = int(update.message.text)
            user.filters[attr].min = val

            kb.ask_max.reply_text(update, params=attr.full_name, keys=num_keys(val, attr.max))
            return State[f'MAX_{attr.name}']

        return min_cb

    def _handle_max(self, attr: Attribute) -> Callable[[Update, CallbackContext], State]:
        def max_cb(update: Update, context: CallbackContext) -> State:
            user = user_data[update.message.from_user.id]

            user.filters[attr].max = max(user.filters[attr].min, int(update.message.text))

            next_index = list(Attribute).index(attr) + 1
            next_attr = list(Attribute)[next_index]

            kb.ask_min.reply_text(update, params=next_attr.full_name, keys=num_keys(0, next_attr.max, ignore=True))
            return State[f'MIN_{next_attr.name}']

        return max_cb

    def _handle_min_tech(self, update: Update, context: CallbackContext):
        user = user_data[update.message.from_user.id]

        if update.message.text == 'Ignore':
            return self._world_selection(update)

        val = int(update.message.text)
        user.filters[Attribute.TECH].min = val

        kb.ask_max.reply_text(update, params=Attribute.TECH.full_name, keys=num_keys(val, Attribute.TECH.max))
        return State.MAX_TECH

    def _handle_max_tech(self, update: Update, context: CallbackContext) -> State:
        user = user_data[update.message.from_user.id]

        user.filters[Attribute.TECH].max = max(user.filters[Attribute.TECH].min, int(update.message.text))

        return self._world_selection(update)

    def _world_selection(self, update: Update):
        user = user_data[update.message.from_user.id]

        worlds = api.world_filter(user.adventure.sector, user.filters)

        if len(worlds) == 0:
            kb.no_world_found.reply_text(update)
            kb.ask_min.reply_text(update, params=Attribute.STARPORT.full_name,
                                  keys=[['X', 'E', 'D'], ['C', 'B', 'A'], ['Ignore']])
            return State.MIN_STARPORT

        kb.choose_world.reply_text(update, params=user.adventure.sector, keys=single_keys(worlds))
        return State.WORLD

    def _handle_world(self, update: Update, context: CallbackContext):
        user = user_data[update.message.from_user.id]

        homeworld = api.world(user.adventure.sector, update.message.text)
        if not homeworld:
            return State.WORLD

        user.character.set_homeworld(homeworld)

        kb.ask_homeworld_skill.reply_text(update, params=user.character.homeworld_skills_left, keys=single_keys(homeworld.homeworld_skills))
        return State.HOMEWORLD_SKILL

    def _handle_homeworld_skill(self, update: Update, context: CallbackContext):
        user = user_data[update.message.from_user.id]

        skill = update.message.text[:-2]
        if update.message.text not in user.character.homeworld.homeworld_skills or skill in user.character.skill_names:
            return State.HOMEWORLD_SKILL

        user.character.acquire_skill(Skill(skill, 0))
        user.character.homeworld_skills_left -= 1

        if user.character.homeworld_skills_left > 0:
            skills_left = user.character.homeworld.homeworld_skills
            skills_left.remove(update.message.text)
            kb.ask_homeworld_skill.reply_text(update, params=user.character.homeworld_skills_left, keys=single_keys(skills_left))
            return State.HOMEWORLD_SKILL
        elif user.character.education_skills_left > 0:
            kb.ask_education_skill.reply_text(
                update,
                params=user.character.education_skills_left,
                keys=single_keys(user.character.available_education_skills)
            )
            return State.EDUCATION_SKILL
        elif user.adventure.terms != 0:
            kb.career.reply_text(update, keys=single_keys(list(careers.keys())))
            return State.CAREER
        else:
            return self._debts(update)

    def _handle_education_skill(self, update: Update, context: CallbackContext) -> State:
        user = user_data[update.message.from_user.id]

        skill_name = update.message.text[:-2]
        if update.message.text not in user.character.available_education_skills:
            return State.EDUCATION_SKILL

        user.character.acquire_skill(Skill(skill_name, 0))
        user.character.education_skills_left -= 1

        if user.character.education_skills_left > 0:
            kb.ask_education_skill.reply_text(
                update,
                params=user.character.education_skills_left,
                keys=single_keys(user.character.available_education_skills)
            )
            return State.EDUCATION_SKILL
        elif user.adventure.terms != 0:
            kb.career.reply_text(update, keys=single_keys(list(careers.keys())))
            return State.CAREER
        else:
            return self._debts(update)

    def _handle_career(self, update: Update, context: CallbackContext) -> State:
        user = user_data[update.message.from_user.id]

        c = careers.get(update.message.text)
        if not c:
            return State.CAREER

        kb.rolling_qualification.reply_text(update)

        qualified, skills = user.character.qualify(c)
        if qualified:
            kb.qualified.reply_text(update)
            return self._basic_training(update, c, skills)
        else:
            kb.draft_or_drifter.reply_text(update)
            return State.DRAFT_OR_DRIFTER

    def _handle_draft_or_drifter(self, update: Update, context: CallbackContext) -> State:
        user = user_data[update.message.from_user.id]

        if update.message.text == 'Draft':
            c = user.character.draft()
            kb.drafted.reply_text(update, params=c.name)
        else:
            c = career.drifter
        _, skills = user.character.qualify(c, drafted=True)
        return self._basic_training(update, c, skills)

    def _basic_training(self, update: Update, c: CareerType, skills: Optional[List[Skill]]) -> State:
        if skills is not None:
            for s in skills:
                kb.skill_acquired.reply_text(update, params=s)
            return self._survival(update)
        else:
            kb.qualified_sequent_career.reply_text(update, keys=single_keys(list(c.skill_and_training[1].values())))
            return State.CAREER_SKILL

    def _handle_career_skill(self, update: Update, context: CallbackContext):
        user = user_data[update.message.from_user.id]
        if update.message.text not in user.character.career.career_type.skill_and_training[1].values():
            return State.CAREER_SKILL

        user.character.acquire_skill(Skill(update.message.text, 0))
        return self._survival(update)

    def _survival(self, update: Update) -> State:
        user = user_data[update.message.from_user.id]

        kb.rolling_survival.reply_text(update)

        # Survival ROLL
        survived = user.character.survival_roll()
        if survived:
            kb.survival_success.reply_text(update)
        else:
            if user.adventure.survival_kills:
                kb.survival_death.reply_text(update)
                start_character_creation(update)
                return State.MIN_STARPORT
            else:
                return self._mishaps_roll(update)

        # Second survival roll
        if user.character.took_drugs:
            kb.survival_drugs.reply_text(update)
            survived = user.character.survival_roll()
            if survived:
                kb.survival_success.reply_text(update)
            else:
                return self._mishaps_roll(update)

        # Commission and advancement
        if not user.character.drafted:
            kb.rolling_commission.reply_text(update)

            success, skill = user.character.commission_roll()
            if success is not None:
                if success:
                    kb.promoted.reply_text(update, params='1')
                    if skill:
                        kb.skill_acquired.reply_text(update, params=skill)
                    kb.table_choice.reply_text(update)
                    return State.COMMISSION
                else:
                    kb.commission_failed.reply_text(update)

        return self._advancement(update)

    def _mishaps_roll(self, update: Update) -> State:
        user = user_data[update.message.from_user.id]

        kb.survival_fail.reply_text(update)

        message, dmg, crisis = user.character.mishaps_roll()

        update.message.reply_text(message)
        if dmg:
            kb.characteristics_dmg.reply_text(update, params=user.character.stats_tuple)

        if crisis > 0:
            kb.injury_crisis.reply_text(update, params=crisis)

        return self._benefits(update, failed_survival=True)

    def _skills_and_training(self, update: Update):
        user = user_data[update.message.from_user.id]

        upgrade = user.character.skills_and_training(update.message.text)
        if isinstance(upgrade, Characteristic):
            kb.char_increased.reply_text(update, params=upgrade.value)
        elif isinstance(upgrade, Skill):
            kb.skill_acquired.reply_text(update, params=upgrade)

    def _handle_commission_table(self, update: Update, context: CallbackContext) -> State:
        self._skills_and_training(update)
        return self._advancement(update)

    def _advancement(self, update: Update) -> State:
        user = user_data[update.message.from_user.id]

        kb.rolling_advancement.reply_text(update)

        # Advancement roll
        success, skill = user.character.advancement_roll()
        if success is not None:
            if success:
                kb.promoted.reply_text(update, params=str(user.character.career.rank))
                if skill:
                    kb.skill_acquired.reply_text(update, params=skill)

                kb.table_choice.reply_text(update)
                return State.ADVANCEMENT
            else:
                kb.advancement_failed.reply_text(update)

        kb.table_choice.reply_text(update)
        return State.SKILLS_AND_TRAINING

    def _handle_advancement_table(self, update: Update, context: CallbackContext) -> State:
        self._skills_and_training(update)

        kb.table_choice.reply_text(update)
        return State.SKILLS_AND_TRAINING

    def _handle_skills_and_training(self, update: Update, context: CallbackContext) -> State:
        user = user_data[update.message.from_user.id]
        self._skills_and_training(update)

        c = user.character.career.career_type
        if c.commission or c.advancement:
            return self._ask_drugs(update)

        kb.table_choice.reply_text(update)
        return State.SECOND_SKILLS_AND_TRAINING

    def _handle_second_skills_and_training(self, update: Update, context: CallbackContext) -> State:
        self._skills_and_training(update)
        return self._ask_drugs(update)

    def _ask_drugs(self, update: Update) -> State:
        user = user_data[update.message.from_user.id]

        if user.character.age >= 30:
            kb.ask_drugs.reply_text(update)
            return State.DRUGS

        return self._age(update)

    def _handle_drugs(self, update: Update, context: CallbackContext) -> State:
        user = user_data[update.message.from_user.id]

        result = user.character.use_drugs(update.message.text == 'Yes')
        if result is not None:
            success, crisis = result
            if not success:
                kb.stop_drugs.reply_text(update)
                kb.characteristics_dmg.reply_text(update, params=user.character.stats_tuple)

                if crisis > 0:
                    kb.aging_crisis.reply_text(update, params=crisis)

        return self._age(update)

    def _age(self, update: Update) -> State:
        user = user_data[update.message.from_user.id]

        success, crisis = user.character.increase_age()
        kb.aging.reply_text(update, params=user.character.age)

        if not success:
            kb.aging_fail.reply_text(update)
            kb.characteristics_dmg.reply_text(update, params=user.character.stats_tuple)

            if crisis > 0:
                kb.aging_crisis.reply_text(update, params=crisis)

        # Re Enlistment
        return self._reenlistment(update)

    def _reenlistment(self, update: Update) -> State:
        user = user_data[update.message.from_user.id]

        kb.rolling_reenlinstment.reply_text(update)

        outcome = user.character.reenlistment_roll(user.adventure.terms)
        if outcome == ReEnlistmentOutcome.MUST_RETIRE:
            kb.reenlistment_retire.reply_text(update)
            return self._benefits(update)
        elif outcome == ReEnlistmentOutcome.FORCED_CONTINUE:
            user.character.continue_career()
            kb.reenlistment_12.reply_text(update)
            return self._survival(update)
        elif outcome == ReEnlistmentOutcome.SUCCESS:
            kb.ask_retire.reply_text(update)
            return State.RETIRE
        else:
            kb.reenlistment_fail.reply_text(update)
            return self._benefits(update)

    def _handle_retire(self, update: Update, context: CallbackContext) -> State:
        user = user_data[update.message.from_user.id]

        if update.message.text == 'Yes':
            user.character.retire()
            return self._benefits(update)
        else:
            kb.continue_career.reply_text(update)
            return State.CONTINUE

    def _handle_continue(self, update: Update, context: CallbackContext) -> State:
        user = user_data[update.message.from_user.id]

        if update.message.text == 'Yes':
            user.character.continue_career()
            return self._survival(update)
        else:
            return self._benefits(update)

    def _benefits(self, update: Update, failed_survival: bool = False) -> State:
        user = user_data[update.message.from_user.id]

        user.character.compute_benefit_rolls(failed_survival)

        if user.character.benefit_rolls <= 0:
            if not user.character.retired:
                kb.career.reply_text(update, keys=single_keys(user.character.available_careers))
                return State.CAREER
            else:
                return self._debts(update)

        if user.character.cash_rolls > 0:
            kb.muster_choice.reply_text(update)
            return State.BENEFITS

        return self._benefit_roll(update)

    def _handle_benefits(self, update: Update, context: CallbackContext) -> State:
        return self._benefit_roll(update, cash=update.message.text == 'Cash')

    def _benefit_roll(self, update: Update, cash: bool = False):
        user = user_data[update.message.from_user.id]

        benefit = user.character.roll_benefit(cash)
        if cash:
            kb.credits_gained.reply_text(update, params=benefit)
        else:
            if isinstance(benefit, int):
                kb.ship_shares.reply_text(update, params=benefit)
            elif isinstance(benefit, Weapon):
                kb.weapon_benefit.reply_text(update, params=benefit.name)
            elif isinstance(benefit, str) and benefit == 'Society':
                kb.adv_society.reply_text(update)
            elif isinstance(benefit, Skill):
                kb.skill_acquired.reply_text(update, params=benefit)
            elif isinstance(benefit, Characteristic):
                kb.char_increased.reply_text(update, params=benefit.value)

        if user.character.benefit_rolls <= 0:
            if not user.character.retired:
                kb.career.reply_text(update, keys=single_keys(user.character.available_careers))
                return State.CAREER
            else:
                return self._debts(update)

        if user.character.cash_rolls > 0:
            kb.muster_choice.reply_text(update)
            return State.BENEFITS

        return self._benefit_roll(update)

    def _debts(self, update: Update) -> State:
        user = user_data[update.message.from_user.id]

        alive, message = user.character.pay_debts()
        update.message.reply_text(message, reply_markup=ReplyKeyboardRemove(), parse_mode=telegram.ParseMode.MARKDOWN)

        if not alive:
            start_character_creation(update)
            return State.MIN_STARPORT

        return self._undo_damage(update)

    def _undo_damage(self, update: Update) -> State:
        user = user_data[update.message.from_user.id]

        to_restore = user.character.to_restore
        if len(to_restore) > 0:
            kb.undo_damage.reply_text(update, params=user.character.credits, keys=single_keys(to_restore + ['Skip']))
            return State.UNDO_DAMAGE
        else:
            kb.character_name.reply_text(update)
            return State.NAME

    def _handle_undo_damage(self, update: Update, context: CallbackContext) -> State:
        user = user_data[update.message.from_user.id]

        if update.message.text == 'Skip':
            kb.character_name.reply_text(update)
            return State.NAME

        if update.message.text not in user.character.to_restore:
            return State.UNDO_DAMAGE

        l = update.message.text.split('(')[0].replace(' ', '').split('-')
        char = Characteristic[l[0]]
        price = int(l[1][:-2])

        user.character.restore_damage(char, price)

        return self._undo_damage(update)

    def _handle_sex(self, update: Update, context: CallbackContext) -> State:
        user = user_data[update.message.from_user.id]

        user.character.sex = update.message.text

        self.service.create_character(update.message.from_user.id, user.adventure.id, user.character)

        kb.creation.reply_text(update)
        return State.END

    def _handle_name(self, update: Update, context: CallbackContext) -> State:
        user = user_data[update.message.from_user.id]

        if len(update.message.text) > 32:
            kb.name_too_long.reply_text(update)
            return State.NAME

        user.character.name = update.message.text

        kb.character_sex.reply_text(update)
        return State.SEX


def start_character_creation(update: Update):
    user = user_data[update.message.from_user.id]

    kb.rolling_stats.reply_text(update)
    # Create character
    user.character = Character()
    user.character.roll_stats()

    kb.characteristics.reply_text(update, params=user.character.stats_tuple)

    kb.world.reply_text(update, params=user.adventure.sector)

    kb.ask_min.reply_text(
        update, params='Starport',
        keys=[['X', 'E', 'D'], ['C', 'B', 'A'], ['Ignore']]
    )


def num_keys(start: int, end: int, ignore: bool = False) -> List[List[str]]:
    kl = [str(i) for i in range(start, end + 1)]

    if ignore:
        kl.append('Ignore')

    return [kl[i: i + 3] for i in range(0, len(kl), 3)]

