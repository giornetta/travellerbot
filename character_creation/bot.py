from typing import Callable, Optional

from telegram import Update
from telegram.ext import ConversationHandler, MessageHandler, Filters, CallbackContext

from cache.userdata import user_data
from character_creation import kb
from character_creation.service import CharacterCreator
from traveller import career
from traveller.career import CareerType, ReEnlistmentOutcome, careers
from traveller.character import Character
from traveller.characteristic import Characteristic
from traveller.skill import Skill, education_skills
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
    CONTINUE = auto()
    BENEFITS = auto()
    END = auto()


filter_starport = Filters.regex('^(X|E|D|C|B|A|Ignore)$')
filter_10 = Filters.regex('^([0-9]|10|Ignore)$')
filter_15 = Filters.regex('^([0-9]|1[0-5]|Ignore)$')
filter_skills_and_training = Filters.regex('^(Personal Development|Service Skills|Specialist Skills|Advanced Education)$')


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
                State.CAREER: [MessageHandler(Filters.text, self._handle_career)],
                State.DRAFT_OR_DRIFTER: [MessageHandler(Filters.regex('^(Drifter|Draft)$'), self._handle_draft_or_drifter)],
                State.CAREER_SKILL: [MessageHandler(Filters.text, self._handle_career_skill)],
                State.COMMISSION: [MessageHandler(filter_skills_and_training, self._handle_commission_table)],
                State.ADVANCEMENT: [MessageHandler(filter_skills_and_training, self._handle_advancement_table)],
                State.SKILLS_AND_TRAINING: [MessageHandler(filter_skills_and_training,self._handle_skills_and_training)],
                State.SECOND_SKILLS_AND_TRAINING: [MessageHandler(filter_skills_and_training, self._handle_second_skills_and_training)],
                State.DRUGS: [MessageHandler(Filters.regex('^(Yes|No)$'), self._handle_drugs)],
                State.CONTINUE: [MessageHandler(Filters.regex('^(Yes|No)$'), self._handle_continue)],
                State.BENEFITS: [MessageHandler(Filters.regex('(Cash|Material)$'), self._handle_benefits)]
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
        skills = 3 + user_data[user_id].character.modifier(Characteristic.EDU)
        user_data[user_id].homeworld_skills_left = min(skills, min(2, len(homeworld.homeworld_skills)))
        user_data[user_id].education_skills_left = max(0, skills - user_data[user_id].homeworld_skills_left)

        kb.ask_homeworld_skill.reply_text(update, keys=single_keys(homeworld.homeworld_skills))
        return State.HOMEWORLD_SKILL

    def _handle_homeworld_skill(self, update: Update, context: CallbackContext):
        user_id = update.message.from_user.id

        skill = update.message.text
        if skill not in user_data[user_id].character.homeworld.homeworld_skills or skill in user_data[user_id].character.skill_names:
            return State.HOMEWORLD_SKILL

        user_data[user_id].character.acquire_skill(Skill(skill, 0))
        user_data[user_id].homeworld_skills_left -= 1

        if user_data[user_id].homeworld_skills_left > 0:
            skills_left = user_data[user_id].character.homeworld.homeworld_skills
            skills_left.remove(skill)
            kb.ask_homeworld_skill.reply_text(update, keys=single_keys(skills_left))
            return State.HOMEWORLD_SKILL
        elif user_data[user_id].education_skills_left > 0:
            kb.ask_education_skill.reply_text(update, keys=single_keys(education_skills))
            return State.EDUCATION_SKILL
        elif user_data[user_id].adventure.terms != 0:
            kb.career.reply_text(update, keys=single_keys(list(careers.keys())))
            return State.CAREER
        else:
            return self._debts(update)  # TODO eventually change this to proper stage: i.e. skipping careers

    def _handle_education_skill(self, update: Update, context: CallbackContext) -> State:
        user_id = update.message.from_user.id

        skill = update.message.text
        # TODO REMOVE SKILLS I HAVE FROM LIST
        if skill not in education_skills or skill in user_data[user_id].character.skill_names:
            return State.EDUCATION_SKILL

        user_data[user_id].character.acquire_skill(Skill(skill, 0))
        user_data[user_id].education_skills_left -= 1

        if user_data[user_id].education_skills_left > 0:
            skills_left = education_skills.copy()
            skills_left.remove(skill)
            kb.ask_education_skill.reply_text(update, keys=single_keys(skills_left))
            return State.EDUCATION_SKILL
        elif user_data[user_id].adventure.terms != 0:
            kb.career.reply_text(update, keys=single_keys(list(careers.keys())))
            return State.CAREER
        else:
            return self._debts(update) # TODO eventually change this to proper stage: i.e. skipping careers

    def _handle_career(self, update: Update, context: CallbackContext) -> State:
        user_id = update.message.from_user.id

        c = careers.get(update.message.text)
        if not c:
            return State.CAREER

        qualified, skills = user_data[user_id].character.qualify(c)
        if qualified:
            return self._basic_training(update, c, skills)
        else:
            kb.draft_or_drifter.reply_text(update)
            return State.DRAFT_OR_DRIFTER

    def _handle_draft_or_drifter(self, update: Update, context: CallbackContext) -> State:
        user_id = update.message.from_user.id

        if update.message.text == 'Draft':
            c = user_data[user_id].character.draft()
            kb.drafted.reply_text(update, params=c.name)
        else:
            c = career.drifter
        _, skills = user_data[user_id].character.qualify(c, drafted=True)
        return self._basic_training(update, c, skills)

    def _basic_training(self, update: Update, c: CareerType, skills: Optional[List[str]]) -> State:
        user_id = update.message.from_user.id

        if skills is not None:
            kb.qualified.reply_text(update, params=', '.join(skills))
            return self.survival(update)
        else:
            kb.qualified_sequent_career.reply_text(update, keys=single_keys(list(c.skill_and_training[1].values())))
            return State.CAREER_SKILL

    def _handle_career_skill(self, update: Update, context: CallbackContext):
        user_id = update.message.from_user.id
        if update.message.text not in user_data[user_id].character.career.career_type.skill_and_training[1].values():
            return State.CAREER_SKILL

        user_data[user_id].character.acquire_skill(Skill(update.message.text, 0))
        return self.survival(update)

    def survival(self, update: Update) -> State:
        user_id = update.message.from_user.id
        # Survival ROLL
        survived = user_data[user_id].character.survival_roll()
        if not survived:
            if user_data[user_id].adventure.survival_kills:
                kb.survival_death.reply_text(update)
                start_character_creation(update)
                return State.MIN_STARPORT
            else:
                # TODO add better messaging
                message = user_data[user_id].character.mishaps_roll()
                update.message.reply_text(message)
                kb.characteristics.reply_text(update, params=user_data[user_id].character.stats_tuple)
                return self._benefits(update, failed_survival=True)

        # Second survival roll
        if user_data[user_id].character.took_drugs:
            survived = user_data[user_id].character.survival_roll()
            if not survived:
                # TODO add better messaging
                message = user_data[user_id].character.mishaps_roll()
                update.message.reply_text(message)
                kb.characteristics.reply_text(update, params=user_data[user_id].character.stats_tuple)
                return self._benefits(update, failed_survival=True)

        # Commission and advancement
        if not user_data[user_id].character.drafted:
            success = user_data[user_id].character.commission_roll()
            if success is not None:
                if success:
                    kb.table_choice.reply_text(update, params='1')
                    return State.COMMISSION
                else:
                    kb.commission_failed.reply_text(update)

        return self._advancement(update)

    def _skills_and_training(self, update: Update):
        user_id = update.message.from_user.id
        upgrade = user_data[user_id].character.skills_and_training(update.message.text)
        if isinstance(upgrade, Characteristic):
            # TODO Notify +1 Char
            update.message.reply_text(f'Your {upgrade.value} increased!')
        else:
            update.message.reply_text(f'You acquired {upgrade}!')

    def _handle_commission_table(self, update: Update, context: CallbackContext) -> State:
        self._skills_and_training(update)
        return self._advancement(update)

    def _advancement(self, update: Update) -> State:
        user_id = update.message.from_user.id
        # Advancement roll
        success = user_data[user_id].character.advancement_roll()
        if success is not None:
            if success:
                kb.table_choice.reply_text(update, params=str(user_data[user_id].character.career.rank))
                return State.ADVANCEMENT
            else:
                kb.advancement_failed.reply_text(update)

        kb.table_choice_no_promo.reply_text(update)
        return State.SKILLS_AND_TRAINING

    def _handle_advancement_table(self, update: Update, context: CallbackContext) -> State:
        self._skills_and_training(update)

        kb.table_choice_no_promo.reply_text(update)
        return State.SKILLS_AND_TRAINING

    def _handle_skills_and_training(self, update: Update, context: CallbackContext) -> State:
        user_id = update.message.from_user.id
        self._skills_and_training(update)

        c = user_data[user_id].character.career.career_type
        if c.commission or c.advancement:
            return self._ask_drugs(update)

        kb.table_choice_no_promo.reply_text(update)
        return State.SECOND_SKILLS_AND_TRAINING

    def _handle_second_skills_and_training(self, update: Update, context: CallbackContext) -> State:
        user_id = update.message.from_user.id
        self._skills_and_training(update)
        return self._ask_drugs(update)

    def _ask_drugs(self, update: Update) -> State:
        user_id = update.message.from_user.id

        if user_data[user_id].character.age >= 30:
            kb.ask_drugs.reply_text(update)
            return State.DRUGS

        return self._age(update)

    def _handle_drugs(self, update: Update, context: CallbackContext) -> State:
        user_id = update.message.from_user.id

        user_data[user_id].character.use_drugs(update.message.text == 'Yes')

        return self._reenlistment(update)

    def _age(self, update: Update) -> State:
        user_id = update.message.from_user.id
        user_data[user_id].character.increase_age()

        # Re Enlistment
        return self._reenlistment(update)

    def _reenlistment(self, update: Update) -> State:
        user_id = update.message.from_user.id

        outcome = user_data[user_id].character.reenlistment_roll(user_data[user_id].adventure.terms)
        if outcome == ReEnlistmentOutcome.MUST_RETIRE:
            kb.reenlistment_retire.reply_text(update)
            return self._benefits(update)
        elif outcome == ReEnlistmentOutcome.FORCED_CONTINUE:
            user_data[user_id].character.continue_career()
            kb.reenlistment_12.reply_text(update)
            return self.survival(update)
        elif outcome == ReEnlistmentOutcome.SUCCESS:
            kb.continue_career.reply_text(update)
            return State.CONTINUE
        else:
            return self._benefits(update)

    def _handle_continue(self, update: Update, context: CallbackContext) -> State:
        user_id = update.message.from_user.id

        if update.message.text == 'Yes':
            user_data[user_id].character.continue_career()
            return self.survival(update)
        else:
            return self._benefits(update)

    def _benefits(self, update: Update, failed_survival: bool = False) -> State:
        user_id = update.message.from_user.id

        user_data[user_id].character.compute_benefit_rolls(failed_survival)

        if user_data[user_id].character.benefit_rolls <= 0:
            if not user_data[user_id].character.retired:
                kb.career.reply_text(update, keys=single_keys(user_data[user_id].character.available_careers))
                return State.CAREER
            else:
                return self._debts(update)

        if user_data[user_id].character.cash_rolls > 0:
            kb.muster_choice.reply_text(update)
            return State.BENEFITS

        return self._benefit_roll(update)

    def _handle_benefits(self, update: Update, context: CallbackContext) -> State:
        return self._benefit_roll(update, cash=update.message.text == 'Cash')

    def _benefit_roll(self, update: Update, cash: bool = False):
        user_id = update.message.from_user.id

        user_data[user_id].character.roll_benefit(cash)

        if user_data[user_id].character.benefit_rolls <= 0:
            if not user_data[user_id].character.retired:
                kb.career.reply_text(update, keys=single_keys(user_data[user_id].character.available_careers))
                return State.CAREER
            else:
                return self._debts(update)

        if user_data[user_id].character.cash_rolls > 0:
            kb.muster_choice.reply_text(update)
            return State.BENEFITS

        return self._benefit_roll(update)

    def _debts(self, update: Update) -> State:
        update.message.reply_text('DEBITI')
        return State.END  # TODO ADD PROPER


def start_character_creation(update: Update):
    user_id = update.message.from_user.id

    # Create character
    user_data[user_id].character = Character()
    user_data[user_id].character.roll_stats()

    kb.characteristics.reply_text(update, params=user_data[user_id].character.stats_tuple)

    kb.world.reply_text(update, params=user_data[user_id].adventure.sector)

    kb.ask_min.reply_text(
        update, params='Starport',
        keys=[['X', 'E', 'D'], ['C', 'B', 'A'], ['Ignore']]
    )


def num_keys(start: int, end: int) -> List[List[str]]:
    kl = [str(i) for i in range(start, end + 1)]
    kl.append('Ignore')

    return [kl[i: i + 3] for i in range(0, len(kl), 3)]


def single_keys(l: List[str]) -> List[List[str]]:
    return [l[i: i + 1] for i in range(0, len(l), 1)]