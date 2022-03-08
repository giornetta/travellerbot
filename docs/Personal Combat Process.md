# Personal Combat Process

Our implementation of Personal Combat in Traveller follows a simplified version of the *Cepheus Engine SRD* ruleset.

## Simplification Assumptions

1. You cannot interrupt another round during combat when delaying your turn.
2. Drugs cannot be taken during combat.
3. Combat drug lasts one combat.
4. Combat field is considered to be on a one-dimensional line.
5. At the start of combat all players are considered to be in the same position, and the same applies for enemies.
6. A player can perform an action that isn't specified in the action lists by communicating his intentions to the Referee. They then have to wait for the Referee to take any necessary action, and only afterwards they may press the *Other* button.
7. Every weapon requires a Minor Action to be drawn or reloaded.
8. The Referee is the one responsible of setting the cover status.
9. Helpless means Unconscious.

## Checklist

The combat is formed by these elements.

1. **Initiative**
    - The Referee chooses which characters are aware of their opponent. The initiative roll of these characters is considered to be `12`.
    - All remaining characters roll 2D6 for the initiative roll.
    - If a character has the Tactics skill they can make a Skill Check and add the resulting effect to the initiative of their allies.
    - To compute the initiative, use initiative roll + DEX (if present add the result of the Tactics Skill Check).
    - The order of action is determined by sorting in descending order. In case of a tie the character with higher DEX goes first. If there are still ties, their order is chosen randomly.
2. **Combat Round**
    - First of all, the bot asks any conscious player who has chosen to delay their turn if they want to intervene following a *FIFO* order.
    - If the player whose turn it is is unconscious, the Referee will be asked if they want to try an Endurance check to wake up the character.
    - If the player whose turn it is is seriously wounded, they lose their minor action and their movement is limited to 1.5 meters.
    - Each character can make one minor action and one significant action (they can optionally make two minor actions instead of the significant one).
        - Alternatively, you can skip or delay your turn.
3. **Minor Action**
    - The possible Minor Actions are:
        - *Aiming*: select a target and gain `+1 DM` to the next attack on that target as long you do nothing other than the Minor Action *Aiming*. This action can be repeated to gain more bonus up to `+6 DM`.
        - *Aiming for the kill*: select a target and gain `+2` damage on the next attack to that target as long you do nothing other than the Minor Action *Aiming for the kill*. This action can be repeated to gain more bonus up to `+6` damage.
        - *Changing Stance*: change your stance to any one of these stances: *Prone, Crouched or Standing*.
        - *Drawing & Reloading*: draw or reload a weapon to attack with.
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
6. **After being hit**
    - When you are hit the damage is subtracted from your *Endurance*. If your *Endurance* is reduced to 0 the damage is subtracted from your *Strength* or *Dexterity* (your choice).
    - When two out of three phisical charateristics are reduced to 0, you become unconscious.
    - If all physical characteristics are reduced to 0, you are killed.
7. **End of Combat**
    - Every player will be asked if they want to perform first aid on an ally or on themselves.
        - Applying first aid restores a number of characteristic points equal to twice the Effect of the Medic check. Points restored by first aid are divided as desired among all damaged physical characteristics.
        - If you perform first aid on yourself to receive a `-2 DM`.
    - If first aid succeded on a seriously wounded character the bot will ask if they want to do a surgery too on the same character.
        -  Surgery restores characteristic points just like first aid but if the check is failed the patient loses characteristic points equal to the Effect.
        - If you perform surgery on yourself to receive a `-4 DM`.

## Telegram Bot Interaction

This is an example conversation a user might have with the bot during Personal Combat, broken down into the phases described in the Checklist:

### **1. Initiative**

*Referee's chat:*

```
> /startCombat
$ Which characters are aware of their opponents?
> InlineKeyboard[PlayerName1, PlayerName2, ..., Enemy1, Enemy2, ..., All, X]
$ What's the starting range (meters)?
> 5
```

Any player who has the Tactics skill will receive a message asking them if they want to try a Skill Check:

```
$ Do you want to make a Tactics Check?
> ReplyKeyboard[Yes, No]
$ You succeeded!
```

After everyone has decided, the Referee will receive the order of action in their chat.

```
$ The current order of action is:
    Character 1 | 16
    Character 2 | 14
    ...
    Character n | 3
```

### **2. Combat Round**

First of all, the bot asks any player who has chosen to delay their turn if they want to intervene following a *FIFO* order.

```
$ Do you want to take your turn before Alice?
> ReplyKeyboard[Yes, No]
```

If any of them accepts, they will act as if it was their turn, otherwise, the bot will ask the next character who will act following the Initiative order.

If the turn should be taken by an unconscious character, the Referee will decide if they're ready to attempt an Endurance check to wake up:

*Referee's chat*
```
$ Bod is unconscious, can they try to wake up?
> ReplyKeyboard[PlayerName1, PlayerName2, ..., Enemy1, Enemy2, ..., <-]☺
$ Bob rolled 9.
```

*Bob's chat*
```
$ You woke up!
```

Afterwards, the character is ready to begin their turn.

*Everyone's chat:*

```
$ It's Bob's turn.
``` 

*Bob's chat:*

```
$ It's your turn. What do you want to do?
> ReplyKeyboard[Minor Action, Significant Action, Skip, Delay]
```

### **3. Minor Action**

```
> ReplyKeyboard[Minor Action, Significant Action]
$ Choose Minor Action:
> ReplyKeyboard[Aim, Aim for the kill, Change Stance, Draw, Reload, Movement, Skill Check, Other, <-]
```

#### **Minor Action: Aiming or Aiming for the kill**

```
$ Choose Target:
> ReplyKeyboard[PlayerName1, PlayerName2, ..., Enemy1, Enemy2, ..., <-]
$ You are aiming at {Target}.
```

#### **Minor Action: Changing Stance**

```
$ Choose your next stance:
> ReplyKeyboard[Prone, Crouched, <-]
$ You switched to Prone.
```

#### **Minor Action: Drawing**

```
$ Choose the weapon to draw:
> ReplyKeyboard[Sword, Rifle, <-]
$ You drew your Sword.
```

#### **Minor Action: Movement**

```
$ In which direction do you want to move:
> ReplyKeyboard[Forward, Back, <-]
$ How much (0m-8m)?
> 5
$ You moved back 5 meters.
```

#### **Minor Action: Skill Check**

```
$ Choose a skill:
> ReplyKeyboard[Skill 1, Skill 2, Skill 3, <-]
```

The interactions that occur after choosing a skill are described in [the Skills documentation](Skills.md).

### **4. Significant Action**

```
> ReplyKeyboard[Minor Action, Significant Action]
$ Choose Significant Action:
> ReplyKeyboard[Two Minor Actions, Attack, Coup de Grace, Skill Check, Other, <-]
```

#### **Significant Action: Attack**

```
$ Choose Target:
> ReplyKeyboard[PlayerName1, PlayerName2, ..., Enemy1, Enemy2, ..., <-]
```

If the target reacts:
```
$ Target dodged, you missed.
```

Finally, the character inflicts damage to the target (if the attack hit):
```
$ You dealt 4 damage.
```

#### **Significant Action: Coup de Grace**

```
$ Choose Target:
> ReplyKeyboard[PlayerName1, PlayerName2, ..., Enemy1, Enemy2, ..., <-]
$ You executed {Enemy}.
```

#### **Significant Action: Skill Check**

```
$ Choose a skill:
> ReplyKeyboard[Skill 1, Skill 2, Skill 3, <-]
```

The interactions that occur after choosing a skill are described in [the Skills documentation](Skills.md).

### **5. Reactions**

If the player is the target of an attack:

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

### **7. End of Combat**

Each conscious player will be asked if they want to perform First Aid on an ally.
```
$ Do you want to perform first aid?
> ReplyKeyboard[Yes, No]
> ReplyKeyboard[PlayerName1, PlayerName2, ..., <-]
```

If the target is Seriously Wounded:
```
$ Do you want to perform surgery?
> ReplyKeyboard[Yes, No]
```

*Target's chat:*

```
$ You can restore 5 points of damage, which characteristics should be healed?
> InlineKeyboard[Endurance, Strength, Dexterity]
```

