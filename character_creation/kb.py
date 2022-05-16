import telegram
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

from keyboards.keyboards import Keyboard

# Characteristics

rolling_stats = Keyboard('🎲 Rolling for your starting *characteristics*...', parse_mode=telegram.ParseMode.MARKDOWN)

_ch: str = '💪 *STR*: %s\n' \
           '🏃 *END*: %s\n' \
           '🗡️ *DEX*: %s\n' \
           '🧠 *INT*: %s\n' \
           '📚 *EDU*: %s\n' \
           '👑 *SOC*: %s'

characteristics = Keyboard(
    'Results are in! These are your starting *characteristics*:\n' + _ch,
    reply_markup=ReplyKeyboardRemove(),
    parse_mode=telegram.ParseMode.MARKDOWN
)

# Homeworld

world = Keyboard('🪐 You\'ll now have to choose your homeworld in _%s_ sector!',
                 parse_mode=telegram.ParseMode.MARKDOWN)

ask_min = Keyboard('✨️ Choose the *minimum* desired *%s*',
                   reply_markup=ReplyKeyboardMarkup([
                       ['0', '1', '...', 'Ignore']
                   ], one_time_keyboard=True),
                   parse_mode=telegram.ParseMode.MARKDOWN)

ask_max = Keyboard('✨️ Choose the *maximum* desired *%s*',
                   reply_markup=ReplyKeyboardMarkup([
                       ['0', '1', '...', '10']
                   ], one_time_keyboard=True),
                   parse_mode=telegram.ParseMode.MARKDOWN)

choose_world = Keyboard('🪐 These are the available worlds on _%s_ that match your criteria, choose one!',
                        reply_markup=ReplyKeyboardMarkup([
                            ['A', 'B', '...']
                        ], one_time_keyboard=False),
                        parse_mode=telegram.ParseMode.MARKDOWN)

no_world_found = Keyboard('❌ Sorry! There are no worlds in this sector that satisfy your filters, let\'s try again!')

# Homeworld and Education skills

ask_homeworld_skill = Keyboard('📝 Choose a *homeworld skill* to acquire: _(%s left)_',
                               reply_markup=ReplyKeyboardMarkup([
                                   ['Skill1', 'Skill2', '...']
                               ], one_time_keyboard=False),
                               parse_mode=telegram.ParseMode.MARKDOWN)

ask_education_skill = Keyboard('📝 Choose an *education skill* to acquire: _(%s left)_',
                               reply_markup=ReplyKeyboardMarkup([
                                   ['Skill1', 'Skill2', '...']
                               ], one_time_keyboard=False),
                               parse_mode=telegram.ParseMode.MARKDOWN)

# Career qualification + Basic Training

career = Keyboard('🔨 Which *career* do you want to qualify for?',
                  reply_markup=ReplyKeyboardMarkup([
                      ['Skill1', 'Skill2', '...']
                  ], one_time_keyboard=True),
                  parse_mode=telegram.ParseMode.MARKDOWN)

rolling_qualification = Keyboard('🎲 Rolling for *qualification*...', parse_mode=telegram.ParseMode.MARKDOWN)

qualified = Keyboard('✅ You successfully qualified!')

qualified_sequent_career = Keyboard('✅ You qualified! Choose a *Skill* to acquire:',
                                    reply_markup=ReplyKeyboardMarkup([
                                        ['Skill1', 'Skill2', '...']
                                    ], one_time_keyboard=False),
                                    parse_mode=telegram.ParseMode.MARKDOWN)

skill_acquired = Keyboard('✨ You acquired *%s!*', parse_mode=telegram.ParseMode.MARKDOWN)

draft_or_drifter = Keyboard('❌ You failed to qualify. Choose to become a *Drifter* or to be *Drafted*:',
                            reply_markup=ReplyKeyboardMarkup([
                                ['Drifter', 'Draft']
                            ], one_time_keyboard=True),
                            parse_mode=telegram.ParseMode.MARKDOWN)

drafted = Keyboard('🔨 You were drafted into *%s*!', parse_mode=telegram.ParseMode.MARKDOWN)

# Survival

rolling_survival = Keyboard('🎲 Rolling for *survival*...', parse_mode=telegram.ParseMode.MARKDOWN)

survival_drugs = Keyboard('🔁 You used drugs last term, rolling for a second *survival* check...', parse_mode=telegram.ParseMode.MARKDOWN)

survival_success = Keyboard('✅ You passed your survival roll!')

survival_death = Keyboard('💀 You failed your survival roll and died during this term. You\'ll need to start over.')

survival_fail = Keyboard('❌ You failed your survival roll!')

characteristics_dmg = Keyboard(
    'Your *characteristics* after being damaged are:' + _ch,
    reply_markup=ReplyKeyboardRemove(),
    parse_mode=telegram.ParseMode.MARKDOWN
)

injury_crisis = Keyboard('🏥 You suffered from an injury crisis, you\'ll die unless you\'ll be able to pay %sCr!')

# Commission and Advancement

rolling_commission = Keyboard('🎲 Rolling for *commission*...', parse_mode=telegram.ParseMode.MARKDOWN)

rolling_advancement = Keyboard('🎲 Rolling for *advancement*...', parse_mode=telegram.ParseMode.MARKDOWN)

promoted = Keyboard('✅ You got promoted to *Rank %s*!', parse_mode=telegram.ParseMode.MARKDOWN)

commission_failed = Keyboard('❌ You failed your commission roll!')

advancement_failed = Keyboard('❌ You failed your advancement roll!')

table_choice = Keyboard('📦 Choose one of the following tables to roll on:',  # TODO dice instead of package?
                        reply_markup=ReplyKeyboardMarkup([
                            ['Personal Development'], ['Service Skills'], ['Specialist Skills'], ['Advanced Education']
                        ], one_time_keyboard=False))

char_increased = Keyboard('✨ Your *%s* increased!', parse_mode=telegram.ParseMode.MARKDOWN)

# Drugs + Aging

ask_drugs = Keyboard(
    '💊 Do you want to use *anagathic drugs* this term?',
    reply_markup=ReplyKeyboardMarkup([['Yes', 'No']]),
    parse_mode=telegram.ParseMode.MARKDOWN
)

stop_drugs = Keyboard('The shock hits you!')

aging = Keyboard('You are now %s')

aging_fail = Keyboard('Effects of aging show up...')

aging_crisis = Keyboard('You suffered from an aging crisis, you\'ll die if you won\'t be able to pay %sCr!')

reenlistment_retire = Keyboard('You are now too old to keep working, you must retire.')

reenlistment_12 = Keyboard('You are too good and must continue in this career')

reenlistment_fail = Keyboard('You failed to reenlist!')


debt = Keyboard('During your career you got in debt and now you paid "%s"')

negative_number = Keyboard('You are in debt of "%s" credits')

ask_retire = Keyboard('Do you want to retire?',
                      reply_markup=ReplyKeyboardMarkup([
                          ['Yes', 'No']
                      ], one_time_keyboard=True))

continue_career = Keyboard('Do you want continue with this career?',
                           reply_markup=ReplyKeyboardMarkup([
                               ['Yes', 'No']
                           ], one_time_keyboard=False))

muster_choice = Keyboard('Do you want to roll on Cash or Material Benefits?',
                         reply_markup=ReplyKeyboardMarkup([
                             ['Cash', 'Material']
                         ], one_time_keyboard=True))

undo_damage = Keyboard('Do you want to restore a point of damage in the following characteristics?',
                       reply_markup=ReplyKeyboardMarkup([
                           ['Strength - 2000Cr'], ['Dexterity - 1000Cr']
                       ]))

character_name = Keyboard('What\'s your name?')

character_sex = Keyboard('What\'s your sex?', reply_markup=ReplyKeyboardMarkup([['M', 'F']]))

buy_equip = Keyboard('You have "%s" credits, do you want to buy something?',
                     reply_markup=ReplyKeyboardMarkup([
                         ['A', 'B', '...', 'No']
                     ], one_time_keyboard=True))
