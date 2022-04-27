```mermaid
stateDiagram-v2
    [*] --> Start
    Start --> HandleTitle : Create
    Start --> AskCode : Join
    HandleTitle --> HandleSector
    AskCode --> AskCode: Invalid Choice
    AskCode --> StartCharacterCreation: Join w/o char
    AskCode --> IdleGame: Join with char
    
    HandleSector --> AskSector: Let me choose
    HandleSector --> GenerateSector: Generate Random
    AskSector --> HandleWorld: Valid Choice
    AskSector --> AskSector: Invalid Choice
    AskSector --> GenerateSector: Generate Random
    GenerateSector --> GenerateSector: Choose another
    GenerateSector --> AskSector: Let me choose
    GenerateSector --> HandleWorld: Accept
    
    HandleWorld --> AskWorld: Let me choose
    HandleWorld --> GenerateWorld: Generate Random
    AskWorld --> AskTerms: Valid Choice
    AskWorld --> AskWorld: Invalid Choice
    AskWorld --> GenerateWorld: Generate Random
    GenerateWorld --> GenerateWorld: Choose another
    GenerateWorld --> AskWorld: Let me choose
    GenerateWorld --> AskTerms: Accept
    
    AskTerms --> AskTerms: Invalid Choice
    AskTerms --> AskSurvival: Valid Choice
    
    AskSurvival --> [*]
    
    StartCharacterCreation --> HandleHomeworld
    HandleHomeworld --> AskHomeworld: Let me Choose
    HandleHomeworld --> GenerateHomeworld: Generate Random
    HandleHomeworld --> AskFilters: Search
    AskFilters --> AskFilters: More needed
    AskFilters --> SelectWorld: All filter set
    SelectWorld --> ChooseBackgroundSkill
    AskHomeworld --> ChooseBackgroundSkill: Valid Choice
    AskHomeworld --> AskHomeworld: Invalid Choice
    AskHomeworld --> GenerateHomeworld: Generate Random
    GenerateHomeworld --> GenerateHomeworld: Choose another
    GenerateHomeworld --> AskHomeworld: Let me choose
    GenerateHomeworld --> ChooseBackgroundSkill: Accept
    ChooseBackgroundSkill --> ChooseBackgroundSkill: Another to choose
    ChooseBackgroundSkill --> FirstCareer: All chosen
    FirstCareer --> FirstCareerRank0: Qualify
    FirstCareer --> DraftorDriften: Not qualified
    DraftorDriften --> Driften: Driften
    DraftorDriften --> Draft: Draft
    
    FirstCareerRank0 --> SurvivalRoll
    Driften --> SurvivalRoll
    Draft --> SurvivalRoll
    
    SurvivalRoll --> StartCharacterCreation: Death
    
```