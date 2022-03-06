# Personal Combat Process

Our implementation of Personal Combat in Traveller follows a simplified version of *Cepheus Engine SRD* ruleset.

## Simplification Assumption

1. You cannot interrupt another round during combat when delaying your turn.
2. Drugs cannot be taken during combat.
3. Combat drug lasts one combat.
4. Combat field is considered to be on a one-dimensional line.
5. At the start of combat all player are considered in the same position as well of all the enemies.
6. To take an "Other Action" the player has to tell what he wants to do to the Referee and wait the Referee’s actions. When the Referee finish he can press the *Skip* button.

## Checklist

The combat is formed by these elements.

1. **Initiative**
    - The Referee choose the character that are aware of the opponent. The initiative roll of this character is considered `12`.
    - All remaining character roll 2D6 for the initiative roll.
    - If a character has the Tactics Skill can make a Skill Check and add the resulting effect to the character's initiative of his unit.
    - To compute the initiative, use initiative roll `+ DEX` (if present add the result of the Tactics Skill Check).
    - The order of action is determined by sorting in descending order. In case of tie the character with the grater `DEX` go first. If there are still tie the first is chosen randomly.
2. **Combat Round**
    - The character can make one minor action and one significant action (optionally can make 2 minor actions instead of the significant one).
        - Alternatively, you can skip or delay your turn.
3. **Minor Action**
    - The possible Minor Action are:
        - *Aiming*: select a target and gain `+1 DM` to the next attack on that target as long you do nothing other than the Minor Action *Aiming*. This action can be repeated to gain more bonus up to `+6 DM`.
        - *Aiming for the kill*: select a target and gain `+2` damage on the next attack to that target as long you do nothing other than the Minor Action *Aiming for the kill*. This action can be repeated to gain more bonus up to `+6` damage.
        - *Changing Stance*: change your stance to any one of thes stances: *prone, crouched or standing*.
        - *Drawing & Reload*: depending on the specific weapon the number of Minor Action required to draw or reload varies. Typically, those action last one Minor Action.
        - *Movement*: you can usually move up to 6 meters, but stance, carrying weight, gravity and terrains can alter this value.
        - *Miscellaneous*: you can do a skill check or a **Other Actions**.
4. **Significant Action**
    - The possible Significant Action are:
        - Two Minor Action
        - Attack: based on your drawn and loaded weapon you can choose and attack a target in range.
        - Coup de Grace: you can attack a helpless adjacent opponent. The attack cannot fail and the target automatically dies.
        - Miscellaneous: you can do a skill check or a **Other Actions**.
5. **Reactions**
    - When attacked you can react, you receive `-2` to your initiative. You can react by:
        - Dodging: when attacked you can dodge, your attacker receive a `-1 DM` (`-2 DM` if he is in cover) to his attack roll. You receives a `-1 DM` to all your skill check until the end of your next turn.
        - Parrying: when attacked melee you can patty, your attacker receives a negative `DM` equal to your *Melee* skill. You receive a `-1 DM` to all your skill check until the end of your next turn.
6. **Other Actions**
    - Other action are possible, but are left to the Referee discretion.


## Telegram Bot Interaction

This is an example conversation a user might have with the bot during Personal Combat, broken down into the phases described in the Checklist:

### **1. Initiative**

*Referee chat:*

```
> /startCombat
$ Witch character are aware of the opponent?
InlineKeyboard[PlayerName1, PlayerName2, ..., Enemy1, Enemy2, ..., All, X]
$ What's the starting range (meter)?
> 5
```

*Player with Tactics chat:*

```
$ Do you want to make a Tactics Check?
ReplyKeyboard[Yes, No]
$ You succeeded!
```

*Referee chat:*

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
$ Is Bob's turn.
``` 

*Bob's chat:*

```
$ Is your turn. What do you want to do?
ReplyKeyboard[Minor Action, Significant Action, Skip, Delay]
```

#### **If you delayed your action**

Before each other character turn you receive a notification.

```
$ Do you want to take your turn before Alice?
ReplyKeyboard[Yes, No]
```

### **3. Minor Action**

If the player chooses to do a Minor Action:

*Bob's chat:*

```
$ Choose Minor Action:
ReplyKeyboard[Aiming, Aiming for the kill, Changing Stance, Drawing or Reload, Movement, Miscellaneous, <-]
```

#### **Minor Action: Aiming or Aiming for the kill**

```
$ Choose Target:
ReplyKeyboard[PlayerName1, PlayerName2, ..., Enemy1, Enemy2, ..., <-]
```

#### **Minor Action: Changing Stance**

```
$ Choose your next stance:
ReplyKeyboard[prone, crouched, <-]
```

#### **Minor Action: Drawing**

```
$ Choose the weapon to draw:
ReplyKeyboard[sword, rifle, <-]
```

#### **Minor Action: Movement**

```
$ Choose your next stance:
ReplyKeyboard[forward, back, <-]
```

#### **Minor Action: Miscellaneous**

*Bob's chat*

```
ReplyKeyboard[Skill Check, Other, <-]
ReplyKeyboard[Skill 1, Skill 2, Skill 3, <-]
```

*Referee's chat*

```
$ Bob wants to make a Survival Skill check
ReplyKeyboard[Allow, Deny]
```

### **4. Significant Action**

If the player chooses to do a Significant Action:

*Bob's chat:*

```
$ Choose Minor Action:
ReplyKeyboard[Two Minor Action, Attack, Coup de Grace, Miscellaneous, <-]
```

#### **Significant Action: Attack**

```
$ Choose Target:
ReplyKeyboard[PlayerName1, PlayerName2, ..., Enemy1, Enemy2, ..., <-]
```

#### **Significant Action: Coup de Grace**

```
$ Choose Target:
ReplyKeyboard[PlayerName1, PlayerName2, ..., Enemy1, Enemy2, ..., <-]
```

#### **Significant Action: Miscellaneous**

*Bob's chat*

```
ReplyKeyboard[Skill Check, Other, <-]
ReplyKeyboard[Skill 1, Skill 2, Skill 3, <-]
```

*Referee's chat*

```
$ Bob wants to make a Survival Skill check
ReplyKeyboard[Allow, Deny]
```

### **5. Reactions**

If the player is the target of an attack:

*Bob's chat:*

```
$ You are being attacked:
ReplyKeyboard[Dodge, Parry, Do noting]
```

### **6. After being hit**

When the player takes damage, the damage value is subtracted from Endurance.

```
$ You took 5 damage:
    STR: 7
    DEX: 9
    END: 2
```

When the player takes damage and his *Endurance* is already reduced to 0, he can choose were to take the next damage:

```
$ You took 5 damage, were do you want to take damage?
ReplyKeyboard[Strength, Dexterity]
```
