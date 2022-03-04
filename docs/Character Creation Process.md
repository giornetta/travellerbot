# Character Creation Process

Our implementation of Character Creation in Traveller follows the *Cepheus Engine SRD* ruleset.

## Checklist

The whole process can be broken down into these phases:

1. **Characteristics**
    - Following the characteristics order (STR DEX END INT EDU SOC) roll 2D6 for each one and assign the result to it.
    - Determine DM 
2. **Homeworld**
    - Choose your homeworld from a list.
        - We are assuming that all members of an Adventure must come from the same Sector, which is chosen by the Referee beforehand.
    - Gain `3 + DM(EDU)` Background Skills at Level 0.
        - The first two have to be taken from your Homeworld, the rest from the Education List.
3. **Career Qualification**
    - Choose a career (that you haven't already left before, except Drifter).
    - Roll to qualify. If this isn't your first career, suffer a `-2 DM` for each previous career.
        - If you qualify, you start that carreer at Rank 0.
        - If you do not qualify, you can enter the Drifter career or submit to the Draft (only once).
4. **Basic Training**
    - If this is your first term in your first career, acquire every skill in the Service Skills Table at Level 0.
    - If this is your first term in a subsequent career, pick on skill from the Service Skills Table at Level 0.
5. **Survival**
    - Roll for survival, if you do not succeed, you have died. Start over.
        - With the Referee's approval, you can instead be forced out of your career and roll on the Mishaps Table. You do not receive a benefit roll for this term.
        - If you get injured and end up suffering for an Injury Crisis, you must either pay for medical care at step *12* or die and start over.
    - If you took Anagathic Drugs last term, you have to roll for survival again. If you fail you are ejected from the career and must roll on the Mishaps table.
6. **Commission and Advancement**
    - If you have been drafted, you are not eligible for a Commission roll in your first term.
    - If your career offers a Commission check and you are Rank 0, you can roll for Commission.
        - If successful, you are now Rank 1 in that career. Choose one of the Skills and Training Tables and roll on it. Take bonuses from the Ranks Table.
    - If your career offers an Advancement check and you are Rank 1+, you can roll for Advancement.
        - If successful, your Rank improves by 1. Choose one of the Skills and Training Tables and roll on it. Take bonuses from the Ranks Table.
7. **Skills and Training**
    - Choose one of the Skills and Training Tables for this career and roll on it.
        - If you gain a Skill and you already have it, increase your Level in that skill by 1. Otherwise take it at Level 1.
    - If your career does not have a Commission or Advancement check, you may roll another time.
8. **Aging**
    - You can choose if you took Anagathics Drugs during the last term.
        - If you did, add `+T DM` to roll on the Aging Table, where `T` is the number of terms since you started taking drugs.
        - If you didn't but had taken them until the previous term, you immediately roll on the Aging Table.
    - Increase your age by 4.
    - If you're 34 or older, roll for Aging.
9. **Re-enlistment**
    - Roll for re-enlistment.
        - If you fail, you must leave this career.
        - If you roll a natural 12, you must continue with this career for another term.
        - If you have served a total of 7+ terms working, you must retire. *(GO TO 10)*
        - If you succeeded and wish to continue in this career *(GO TO 5)*, otherwise *(GO TO 10)*
10. **Benefits**
    - If you're leaving the career, roll for Benefits. You get one Benefit Roll for every full term served in that career.
    - If you reached Rank 4, you get an extra roll.
    - If you reached Rank 5, you get two extra rolls.
    - If you reached Rank 6, you get three extra rolls.
11. **Next Career**
    - If you're leaving your career and you served less than 7 terms in total, you may *(GO TO 3)*.
    - Otherwise *(GO TO 13)*
12. **Pay for debts**
    - If you were injured during a career that allows this, roll `2D6 + Rank` to determine if a Patron will pay for your Medical Care.
    - If you suffered for an Injury Crisis, you must pay 1D6x10000Cr in Medical Care.
    - You can choose to restore any lost characteristic for 5000Cr a point.
    - If you used Anagathic Drugs, you have to pay 1D6x2500Cr for each term you used them. If you can't pay, you go into debt.
13. **Buy starting equipment**
    - Purchase your starting equipment, and possibly a Starship.

## Telegram Bot Interaction

This is an example conversation an user might have with the bot during Character Creation, broken down into the phases described in the Checklist:

### **1. Characteristics**

During this first phase, the bot rolls the dices and notifies the player with the results.

```
> /create
$ Rolling characteristics for your character...
$ Rolls are in!
  STR: 7
  DEX: 9
  END: 4
  INT: 8
  EDU: 8
  SOC: 10
```

### **2. Homeworld**

We use a guided approach to pick an Homeworld. The user will choose Minimum and Maximum values for each world statistic, and then they'll be presented with a list of corresponding Worlds in the Sector chosen by the Referee.

```
$ Pick your Homeworld from {Sector}!
...
$ Choose the Minimum desired Population
> ReplyKeyboard[1, ..., 10, Ignore]
$ Choose the Maximum desired Population
> ReplyKeyboard[1, ..., 10, Ignore]
...
$ Choose the Minimum Desired Tech Level
> ReplyKeyboard[1, ..., 15, Ignore]
$ Choose the Maximum Desired Tech Level
> ReplyKeyboard[1, ..., 15, Ignore]
$ These are the available Worlds on {Sector} that match your criteria!
> InlineKeyboard[Gladstone, Rossyg, Kasaan, Diomedes <-, ->]
```

Afterwards, the user will choose their Background Skills from a list provided by the bot.

```
$ Choose the first skill from your Homeworld
> ReplyKeyboard[Gun Combat-0, Animals-0, Carousing-0]
$ Choose the second skill from your Homeworld
> ReplyKeyboard[Gun Combat-0, Carousing-0]
$ Choose a skill from the Education List:
> ReplyKeyboard[Admin-0, Advocate-0, Animals-1, Cariousing-1, Comms-0, ..., Space-Sciences-0]
```

### **3. Career Qualification**



```
$ Choose a career:
> ReplyKeyboard[Aerospace System Defense, Agent, Athlete, ..., Technician]
$ You have successfully qualified for this career!
```

```
$ Choose a career:
> ReplyKeyboard[Aerospace System Defense, Agent, Athlete, ..., Technician]
$ You failed to qualify. Choose to become a Drifter or to be Drafted.
> ReplyKeyboard[Drifter, Draft]
$ You were drafted into Marine.
```

### **4. Basic Training**

```
$ You have acquired the following skills: 
  Admin-0, Computer-0, Streetwise-0, Bribery-0, Leadership-0, Vehicle-0
```

```
$ Choose a skill to acquire:
> ReplyKeyboard[Admin, Computer, Streetwise, Bribery, Leadership, Vehicle]
```

### **5. Survival**

In the default case, the bot notifies the player of the failure and the process starts over.

```
$ You died during this term. Start over.
```

In this other scenario, the bot automatically rolls Mishaps and Injuries and notifies the player, who will be able to interact only if asked to do so.

```
$ You were injured in service and thus have been medically discharged from it.
$ Due to the injury, one of your phisical characteristics must be reduced by 1, choose which one:
> InlineKeyboard[Strength, Dexterity, Endurance]
$ You are suffering an Injury Crisis! You'll die if you won't be able to pay {1D6x10000}Cr in Medical Care!
```

### **6. Commission and Advancement**

```
$ You got promoted to Rank 1! On which Table do you want to roll?
> ReplyKeyboard[Personal Development, Service Skills, Specialist Skills, Advanced Education]
$ You got +1 DEX!
$ You acquired Athletics-1 as a bonus!
$ You failed to advance.
```

### **7. Skills and Training**

```
On which Table do you want to roll?
> ReplyKeyboard[Personal Development, Service Skills, Specialist Skills, Advanced Education]
$ You acquired Survival-0!
```

### **8. Aging**

```
$ Have you used Anagathic Drugs in the last term?
> ReplyKeyboard[Yes, No]
$ Due to the shock, one physical characteristic has to be reduced by 1. Which one?
> InlineKeyboard[Strength, Dexterity, Endurance]
```

When rolling for Aging, the player will have to choose which characteristic to reduce if injured. Thanks to `InlineKeyboard`, we can update this message to receive multiple inputs.

```
$ You are now 46.
$ Due to aging, three physical characteristics have to be reduced by 1. Choose the first:
> InlineKeyboard[Strength, Dexterity, Endurance]
```

### **9. Re-enlistment**

```
$ You can re-enlist. Do you want to continue with this career or choose another one?
> ReplyKeyboard[Continue, Change]
```

```
$ You have already served 7 terms, you need to retire.
```

### **10. Benefits**

```
$ You have 2 Benefit Rolls available.
> ReplyKeyboard[Material, Cash]
$ You acquired +1 INT!
$ You have 1 Benefit Rolls available.
> ReplyKeyboard[Material, Cash]
$ You acquired 50000Cr!
```

### **11. Next career**

There's no significant interaction during this phase.

### **12. Pay for debts**

```
$ Luckily for you, a Patron offered to cover 75% of your Medical Care, you only have to pay 12000Cr!
$ You used Anagathic Drugs for 2 terms, you have to pay 5000Cr.
$ Your new balance is 3000Cr.
```

### **13. Buy starting equipment**

The player will now be presented with different lists of items they can buy, grouped by category.

Using `InlineKeyboard` as an input method allows us to use pagination and take multiple choices.

```
$ Do you want to buy an Armor?
> InlineKeyboard[Ablat, Battle Dress, ..., Vacc Suit, Skip]
...
$ Do you want to buy Explosives?
> InlineKeyboard[Plastic, Pocket Nuke, TDX, Skip]
...
```