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
    return 'š <b>Name</b>: ' + world + \
           '\nšø <b>Starport</b>: ' + uwp[0] + \
           '\nā°ļø <b>World Size</b>: ' + uwp[1] + \
           '\nā <b>Atmosphere</b>: ' + uwp[2] + \
           '\nš <b>Hydrographics</b>: ' + uwp[3] + \
           '\nš« <b>Population</b>: ' + uwp[4] + \
           '\nš³ļø <b>Government</b>: ' + uwp[5] + \
           '\nāļø <b>Law level</b>: ' + uwp[6] + \
           '\nš¤ <b>Technology level</b>: ' + uwp[8]


def info_adventure(cur: cursor, adv_id: str) -> str:
    cur.execute('SELECT id, title, sector, planet, max_terms, survival_fail_kills, vessel '
                'FROM adventures WHERE id = %s;'
                , (adv_id,))
    adv_id, title, sector, world, max_terms, survival_fail_kills, vessel = cur.fetchone()
    text = f'#ļø <b>Code</b>: <code>{adv_id}</code>' + \
           '\nš <b>Title</b>: ' + title + \
           '\nš <b>Sector</b>: ' + sector + \
           '\nšŖ <b>World</b>: ' + world + \
           '\nšØ <b>Max Terms</b>: ' + str(max_terms) + \
           '\nš Failing a <b>Survival Roll</b> ' + \
           ('kills' if survival_fail_kills else 'does not kill') + \
           ('\nš <b>Vessel</b>: ' + vessel if vessel else '') + \
           '\nš§āš <b>Adventurers</b>:'
    cur.execute('SELECT char_name FROM characters WHERE adventure_id=%s AND alive = TRUE;',
                (adv_id,))
    names = cur.fetchall()
    for name in names:
        text = text + '\n- ' + name[0]
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
                'str_mod, dex_mod, end_mod, int_mod, edu_mod, soc_mod, credits, ship_shares, '
                'equipped_armor, drawn_weapon, stance, rads, wounded, fatigued, stims_taken '
                'FROM characters WHERE char_name = %s AND adventure_id = %s;', (name, adv_id))

    player_info = cur.fetchone()
    if not player_info:
        return 'No one has this name'

    character_id, sex, age, strength, dexterity, endurance, intelligence, education, social_standing, \
    str_mod, dex_mod, end_mod, int_mod, edu_mod, soc_mod, credits_held, ship_shares, \
    equipped_armor, drawn_weapon, stance, rads, wounded, fatigued, stims_taken = player_info

    stance_mod = ['Prone', 'Crouched', 'Standing']
    cur.execute('SELECT equipment_id, amount FROM inventories '
                'WHERE character_id = %s;', (character_id,))
    inventory = cur.fetchall()

    text = f'š <b>Name</b>: {name}\nš» <b>Sex</b>: {sex}\nš“ Age: {age}' \
           f'\nšŖ <b>STR</b>: {strength} {"+" if str_mod > 0 else "-" if str_mod != 0 else ""} {abs(str_mod) if str_mod != 0 else ""}' \
           f'\nš <b>END</b>: {endurance} {"+" if end_mod > 0 else "-" if end_mod != 0 else ""} {abs(end_mod) if end_mod != 0 else ""}' \
           f'\nš”ļø <b>DEX</b>: {dexterity} {"+" if dex_mod > 0 else "-" if dex_mod != 0 else ""} {abs(dex_mod) if dex_mod != 0 else ""}' \
           f'\nš§  <b>INT</b>: {intelligence} {"+" if int_mod > 0 else "-" if int_mod != 0 else ""} {abs(int_mod) if int_mod != 0 else ""}' \
           f'\nš <b>EDU</b>: {education} {"+" if edu_mod > 0 else "-" if edu_mod != 0 else ""} {abs(edu_mod) if edu_mod != 0 else ""}' \
           f'\nš <b>SOC</b>: {social_standing} {"+" if soc_mod > 0 else "-" if soc_mod != 0 else ""} {abs(soc_mod) if soc_mod != 0 else ""}' \
           f'\nšµ <b>Credits</b>: {credits_held}' \
           f'\nš <b>Ship shares</b>: {ship_shares}' \
           f'\nš§ <b>Stance</b>: {stance_mod[stance]}' \
           f'\nā¢ļø <b>Rads</b>: {rads}' \
           f'\nš¦“ <b>Wounded</b>: {wounded}' \
           f'\nš¤ <b>Fatigued</b>: {fatigued}'

    if equipped_armor:
        text = text + f'\nš¦ŗ <b>Equipped armor</b>: {eq.equipments[equipped_armor].name}'

    if drawn_weapon:
        text = text + f'\nāļø <b>Drawn weapon</b>: {eq.equipments[drawn_weapon].name}'

    if len(inventory) > 0:
        text = text + f'\nš <b>Inventory</b>:'

    for eq_id in inventory:
        text = text + '\n- ' + eq.equipments[eq_id[0]].name
        if is_coherent('Computer', eq_id[0]) or is_coherent('Software', eq_id[0]):
            level = eq.equipments[eq_id[0]].technology_level
            text = text + f'LVL{level}'
        if is_coherent('Ranged_Ammunition', eq_id[0]):
            text = text + ' Ammo'
        if eq_id[1] > 1:
            text = text + f': x{eq_id[1]}'

    return text


def info_npcs(cur: cursor, scene_id: int) -> str:
    cur.execute('SELECT npc_name, strength, dexterity, endurance, intelligence,'
                ' education, social_standing, career, rank, armor, weapon,'
                ' ally FROM npcs WHERE scene=%s;',
                (scene_id,))
    npcs = cur.fetchall()
    text = 'There are no NPCs in this scene'
    if len(npcs) > 0:
        text = '<b>NPCs</b>:\n'
        for npc in npcs:
            name, strength, dexterity, endurance, intelligence, education, social_standing, carr, rank, armo, weap, ally = npc
            text = text + f'š <b>Name</b>: {name}' \
                          f'\nšŖ <b>STR</b>: {strength} ' \
                          f'\nš <b>END</b>: {endurance} ' \
                          f'\nš”ļø <b>DEX</b>: {dexterity} ' \
                          f'\nš§  <b>INT</b>: {intelligence} ' \
                          f'\nš <b>EDU</b>: {education} ' \
                          f'\nš <b>SOC</b>: {social_standing} ' \
                          f'\nāØ <b>Career</b>: {carr}' \
                          f'\nā¬ <b>Rank</b>: {rank}' \
                          f'\nš¦ŗ <b>Equipped armor</b>: {eq.equipments[armo].name}' \
                          f'\nāļø <b>Drawn weapon</b>: {eq.equipments[weap].name}'
            text = text + ("\nš¢ <b>Ally</b>" if ally else "\nš“ <b>Enemy</b>")
            text = text + '\n\n\n'
    return text


def get_items(cur: cursor, adv_id, user_id) -> List[List[str]]:  # TODO make this a List[str] and use single_keys
    cur.execute('SELECT id FROM characters WHERE alive=TRUE AND adventure_id = %s AND user_id = %s',
                (adv_id, user_id))
    character_id = cur.fetchone()[0]
    cur.execute('SELECT equipment_id FROM inventories '
                'WHERE character_id = %s;', (character_id,))
    inventory = cur.fetchall()
    inventory = [item for t in inventory for item in t]
    items = eq_name_from_id(inventory)
    items.append(['Nothing'])
    return items


def add_item(cur: cursor, char_id: int, value: int, e: int):
    cur.execute('SELECT amount FROM inventories WHERE equipment_id = %s and character_id = %s;', (e, char_id))
    amount = cur.fetchone()
    if amount:
        cur.execute('UPDATE inventories '
                    'SET amount = %s '
                    'WHERE character_id = %s AND equipment_id = %s',
                    (amount[0] + value, char_id, e))
    else:
        cur.execute('INSERT INTO inventories(character_id, equipment_id, amount, damage) '
                    'VALUES(%s, %s, %s, %s);', (char_id, e, value, 0))


def enough_money(cur: cursor, char_id: int, e: int) -> Tuple[bool, int]:
    cur.execute('SELECT credits FROM characters WHERE id = %s', (char_id,))
    credits = cur.fetchone()[0]
    if credits < eq.equipments[e].cost:
        return False, credits
    else:
        cur.execute('UPDATE characters SET credits = credits - %s WHERE id = %s', (eq.equipments[e].cost, char_id))
        return True, credits - eq.equipments[e].cost


def categories_from_shop(cur: cursor, adv_id, user_id) -> List[str]:
    cur.execute('SELECT category FROM shop WHERE adventure_id = %s', (adv_id,))

    categories: List[str] = []
    for t in cur.fetchall():
        categories.append(t[0].title().replace('_', ' '))

    return categories


def eq_name_from_id(ids: List[int]) -> List[List[str]]:
    items = []
    for eq_id in ids:
        item_name = eq.equipments[eq_id].name
        if is_coherent('Ranged_Ammunition', eq_id):
            item_name = f'{item_name}:Ammo'
        elif is_coherent('Heavy_Weapon_Ammunition', eq_id):
            item_name = f'{item_name}:Ammo'
        elif is_coherent('Computer', eq_id):
            level = eq.equipments[eq_id].technology_level
            item_name = f'{item_name}:{level}'
        elif is_coherent('Software', eq_id):
            level = eq.equipments[eq_id].technology_level
            item_name = f'{item_name}:{level}'
        items.append([item_name])
    return items


def is_item(name: str) -> Tuple[bool, int]:
    eq_id: int = -1

    splitted = name.split(':', 2)

    eq_name = splitted[0]
    spec = splitted[1] if len(splitted) > 1 else None
    found = False

    for k, v in eq.equipments.items():
        if spec and spec.isdigit():
            if v.name.replace(" ", "_").upper() == eq_name and v.technology_level == int(spec):
                eq_id = k
                found = True
                break
        elif spec == 'AMMO':
            if v.name.replace(" ", "_").upper() == eq_name and \
                    (isinstance(v, eq.RangedAmmunition) or isinstance(v, eq.HeavyWeaponAmmunition)):
                eq_id = k
                found = True
                break
        else:
            if eq_name == v.name.replace(" ", "_").upper():
                eq_id = k
                found = True
                break
    return found, eq_id


def is_coherent(c: str, i: int) -> bool:
    e = eq.equipments[i]
    c = c.upper()

    return isinstance(e, eq.categories.get(c))
