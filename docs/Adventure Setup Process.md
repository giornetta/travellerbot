# Adventure Setup Process

Here is described the process that any new user will go through when creating or joining an Adventure.

```
> /start
$ Welcome to Traveller Bot, do you want to create or join an Adventure?
> ReplyKeyboard[Create, Join]
```

### Create a new Adventure
 
```
$ What's the title of your adventure?
> {Adventure's title}
$ Do you want to choose a starting Sector for the adventurers or do you want to generate one randomly?
> InlineKeyboard[Let me choose, Generate Random]
```
If they decide to choose a Sector, they'll have to input its name manually:

If the Sector exists, the process will silently move on, otherwise:

```
$ What's the name of the Sector?
> {Sector}
$ No such Sector exists in this universe.
> InlineKeyboard[Choose another, Generate Random]
```

If they decide to generate a random one, the bot will propose them a Sector that they can accept or decline.

```
$ Will the adventure be set in {Sector}?
> InlineKeyboard[Accept, Generate Another, Let me choose]
```

The bot will then ask for the maximum number of terms the adventurers will be able to spend working at maximum:

```
$ How many terms will the adventurers spend working before having to retire? (Default is 7, Infinite is -1)
> {Terms}
```

The Referee will be asked to decide whether a Survival fail will make the adventurer die during [Character Creation](Character Creation Process.md).

```
$ When a Survival Check is failed, will the Adventurer die?
> ReplyKeyboard[Yes, No]
```

At this point, Adventure setup is complete and players can join:

```
$ Adventure Setup Complete! Give this code to the adventurers to make them join: {Code}!
```

When a new player joins, the Referee will receive a notification:

```
$ @{telegram_id} joined the Adventure!
```

### Join an existing adventure

```
$ What's the Code of the Adventure you'd like to join?
> {Code}
```

If the player doesn't already have an alive character in the Adventure they joined, [Character Creation](Character Creation Process.md) will start.