from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

from keyboards.keyboards import Keyboard

characteristics = Keyboard(
    'STR: %s\n'
    'END: %s\n'
    'DEX: %s\n'
    'INT: %s\n'
    'EDU: %s\n'
    'SOC: %s', reply_markup=ReplyKeyboardRemove())

world = Keyboard('Choose your homeworld from %s.')

ask_min = Keyboard('Choose the Minimum desired %s',
                   reply_markup=ReplyKeyboardMarkup([
                       ['0', '1', '...', 'Ignore']
                   ], one_time_keyboard=True))

ask_max = Keyboard('Choose the Maximum desired %s',
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

ask_education_skill = Keyboard('Choose an Education skill',
                               reply_markup=ReplyKeyboardMarkup([
                                   ['Skill1', 'Skill2', '...']
                               ], one_time_keyboard=False))


choose_skill = Keyboard('Choose your next skill (skill left to choose: %s)',
                        reply_markup=ReplyKeyboardMarkup([
                            ['Skill1', 'Skill2', '...']
                        ], one_time_keyboard=True))

career = Keyboard('Choose the career you want to qualify for',
                  reply_markup=ReplyKeyboardMarkup([
                      ['Skill1', 'Skill2', '...']
                  ], one_time_keyboard=True))

draft_or_drifter = Keyboard('You failed to qualify. Choose to become a Drifter or to be Drafted.',
                            reply_markup=ReplyKeyboardMarkup([
                                ['Drifter', 'Draft']
                            ], one_time_keyboard=True))

draft = Keyboard('You were drafted into %s', )

qualified = Keyboard('You qualified to rank 0 and got the sequent skills: %s')

promotion = Keyboard('You got promoted to rank %s')

qualified_sequent_career = Keyboard('You qualified, choose a skill to gain',
                                    reply_markup=ReplyKeyboardMarkup([
                                        ['Skill1', 'Skill2', '...']
                                    ], one_time_keyboard=True))

aging = Keyboard('You are now %s')

roll_age = Keyboard('You are now %s and the age %s')

reenlistment_12 = Keyboard('You are too good and must continue in this career')

reenlistment_fail = Keyboard('You failed to reenlist')

survival_death = Keyboard('You died during this term. Start over.')

survival_fail = Keyboard('You failed your survival and %s')

debt = Keyboard('During your career you got in debt and now you paid %s')

negative_number = Keyboard('You are in debt of %s credits')

table_choice = Keyboard('You got promoted to Rank %s! On which Table do you want to roll?',
                        reply_markup=ReplyKeyboardMarkup([
                            ['Personal Development', 'Service Skills', 'Specialist Skills', 'Advanced Education']
                        ], one_time_keyboard=True))

table_choice_no_promo = Keyboard('On which Table do you want to roll?',
                                 reply_markup=ReplyKeyboardMarkup([
                                     ['Personal Development', 'Service Skills', 'Specialist Skills',
                                      'Advanced Education']
                                 ], one_time_keyboard=True))

retire = Keyboard('Do you want to retire?',
                  reply_markup=ReplyKeyboardMarkup([
                      ['Yes', 'No']
                  ], one_time_keyboard=True))

change_career = Keyboard('Do you want to change career?',
                         reply_markup=ReplyKeyboardMarkup([
                             ['Yes', 'No']
                         ], one_time_keyboard=True))

muster_choice = Keyboard('Do you want to roll on Money or MaterialBenefits?',
                         reply_markup=ReplyKeyboardMarkup([
                             ['Money', 'MaterialBenefits']
                         ], one_time_keyboard=True))

character_name = Keyboard('What\'s your name?')

buy_equip = Keyboard('You have %s credits, do you want to buy something?',
                     reply_markup=ReplyKeyboardMarkup([
                         ['A', 'B', '...', 'No']
                     ], one_time_keyboard=True))
