# Personal Combat Process

Our implementation of Personal Combat in Traveller follows a semplified version of *Cepheus Engine SRD* ruleset.

## Checklist

The combat is formed by these elements.

1. **Initiative**
    - The Referee choose the character that are awere of the opponent. The inititive roll of this character is considered `12`.
    - All remaning character roll 2D6 for the initiative roll.
    - If a character has the Tactics Skill can make a Skill Check and add the resulting effect to the character's initiative of his unit.
    - To compute the initiative use initiative roll `+ DEX` (if present add the result of the Tactics Skill Check).
    - The order of action is determined by sorting in descending order. In case of tie the character with the grater `DEX` go first. If there are still tie the first is choosen randomly.
2. **Combact Round**
    - Each round is 6 seconds long.
    - The character can make one minor action and one significant action (optionally can make 2 minor action instead of the significant one).
        - Alternativly you can skip or delay your turn.
3. **Minor Action**
    - The possible Minor Action are:
        - Aiming
        - Aiming for the kill
        - Changing Stance
        - Drawing & Preload
        - Movement
        - Miscellaneous
4. **Significant Action**
    - The possible Significant Action are:
        - Two Minor Action
        - Attack
        - Coup de Grace
        - Miscellaneous
5. **Reactions**
    - When attacked you can react by:
        - Dodging
        - Parrying
6. **Other Actions**
    - Other action are possible, but are left to the Referee discretion.


## Telegram Bot Interaction

This is an example conversation an user might have with the bot during Personal Combat, broken down into the phases described in the Checklist:

### **1. Initiative**

*Referee chat:*

```
> /startCombat
$ Witch chraracter are awere of the opponent?
InlineKeyboard[PlayerName1, PlayerName2, ..., Enemy1, Enemy2, ..., All, X]
$ What's the starting range (meter)?
> 5
```

*Player with Tactics chat:*

```
$ Do you want to make a Tactics Check?
ReplyKeyboard[Yes, No]
$ You succeded!
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

### **3. Minor Action**

If the player choose to do a Minor Action:

*Bob's chat:*

```
$ Choose Minor Action:
ReplyKeyboard[Aiming, Aiming for the kill, Changing Stance, Drawing or Preload, Movement, Miscellaneous, <-]
```

### **4. Significant Action**

If the player choose to do a Significant Action:

*Bob's chat:*

```
$ Choose Minor Action:
ReplyKeyboard[Two Minor Action, Attack, Coup de Grace, Miscellaneous, <-]
```

### **5. Reactions**

If the player is the target of an attack:

*Bob's chat:*

```
$ You are being attacked:
ReplyKeyboard[Dodge, Parry, Do noting]
```

## Semplifcation Assumption

1. You cannot interrupt another round during combat when delaying your turn.
2. Drugs cannot be taken during combat.
3. Combat drug lasts one combat.
4. Combat field is considered to be on a one-dimensional line.
5. At the start of combat all player are considered in the same position as well of all the enemies.
