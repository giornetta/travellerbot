from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

from keyboards.keyboards import Keyboard

# Characteristics

rolling_stats = Keyboard('🎲 Rolling for your starting *characteristics*...', )

_ch: str = '💪 *STR*: %s\n' \
           '🏃 *END*: %s\n' \
           '🗡️ *DEX*: %s\n' \
           '🧠 *INT*: %s\n' \
           '📚 *EDU*: %s\n' \
           '👑 *SOC*: %s'

characteristics = Keyboard('Results are in! These are your starting *characteristics*:\n' + _ch, reply_markup=ReplyKeyboardRemove())

# Homeworld

world = Keyboard('🪐 You\'ll now have to choose your homeworld in _%s_ sector!')

ask_min = Keyboard('✨️ Choose the *minimum* desired *%s*',
                   reply_markup=ReplyKeyboardMarkup([
                       ['0', '1', '...', 'Ignore']
                   ], one_time_keyboard=True))

ask_max = Keyboard('✨️ Choose the *maximum* desired *%s*',
                   reply_markup=ReplyKeyboardMarkup([
                       ['0', '1', '...', '10']
                   ], one_time_keyboard=True))

choose_world = Keyboard('🪐 These are the available worlds on _%s_ that match your criteria, choose one!',
                        reply_markup=ReplyKeyboardMarkup([
                            ['A', 'B', '...']
                        ], one_time_keyboard=False))

no_world_found = Keyboard('❌ Sorry! There are no worlds in this sector that satisfy your filters, let\'s try again!')

# Homeworld and Education skills

ask_homeworld_skill = Keyboard('📝 Choose a *homeworld skill* to acquire: _(%s left)_',
                               reply_markup=ReplyKeyboardMarkup([
                                   ['Skill1', 'Skill2', '...']
                               ], one_time_keyboard=False)       )

ask_education_skill = Keyboard('📝 Choose an *education skill* to acquire: _(%s left)_',
                               reply_markup=ReplyKeyboardMarkup([
                                   ['Skill1', 'Skill2', '...']
                               ], one_time_keyboard=False))

# Career qualification + Basic Training

career = Keyboard('🔨 Which *career* do you want to qualify for?',
                  reply_markup=ReplyKeyboardMarkup([
                      ['Skill1', 'Skill2', '...']
                  ], one_time_keyboard=True))

rolling_qualification = Keyboard('🎲 Rolling for *qualification*...')

qualified = Keyboard('✅ You successfully qualified!')

qualified_sequent_career = Keyboard('✅ You qualified! Choose a *Skill* to acquire:',
                                    reply_markup=ReplyKeyboardMarkup([
                                        ['Skill1', 'Skill2', '...']
                                    ], one_time_keyboard=False))

skill_acquired = Keyboard('✨ You acquired *%s!*')

draft_or_drifter = Keyboard(
    '❌ You failed to qualify. Choose to become a *Drifter* or to be *Drafted*:',
    reply_markup=ReplyKeyboardMarkup([['Drifter', 'Draft']], one_time_keyboard=True))

drafted = Keyboard('🔨 You were drafted into *%s*!')

# Survival

rolling_survival = Keyboard('🎲 Rolling for *survival*...')

survival_drugs = Keyboard('🔁 You used drugs last term, rolling for a second *survival* check...')

survival_success = Keyboard('✅ You passed your survival roll!')

survival_death = Keyboard('💀 You failed your survival roll and died during this term. You\'ll need to start over.')

survival_fail = Keyboard('❌ You failed your survival roll!')

characteristics_dmg = Keyboard('Your *characteristics* after being damaged are:' + _ch, reply_markup=ReplyKeyboardRemove())

injury_crisis = Keyboard('🏥 You suffered from an injury crisis, you\'ll die unless you\'ll be able to pay %sCr!')

# Commission and Advancement

rolling_commission = Keyboard('🎲 Rolling for *commission*...')

rolling_advancement = Keyboard('🎲 Rolling for *advancement*...')

promoted = Keyboard('✅ You got promoted to *Rank %s*!')

commission_failed = Keyboard('❌ You failed your commission roll!')

advancement_failed = Keyboard('❌ You failed your advancement roll!')

table_choice = Keyboard('📦 Choose one of the following tables to roll on:',  # TODO dice instead of package?
                        reply_markup=ReplyKeyboardMarkup([
                            ['Personal Development'], ['Service Skills'], ['Specialist Skills'], ['Advanced Education']
                        ], one_time_keyboard=False))

char_increased = Keyboard('✨ Your *%s* increased!')

# Drugs + Aging

ask_drugs = Keyboard(
    '💊 Do you want to use *anagathic drugs* this term?',
    reply_markup=ReplyKeyboardMarkup([['Yes', 'No']]))

aging = Keyboard('⏩ You are now %s years old!')

aging_fail = Keyboard('🦴 Effects of aging show up...')

aging_crisis = Keyboard('🏥 You suffered from an aging crisis, you\'ll die unless you\'ll be able to pay %sCr!')

stop_drugs = Keyboard('🦴 The shock hits you!')

# Re-enlistment

rolling_reenlinstment = Keyboard('🎲 Rolling for *re-enlistment*...')

reenlistment_retire = Keyboard('👴 You are now too old to keep working, you must retire.')

reenlistment_12 = Keyboard('⭐ You are too good and must continue in this career!')

reenlistment_fail = Keyboard('❌ You failed to reenlist!')

ask_retire = Keyboard(
    '✅ You can re-enlist! Do you want to *retire*?',
    reply_markup=ReplyKeyboardMarkup([
        ['Yes', 'No']
    ], one_time_keyboard=True))

continue_career = Keyboard(
    '🔨 Do you want to *continue* with this career?',
    reply_markup=ReplyKeyboardMarkup([
        ['Yes', 'No']
    ], one_time_keyboard=False))

# Benefit

muster_choice = Keyboard(
    '📦 Do you want to roll on Cash or Material Benefits?',
    reply_markup=ReplyKeyboardMarkup([
        ['Cash', 'Material']
    ], one_time_keyboard=True))

credits_gained = Keyboard('💵 You obtained *%sCr*!')

ship_shares = Keyboard('🚀 You obtained *%s ship shares*!')

weapon_benefit = Keyboard('⚔️ You obtained a *%s*!')

adv_society = Keyboard('♦️ You joined the *Adventurer\'s Society*!')

# Debts

undo_damage = Keyboard('✨ You have *%sCr*, do you want to restore a point of damage in the following characteristics?',
                       reply_markup=ReplyKeyboardMarkup([
                           ['Strength - 2000Cr'], ['Dexterity - 1000Cr']
                       ]))

# Final details

character_name = Keyboard('📝 What\'s your name?', reply_markup=ReplyKeyboardRemove())

name_too_long = Keyboard('❌ That name is too long, sorry. Retry.')

character_sex = Keyboard('📝 What\'s your sex?', reply_markup=ReplyKeyboardMarkup([['M', 'F']]))

buy_equip = Keyboard('💰 You have *%sCr*, do you want to buy something?',
                     reply_markup=ReplyKeyboardMarkup([
                         ['A', 'B', '...', 'No']
                     ], one_time_keyboard=True))

creation = Keyboard('⚔ Do you want to buy something?',
                    reply_markup=ReplyKeyboardMarkup([
                        ['Yes', 'No']
                    ], one_time_keyboard=True))
