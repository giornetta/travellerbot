# Referee Instruction Set

This document describes all the possible actions that the Referee can take.

- `/info {<name>|world|map|scene|adventure}`
- `/set <name> <... fieldName> [{+|-}][<value>]`
- `/shop {[... <type>]|close}`
- `/rest {short|long}`
- `/combat <sceneName> [end]`
- `/travel <destination>`
- `/age [... <drugsUser>] [roll] [... <character>]`
- `/scene new <name>`

## Info
```
> /info {<name>|world|map|scene|adventure}
```

The Referee will be able to get full information about:
- The characters
- The world the characters are in
- The surrounding worlds
- The current scene
- The adventure

## Set
```
> /set <name> <... fieldName> [{+|-}][<value>]
```

For each character, the Referee will be able to:
- Edit their characteristics
    - `/set Bob stat int 12`
- Edit their statuses (Stance, Wounds, Fatigue, ...)
    - `/set Bob status wounded yes`
- Edit their Credits
    - `/set Bob cr -2000`
- Add or remove items from their inventory
    - `/set Bob inv add explosive:pocketNuke 3`
    - `/set Bob inv rm personalDevice:wristWatch`

## Shop
```
> /shop {[... <type>]|close}
```

The Referee will be able to decide when to open or close a shop. When opening one, they can determine which types of equipments will be available to be bought by the players.
- `> /shop weapon armor`

## Rest
```
> /rest {short|long}
```

The Referee will be able to make the whole party rest for either a short or long duration.

## Combat
```
> /combat <sceneName> [end]
```

The Referee will be able to start or end a combat in the provided scene. Further interactions are described in [the personal Combat Documentation](PersonalCombatProcess.md).

## Travel
```
> /travel <destination>
```

The Referee will be able to choose a world the party will travel to.

## Age
```
> /age [... <drugsUser>] [roll] [... <character>]
```

The Referee will trigger the aging process for the party. They can list which characters have been taking Anagathic Drugs in the last term and which stopped doing so.

## Scene
```
> /scene new <name>
```

The Referee will be able to create a scene. Details of the creation process are described in [the Scene Creation Process documentation](SceneCreationProcess.md).
