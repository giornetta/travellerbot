from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

from keyboards.keyboards import FKeyboard, Keyboard

world = FKeyboard('Your stats are:\n "%s","%s","%s","%s","%s","%s"\nDo you want to choose a starting Homeworld '
                  'or do you want to generate one randomly?',
                  reply_markup=ReplyKeyboardMarkup([
                      ['Generate Random', 'Let me choose', 'Search for a world']
                  ], one_time_keyboard=True))

world_name = Keyboard('What\'s the name of your Homeworld?',
                      reply_markup=ReplyKeyboardRemove())

confirm_world = FKeyboard('Will your Homeworld be "%s"?',
                          reply_markup=ReplyKeyboardMarkup([
                              ['Accept', 'Generate another', 'Let me choose']
                          ], one_time_keyboard=True))

no_world = Keyboard('No such world exists in this universe.',
                    reply_markup=ReplyKeyboardMarkup([
                        ['Choose another', 'Generate Random']
                    ], one_time_keyboard=True))

ask_min = FKeyboard('Choose the Minimum desired "%s"',
                    reply_markup=ReplyKeyboardMarkup([
                        ['0', '1', '...', 'Ignore']  # TODO generate range
                    ], one_time_keyboard=True))

ask_max = FKeyboard('Choose the Maximum desired "%s"',
                    reply_markup=ReplyKeyboardMarkup([
                        ['0', '1', '...', 'Ignore']  # TODO generate range
                    ], one_time_keyboard=True))

choose_world = FKeyboard('These are the available Worlds on "%s" that match your criteria!',
                         reply_markup=ReplyKeyboardMarkup([
                             ['A', 'B', '...']  # TODO generate world
                         ], one_time_keyboard=True))

first_homeworld_skill = Keyboard('Choose your Homeworld skill',
                                 reply_markup=ReplyKeyboardMarkup([
                                     ['Skill1', 'Skill2', '...']  # TODO autogenerate skills
                                 ], one_time_keyboard=True))

second_homeworld_skill = Keyboard('Choose your last Homeworld skill',
                                  reply_markup=ReplyKeyboardMarkup([
                                      ['Skill1', 'Skill2', '...']  # TODO autogenerate skills
                                  ], one_time_keyboard=True))

choose_skill = FKeyboard('Choose your next skill (skill left to choose: "%s")',
                         reply_markup=ReplyKeyboardMarkup([
                             ['Skill1', 'Skill2', '...']  # TODO autogenerate skills
                         ], one_time_keyboard=True))

career = Keyboard('Choose the career you want to qualify for',
                  reply_markup=ReplyKeyboardMarkup([
                      ['Skill1', 'Skill2', '...']  # TODO generate careers?
                  ], one_time_keyboard=True))

draft_or_driften = Keyboard('You failed to qualify. Choose to become a Drifter or to be Drafted.',
                            reply_markup=ReplyKeyboardMarkup([
                                ['Drifter', 'Draft']
                            ], one_time_keyboard=True))

draft = FKeyboard('You were drafted into "%s"', )

survival_death = Keyboard('You died during this term. Start over.'
                          'Your stats are:\n "%s","%s","%s","%s","%s","%s"\nDo you want to choose a starting Homeworld '
                          'or do you want to generate one randomly?',
                          reply_markup=ReplyKeyboardMarkup([
                              ['Generate Random', 'Let me choose', 'Search for a world']
                          ], one_time_keyboard=True))

table_choice = FKeyboard('You got promoted to Rank "%s"! On which Table do you want to roll?',
                         reply_markup=ReplyKeyboardMarkup([
                             ['Personal Development', 'Service Skills', 'Specialist Skills', 'Advanced Education']
                         ], one_time_keyboard=True))

table_choice_no_promo = FKeyboard('On which Table do you want to roll?',
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

buy_equip = FKeyboard('You have "%s" credits, do you want to buy something?',
                      reply_markup=ReplyKeyboardMarkup([
                          ['A', 'B', '...', 'No']
                      ], one_time_keyboard=True))
