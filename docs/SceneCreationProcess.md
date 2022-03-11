# Scene Creation Process
Scenes are used to determine which NPCs are present during combat.
   
The Referee will be asked if they want to add a new NPC to the scene or end the process.
```
$ Do you want to add an NPC?
> ReplyKeyboard[Add, End]
```

If they decide to add a new NPC the Bot will ask how to set the NPC's characteristics.
```
$ How do you want to generate characteristics?
> InlineKeyboard[Manually, Random]
> 1 2 5 9 10 8
```

If they choose to generate them randomly, they'll have the option to accept or decline.
```
$ STR: 4
  DEX: 7
  END: 8
  INT: 2
  EDU: 2
  SOC: 10
> InlineKeyboard[Accept, Generate Again, Let me choose]
```

They will then choose the NPC's career and their rank.
```
$ What career did they take?
> ReplyKeyboard[Agent, Barbarian, ...]
$ What's their rank?
> 3
```

Next, the Referee will pick an armor and a weapon.
```
$ Pick an armor:
> ReplyKeyboard[Armor 1, Armor 2, ...]
$ Pick a weapon:
> ReplyKeyboard[Weapon 1, Weapon 2, ...]
```

Finally, they will choose the name and the faction of the NPC.
```
$ What's their name?
> Alice
$ Are they an ally or an enemy:
> ReplyKeyboard[Ally, Enemy]                
```

When the Referee decides to End the process, the scene is created.
