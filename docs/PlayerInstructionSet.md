# Player Instruction Set

This document describes all the possible actions that players can take when they're out of combat. Combat actions are described in [the Personal Combat documentation](PersonalCombatProcess.md).

- *Character Info*: shows information about the status of the character, their characteristics and Credits.
- *Inventory*: lists all the items in the player's inventory.
    - *Equip/Unequip*: if the equipment is an Armor, the player will be able to equip or unequip it.
    - *Use*: if the equipment is a usable or consumable item, the player will be able to use or consume it.
    - *Throw*: the player can throw any equipment they have in their inventory.
- *Map*: shows information about the world the character is currently in and shares a map of the nearby worlds that the party can travel to.
- *Skills*: shows a list of all the available skills, ordered by their Level. The player can select any of them to perform a skill check. These are better described in [the Skills documentation](Skills.md).
- *Shop*: only if a shop is open, the player will be able to buy new equipments with their Credits. Which items are available in the Shop are determined by the Referee.

## Bot Interaction

### Character Info

The bot will provide the player with a description of their character, following a slim version of the standard described in *Cepheus Engine SRD*:

```
> ReplyKeyboard[Character Info, ...]
$ {Rank/Noble Title} {Name}, Age {Age}
  [...{Career.Name} ({Career.Terms} terms)], Cr {Credits}
  STR: 8
  DEX: 10
  END: 7
  INT: 8
  EDU: 10
  SOC: 10
```

### Inventory

Each item will have an `InlineKeyboard` attached to it that will allow the player to interact with their equipments.

```
> ReplyKeyboard[..., Inventory, ...]
$ Here's your inventory!
$ Ablat
> InlineKeyboard[Equip, Throw]
$ Mesh
> InlineKeyboard[Unequip, Throw]
$ Combat Drug x3
> InlineKeyboard[Use, Throw]
...
```

```
> InlineKeyboard[Equip, Throw]
$ Successfully equipped Ablat!
```

### Map

This will show World's information in UWP format, and an image of the surroundings from the [Traveller Map API](https://travellermap.com).

```
> ReplyKeyboard[..., Map, ...]
$ Loki (Solomani Rim): C9CA369-C
$ {Image}
```

### Skills

The players will be able to perform skill checks as follows:

```
> ReplyKeyboard[..., Skills, ...]
$ Choose a skill:
> ReplyKeyboard[Athletics, Agent, ...]
$ Choose the difficulty of the skill check:
> ReplyKeyboard[Routine, Average, Difficult, Very Difficult, Formidable]
```

Further interactions, if present, are described in [the Skills documentation](Skills.md).

### Shop

The players will be able to navigate the shop filtering out items by their category.

```
> ReplyKeyboard[..., Shop]
$ Choose a category:
> ReplyKeyboard[Armor, Communicators, Weapons, ..., <-]
$ Pick any item to buy:
> ReplyKeyboard[Ablat - 75Cr, Mesh - 150Cr, ..., <-]
$ Bought Ablat for 75Cr!
$ Pick any item to buy:
> ReplyKeyboard[Ablat - 75Cr, Mesh - 150Cr, ..., <-]
$ You don't have enough Credits to buy Mesh.
```