# Skills

Here is a list of all the skills and whether they need a particular implementation or not

## Assumpions
- Gunnary skill is replaced with Gun Combat
- All skills that are cascaded from Vehicle/Animals are replaced with Vehicle/Animals themselves
- Bets are not implemented
- Luxury items are not implemented
- After a skill check, both the player and the Referee receive a notification
- Bribery is simplified

## Simple Skills
The simple skills are the ones that can be called out of combat without interacting with stats or DM.

- Admin
- Advocate
- Animals
- Athletics
- Broker
- Carousing
- Comms
- Computer
- Demolition
- Electronics
- Engineering
- Gambling
- Gravitics
- Linguistic
- Liason
- Mechanics
- Medicine
- Navigation
- Piloting
- Recon
- Sciences:
    - Life Science
    - Physical Science
    - Social Science
    - Space Science
- Steward
- Streetwise
- Tactics

## Skills To Implement
- *Bribery*: If the skill check succedes, 1D6 is thrown to determine the amount of credits to pay based on the chosen crime type
- *Leadership*: In combat it is only a significant action and when used it increases the initiative of a player by the Effect of the skill check

## Passives skills
These skills cannot checked against
- Battle Dress
- Jack-of-All-Trades
- Zero-G
- Gun Combat:
    - Archery
    - Energy Pistol
    - Energy Rifle
    - Shotgun
    - Slug Pistol 
    - Slug Rifle
- Melee Combat: 
    - Bludgeoning Weapons
    - Natural Weapons
    - Piercing Weapons
    - Slashing Weapons

## Bot Interaction

For simple skills the only interaction is a message with the outcome of the skill check.

```
> ReplyKeyboard[Admin,Advocate,...]
$ You succeded the Admin skill check!
```

**Bribery**

```
> ReplyKeyboard[Admin,Bribery,...]
$ What are you accused of?
> ReplyKeyboard[Petty Crime, Misdemeanor, Serious Crime, Capital Crime]
$ You paid 1500Cr
```
```
> ReplyKeyboard[Admin,Bribery,...]
$ What are you accused of?
> ReplyKeyboard[Petty Crime, Misdemeanor, Serious Crime, Capital Crime]
$ You didn't have enough credits to pay
```

**Leadership**

```
> ReplyKeyboard[Minor Action, Significant Action]
> ReplyKeyboard[Two Minor Actions, Attack, Coup de Grace, Skill Check, Other, <-]
> ReplyKeyboard[Admin, Leadership,...]
$ Choose a player
> ReplyKeyboard[Player1,Player2,...]
$ Player2 initiative received a +2
```