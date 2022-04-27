CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    active_adventure CHAR(6)
);

CREATE TABLE adventures (
   id CHAR(6) PRIMARY KEY,
   title VARCHAR(16) NOT NULL,
   sector VARCHAR(64) NOT NULL,
   planet VARCHAR(64) NOT NULL,
   max_terms INT NOT NULL,
   survival_fail_kills BOOLEAN NOT NULL,

   referee_id BIGINT NOT NULL REFERENCES users(id)
);

ALTER TABLE users ADD CONSTRAINT fkActiveAdventure FOREIGN KEY(active_adventure) REFERENCES adventures(id);

CREATE TABLE characters (
    id SERIAL PRIMARY KEY,

    user_id BIGINT NOT NULL REFERENCES users(id),
    adventure_id CHAR(6) NOT NULL REFERENCES adventures(id),

    credits BIGINT NOT NULL
);

CREATE TABLE equipments (
    id SERIAL PRIMARY KEY
);

CREATE TABLE inventories (
    character_id INT REFERENCES characters(id),
    equipment_id INT REFERENCES equipments(id),
    amount INT NOT NULL,

    PRIMARY KEY(character_id, equipment_id)
);

CREATE TABLE skills (
    name VARCHAR(32) PRIMARY KEY,
    is_passive BOOLEAN NOT NULL
);

CREATE TABLE skill_sets (
    character_id INT REFERENCES characters(id),
    skill_name VARCHAR(32) REFERENCES skills(name),

    level INT NOT NULL,

    PRIMARY KEY (character_id, skill_name)
);