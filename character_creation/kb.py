from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

from keyboards.keyboards import Keyboard

characteristics = Keyboard(
    'These are your characteristics:\n'
    'STR: %s\n'
    'END: %s\n'
    'DEX: %s\n'
    'INT: %s\n'
    'EDU: %s\n'
    'SOC: %s', reply_markup=ReplyKeyboardRemove())

# Homeworld

world = Keyboard('Choose your homeworld from %s.')

ask_min = Keyboard('Choose the Minimum desired "%s"',
                   reply_markup=ReplyKeyboardMarkup([
                       ['0', '1', '...', 'Ignore']
                   ], one_time_keyboard=True))

ask_max = Keyboard('Choose the Maximum desired "%s"',
                   reply_markup=ReplyKeyboardMarkup([
                       ['0', '1', '...', 'Ignore']
                   ], one_time_keyboard=True))

choose_world = Keyboard('These are the available Worlds on %s that match your criteria!',
                        reply_markup=ReplyKeyboardMarkup([
                            ['A', 'B', '...']
                        ], one_time_keyboard=False))

no_world_found = Keyboard('No such world satisfies the filters',
                          reply_markup=ReplyKeyboardMarkup([
                              ['Let me choose', 'Generate Random', 'Search again']
                          ], one_time_keyboard=True))

ask_homeworld_skill = Keyboard('Choose a Homeworld skill',
                               reply_markup=ReplyKeyboardMarkup([
                                   ['Skill1', 'Skill2', '...']
                               ], one_time_keyboard=False))

creation = Keyboard('Are you ready to start your adventure?',
                    reply_markup=ReplyKeyboardMarkup([
                        ['Yes!', 'Of course!', 'Sure!']
                    ], one_time_keyboard=True))

ask_education_skill = Keyboard('Choose an Education skill',
                               reply_markup=ReplyKeyboardMarkup([
                                   ['Skill1', 'Skill2', '...']
                               ], one_time_keyboard=False))

# Career

# choose_skill = Keyboard('Choose your next skill (skill left to choose: "%s")',
#                        reply_markup=ReplyKeyboardMarkup([
#                            ['Skill1', 'Skill2', '...']
#                        ], one_time_keyboard=True))

career = Keyboard('Choose the career you want to qualify for',
                  reply_markup=ReplyKeyboardMarkup([
                      ['Skill1', 'Skill2', '...']
                  ], one_time_keyboard=True))

draft_or_drifter = Keyboard('You failed to qualify. Choose to become a Drifter or to be Drafted.',
                            reply_markup=ReplyKeyboardMarkup([
                                ['Drifter', 'Draft']
                            ], one_time_keyboard=True))

drafted = Keyboard('You were drafted into %s', )

qualified = Keyboard('You qualified to rank 0 and got the sequent skills: "%s"')

qualified_sequent_career = Keyboard('You qualified, choose a skill to gain',
                                    reply_markup=ReplyKeyboardMarkup([
                                        ['Skill1', 'Skill2', '...']
                                    ], one_time_keyboard=False))

promotion = Keyboard('You got promoted to rank %s')

skill_acquired = Keyboard('You acquired %s!')

ask_drugs = Keyboard('Do you want to use anagathic drugs this term?', reply_markup=ReplyKeyboardMarkup([['Yes', 'No']]))

stop_drugs = Keyboard('The shock hits you!')

aging = Keyboard('You are now %s')

aging_fail = Keyboard('Effects of aging show up...')

aging_crisis = Keyboard('You suffered from an aging crisis, you\'ll die if you won\'t be able to pay %sCr!')

reenlistment_retire = Keyboard('You are now too old to keep working, you must retire.')

reenlistment_12 = Keyboard('You are too good and must continue in this career')

reenlistment_fail = Keyboard('You failed to reenlist!')

survival_success = Keyboard('You passed your survival roll!')

survival_drugs = Keyboard('You used drugs last term, rolling for a second survival check...')

survival_death = Keyboard('You died during this term. Start over.')

survival_fail = Keyboard('You failed your survival roll!')

injury_crisis = Keyboard('You suffered from an injury crisis, you\'ll die if you won\'t be able to pay %sCr!')

commission_success = Keyboard('You succeeded in your commission roll! You are now Rank 1!')

commission_failed = Keyboard('You failed your commission roll!')

advancement_failed = Keyboard('You failed your advancement roll!')

debt = Keyboard('During your career you got in debt and now you paid "%s"')

negative_number = Keyboard('You are in debt of "%s" credits')

promoted = Keyboard('You got promoted to Rank %s!')

table_choice = Keyboard('On which Table do you want to roll?',
                        reply_markup=ReplyKeyboardMarkup([
                            ['Personal Development', 'Service Skills', 'Specialist Skills',
                             'Advanced Education']
                        ], one_time_keyboard=False))

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
