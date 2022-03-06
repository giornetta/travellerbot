# Personal Combat Process

Our implementation of Personal Combat in Traveller follows a simplified version of the *Cepheus Engine SRD* ruleset.

## Simplification Assumptions

1. You cannot interrupt another round during combat when delaying your turn.
2. Drugs cannot be taken during combat.
3. Combat drug lasts one combat.
4. Combat field is considered to be on a one-dimensional line.
5. At the start of combat all players are considered to be in the same position, and the same applies for enemies.
6. A player can perform an action that isn't specified in the action lists by communicating his intentions to the Referee. They then have to wait for the Referee to take any necessary action, and only afterwards they may press the *Other* button.

## Checklist

The combat is formed by these elements.

1. **Initiative**
    - The Referee chooses which characters are aware of their opponent. The initiative roll of these characters is considered to be `12`.
    - All remaining characters roll 2D6 for the initiative roll.
    - If a character has the Tactics skill they can make a Skill Check and add the resulting effect to the initiative of their allies.
    - To compute the initiative, use initiative roll + DEX (if present add the result of the Tactics Skill Check).
    - The order of action is determined by sorting in descending order. In case of a tie the character with higher DEX goes first. If there are still ties, their order is chosen randomly.
2. **Combat Round**
    - Each character can make one minor action and one significant action (they can optionally make two minor actions instead of the significant one).
        - Alternatively, you can skip or delay your turn.
3. **Minor Action**
    - The possible Minor Actions are:
        - *Aiming*: select a target and gain `+1 DM` to the next attack on that target as long you do nothing other than the Minor Action *Aiming*. This action can be repeated to gain more bonus up to `+6 DM`.
        - *Aiming for the kill*: select a target and gain `+2` damage on the next attack to that target as long you do nothing other than the Minor Action *Aiming for the kill*. This action can be repeated to gain more bonus up to `+6` damage.
        - *Changing Stance*: change your stance to any one of these stances: *Prone, Crouched or Standing*.
        - *Drawing & Reloading*: depending on the specific weapon the number of Minor Actions required to draw or reload varies. Typically, these actions only take one Minor Action.
        - *Movement*: you can usually move up to 6 meters, but stance, carrying weight, gravity and terrains can alter this value.
        - *Miscellaneous*: you can do a *Skill Check* or *Other*.
4. **Significant Action**
    - The possible Significant Actions are:
        - Two Minor Actions
        - *Attack*: based on your drawn and loaded weapon you can choose and attack a target in range.
        - *Coup de Grace*: you can attack a helpless adjacent opponent. The attack cannot fail and the target automatically dies.
        - *Miscellaneous*: you can do a *Skill Check* or *Other*.
5. **Reactions**
    - When attacked you can react, but you receive `-2` to your initiative if you choose to do so. You can react by:
        - *Dodging*: when attacked you can dodge, your attacker receive a `-1 DM` (`-2 DM` if he is in cover) to his attack roll. You receive a `-1 DM` to all your skill checks until the end of your next turn.
        - *Parrying*: when attacked melee you can parry, your attacker receives a negative `DM` equal to your *Melee* skill. You receive a `-1 DM` to all your skill checks until the end of your next turn.

## Telegram Bot Interaction

This is an example conversation a user might have with the bot during Personal Combat, broken down into the phases described in the Checklist:

### **1. Initiative**

*Referee chat:*

```
> /startCombat
$ Which characters are aware of their opponents?
> InlineKeyboard[PlayerName1, PlayerName2, ..., Enemy1, Enemy2, ..., All, X]
$ What's the starting range (meters)?
> 5
```

*Player with Tactics' chat:*

```
$ Do you want to make a Tactics Check?
> ReplyKeyboard[Yes, No]
$ You succeeded!
```

*Referee's chat:*

```
$ The current order of action is:
    Character 1 | 16
    Character 2 | 14
    ...
    Character n | 3
```

### **2. Combat Round**

*Everyone's chat:*

```
$ It's Bob's turn.
``` 

*Bob's chat:*

```
$ It's your turn. What do you want to do?
> ReplyKeyboard[Minor Action, Significant Action, Skip, Delay]
```

#### **If you delayed your action**

Before every other character's turn you receive a notification.

```
$ Do you want to take your turn before Alice?
> ReplyKeyboard[Yes, No]
```

### **3. Minor Action**

If the player chooses to do a Minor Action:

*Bob's chat:*

```
$ Choose Minor Action:
> ReplyKeyboard[Aim, Aim for the kill, Change Stance, Draw or Reload, Movement, Skill Check, Other, <-]
```

#### **Minor Action: Aiming or Aiming for the kill**

```
$ Choose Target:
> ReplyKeyboard[PlayerName1, PlayerName2, ..., Enemy1, Enemy2, ..., <-]
```

#### **Minor Action: Changing Stance**

```
$ Choose your next stance:
> ReplyKeyboard[Prone, Crouched, <-]
```

#### **Minor Action: Drawing**

```
$ Choose the weapon to draw:
> ReplyKeyboard[Sword, Rifle, <-]
```

#### **Minor Action: Movement**

```
$ In which direction do you want to move:
> ReplyKeyboard[Forward, Back, <-]
```

#### **Minor Action: Skill Check**

*Bob's chat*

```
$ Choose a skill:
> ReplyKeyboard[Skill 1, Skill 2, Skill 3, <-]
```

### **4. Significant Action**

If the player chooses to do a Significant Action:

*Bob's chat:*

```
$ Choose Minor Action:
> ReplyKeyboard[Two Minor Actions, Attack, Coup de Grace, Skill Check, Other, <-]
```

#### **Significant Action: Attack**

```
$ Choose Target:
> ReplyKeyboard[PlayerName1, PlayerName2, ..., Enemy1, Enemy2, ..., <-]
```

#### **Significant Action: Coup de Grace**

```
$ Choose Target:
> ReplyKeyboard[PlayerName1, PlayerName2, ..., Enemy1, Enemy2, ..., <-]
```

#### **Significant Action: Skill Check**

*Bob's chat*

```
$ Choose a skill:
> ReplyKeyboard[Skill 1, Skill 2, Skill 3, <-]
```

### **5. Reactions**

If the player is the target of an attack:

*Bob's chat:*

```
$ You are being attacked:
> ReplyKeyboard[Dodge, Parry, Do nothing]
```

### **6. After being hit**

When the player takes damage, the damage value is subtracted from Endurance.

```
$ You took 5 damage:
    STR: 7
    DEX: 9
    END: 2
```

When the player takes damage and their Endurance is already 0, they can choose where to take damage next:

```
$ You took 5 damage, which characteristics should be hit?
> ReplyKeyboard[Strength, Dexterity]
```
