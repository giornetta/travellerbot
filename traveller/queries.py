import json
from typing import List, Tuple

from psycopg2.extensions import cursor

from travellermap import api
import traveller.equipment as eq


def info_world(cur: cursor, adv_id: str) -> str:
    cur.execute('SELECT planet, sector FROM adventures WHERE id = %s;', (adv_id,))
    world, sector = cur.fetchone()
    with open('data/map.json') as d:
        data = json.load(d)
        for planet in data[sector]:
            if planet[0] == world:
                uwp = planet[1]
                break
    return 'Name: ' + world + \
           '\nStarport: ' + uwp[0] + \
           '\nWorld Size: ' + uwp[1] + \
           '\nAtmosphere: ' + uwp[2] + \
           '\nHydrographics: ' + uwp[3] + \
           '\nPopulation: ' + uwp[4] + \
           '\nGovernment: ' + uwp[5] + \
           '\nLaw level: ' + uwp[6] + \
           '\nTechnology level: ' + uwp[8]


def info_adventure(cur: cursor, adv_id: str) -> str:
    cur.execute('SELECT id,title,sector,planet,max_terms,survival_fail_kills '
                'FROM adventures WHERE id = %s;'
                , (adv_id,))
    id, title, sector, world, max_terms, survival_fail_kills = cur.fetchone()
    text = 'Code: ' + id + \
           '\nTitle: ' + title + \
           '\nSector: ' + sector + \
           '\nWorld: ' + world + \
           '\nMax terms: ' + str(max_terms) + \
           '\nFailing a survival roll ' + \
           ('kills' if survival_fail_kills else 'doesn\'t kill') + \
           '\nAdventurers:'
    cur.execute('SELECT char_name FROM characters WHERE adventure_id=%s AND alive = TRUE;',
                (adv_id,))
    names = cur.fetchall()
    for name in names:
        text = text + '\n' + name[0]
    return text


def info_map(cur: cursor, adv_id: str) -> str:
    cur.execute('SELECT sector,planet FROM adventures WHERE id = %s;', (adv_id,))
    sector, world_name = cur.fetchone()
    world = api.world(sector, world_name)
    return f'https://travellermap.com/api/jumpmap?sector={sector.replace(" ", "%20")}&hex={world.hexc}'


def remove_item(cur: cursor, value: int, char_id: int, e: int):
    cur.execute('UPDATE inventories '
                'SET amount = amount - %s '
                'WHERE character_id=%s AND equipment_id =%s '
                'RETURNING amount',
                (value, char_id, e))
    amount = cur.fetchone()
    if amount and amount[0] == 0:
        cur.execute('DELETE FROM inventories WHERE character_id=%s AND equipment_id =%s',
                    (char_id, e))


def info_character(cur: cursor, adv_id: str, name: str) -> str:
    cur.execute('SELECT id,sex, age, strength, dexterity, endurance, '
                'intelligence, education, social_standing, '
                'str_mod, dex_mod, end_mod, int_mod, edu_mod, soc_mod, credits, '
                'equipped_armor, drawn_weapon, stance, rads, wounded, fatigued, stims_taken '
                'FROM characters WHERE char_name = %s AND adventure_id = %s;', (name, adv_id))
    player_info = cur.fetchone()
    if not player_info:
        return 'No one has this name'
    character_id, sex, age, strength, dexterity, endurance, intelligence, education, social_standing, \
    str_mod, dex_mod, end_mod, int_mod, edu_mod, soc_mod, credits_holded, \
    equipped_armor, drawn_weapon, stance, rads, wounded, fatigued, stims_taken = player_info
    stance_mod = ['Prone', 'Crouched', 'Standing']
    cur.execute('SELECT equipment_id, amount FROM inventories '
                'WHERE character_id = %s;', (character_id,))
    inventory = cur.fetchall()
    text = f'Name: {name}\nSex: {sex}\nAge:{age}' \
           f'\nCharacteristics:{strength},{dexterity},{endurance},' \
           f'{intelligence},{education},{social_standing}' \
           f'\nModifiers: {str_mod},{dex_mod},{end_mod},{int_mod},{edu_mod},{soc_mod}' \
           f'\nCredits: {credits_holded}' \
           f'\nStance: {stance_mod[stance]}' \
           f'\nRads: {rads}' \
           f'\nWounded: {wounded}' \
           f'\nFatigued: {fatigued}'
    if equipped_armor:
        text = text + f'\nEquipped armor: {eq.equipments[equipped_armor].name}'
    if drawn_weapon:
        text = text + f'\nDrawn weapon: {eq.equipments[drawn_weapon].name}'
    text = text + f'\nInventory:'
    for eq_id in inventory:
        text = text + '\n'
        text = text + eq.equipments[eq_id[0]].name
        if is_coherent('Computer', eq_id[0]) or is_coherent('Software', eq_id[0]):
            level = eq.equipments[eq_id[0]].technology_level
            text = text + f'LVL{level}'
        text = text + ': '
        text = text + str(eq_id[1])
    return text


def get_items(cur: cursor, adv_id, user_id) -> List[str]:
    cur.execute('SELECT id FROM characters WHERE alive=TRUE AND adventure_id = %s AND user_id = %s',
                (adv_id, user_id))
    character_id = cur.fetchone()[0]
    cur.execute('SELECT equipment_id FROM inventories '
                'WHERE character_id = %s;', (character_id,))
    inventory = cur.fetchall()
    items = []
    for eq_id in inventory:
        item_name = eq.equipments[eq_id[0]].name
        if is_coherent('Armor', eq_id[0]):
            item_name = f'Armor:{item_name}'
        elif is_coherent('Communicator', eq_id[0]):
            item_name = f'Communicator:{item_name}'
        elif is_coherent('Drug', eq_id[0]):
            item_name = f'Drug:{item_name}'
        elif is_coherent('Explosive', eq_id[0]):
            item_name = f'Explosive:{item_name}'
        elif is_coherent('PersonalDevice', eq_id[0]):
            item_name = f'PersonalDevice:{item_name}'
        elif is_coherent('SensoryAid', eq_id[0]):
            item_name = f'SensoryAid:{item_name}'
        elif is_coherent('Shelter', eq_id[0]):
            item_name = f'Shelter:{item_name}'
        elif is_coherent('SurvivalEquipment', eq_id[0]):
            item_name = f'SurvivalEquipment:{item_name}'
        elif is_coherent('Tool', eq_id[0]):
            item_name = f'Tool:{item_name}'
        elif is_coherent('MeleeWeapon', eq_id[0]):
            item_name = f'MeleeWeapon:{item_name}'
        elif is_coherent('RangedWeapon', eq_id[0]):
            item_name = f'RangedWeapon:{item_name}'
        elif is_coherent('RangedAmmunition', eq_id[0]):
            item_name = f'RangedAmmunition:{item_name}'
        elif is_coherent('WeaponAccessory', eq_id[0]):
            item_name = f'WeaponAccessory:{item_name}'
        elif is_coherent('Grenade', eq_id[0]):
            item_name = f'Grenade:{item_name}'
        elif is_coherent('HeavyWeapon', eq_id[0]):
            item_name = f'HeavyWeapon:{item_name}'
        elif is_coherent('HeavyWeaponAmmunition', eq_id[0]):
            item_name = f'HeavyWeaponAmmunition:{item_name}'
        elif is_coherent('Computer', eq_id[0]):
            level = eq.equipments[eq_id[0]].technology_level
            item_name = f'Computer:{item_name}:{level}'
        elif is_coherent('Software', eq_id[0]):
            level = eq.equipments[eq_id[0]].technology_level
            item_name = f'Software:{item_name}:{level}'
        items.append([item_name])
    items.append(['Nothing'])
    return items


def is_item(name: str) -> Tuple[bool, int]:
    flag = False
    splitted = name.split(':', 3)
    if len(splitted) == 1:
        return False, -1
    c = splitted[0].upper()
    eq_name = splitted[1].upper()
    if c == 'COMPUTER' or c == 'SOFTWARE':
        level = int(splitted[2])
        for e in eq.equipments:
            if eq.equipments[e].name.replace(" ", "").upper() == eq_name \
                    and eq.equipments[e].technology_level == level:
                flag = True
                break
        if not flag:
            return False, -1
    else:
        for e in eq.equipments:
            if is_coherent(c, e):
                if eq_name.upper() == eq.equipments[e].name.replace(" ", "").upper():
                    flag = True
                    break
        if not flag:
            return False, -1
    return True, e


def is_coherent(c: str, i: int) -> bool:
    e = eq.equipments[i]
    return c.upper() == 'Armor'.upper() and isinstance(e, eq.Armor) or \
           c.upper() == "Communicator".upper() and isinstance(e, eq.Communicator) or \
           c.upper() == "Computer".upper() and isinstance(e, eq.Computer) or \
           c.upper() == "Software".upper() and isinstance(e, eq.Software) or \
           c.upper() == "Drug".upper() and isinstance(e, eq.Drug) or \
           c.upper() == "Explosive".upper() and isinstance(e, eq.Explosive) or \
           c.upper() == "PersonalDevice".upper() and isinstance(e, eq.PersonalDevice) or \
           c.upper() == "SensoryAid".upper() and isinstance(e, eq.SensoryAid) or \
           c.upper() == "Shelter".upper() and isinstance(e, eq.Shelter) or \
           c.upper() == "SurvivalEquipment".upper() and isinstance(e, eq.SurvivalEquipment) or \
           c.upper() == "Tool".upper() and isinstance(e, eq.Tool) or \
           c.upper() == "MeleeWeapon".upper() and isinstance(e, eq.MeleeWeapon) or \
           c.upper() == "RangedWeapon".upper() and isinstance(e, eq.RangedWeapon) or \
           c.upper() == "RangedAmmunition".upper() and isinstance(e, eq.RangedAmmunition) or \
           c.upper() == "WeaponAccessory".upper() and isinstance(e, eq.WeaponAccessory) or \
           c.upper() == "Grenade".upper() and isinstance(e, eq.Grenade) or \
           c.upper() == "HeavyWeapon".upper() and isinstance(e, eq.HeavyWeapon) or \
           c.upper() == "HeavyWeaponAmmunition".upper() and isinstance(e, eq.HeavyWeaponAmmunition)
