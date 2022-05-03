CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    active_adventure CHAR(6)
);

CREATE TABLE adventures (
   id CHAR(6) PRIMARY KEY,
   title VARCHAR(32) NOT NULL,
   sector VARCHAR(64) NOT NULL,
   planet VARCHAR(64) NOT NULL,
   max_terms INT NOT NULL,
   survival_fail_kills BOOLEAN NOT NULL,

   referee_id BIGINT NOT NULL REFERENCES users(id)
);

ALTER TABLE users ADD CONSTRAINT fkActiveAdventure FOREIGN KEY(active_adventure) REFERENCES adventures(id);

CREATE TABLE characters (
    id SERIAL PRIMARY KEY,
    char_name VARCHAR(32) NOT NULL,
    sex CHAR NOT NULL CHECK (sex = 'M' OR sex = 'F'),
    alive BOOLEAN NOT NULL DEFAULT TRUE,

    user_id BIGINT NOT NULL REFERENCES users(id),
    adventure_id CHAR(6) NOT NULL REFERENCES adventures(id),

    strength INT NOT NULL,
    dexterity INT NOT NULL,
    endurance INT NOT NULL,
    intelligence INT NOT NULL,
    education INT NOT NULL,
    social_standing INT NOT NULL,

    str_mod INT NOT NULL,
    dex_mod INT NOT NULL,
    end_mod INT NOT NULL,
    int_mod INT NOT NULL,
    edu_mod INT NOT NULL,
    soc_mod INT NOT NULL,
    credits BIGINT NOT NULL,

    equipped_armor INT,
    equipped_reflec INT,
    drawn_weapon INT,
    stance SMALLINT NOT NULL CHECK (stance BETWEEN 0 AND 2),
    rads INT NOT NULL,
    is_fatigued BOOLEAN NOT NULL,
    stims_taken INT NOT NULL
);

CREATE TABLE inventories (
    character_id INT NOT NULL,
    equipment_id INT NOT NULL,
    amount INT NOT NULL,
    damage INT,
    PRIMARY KEY(character_id, equipment_id)
);

CREATE TABLE skill_sets (
    character_id INT REFERENCES characters(id),
    skill_name VARCHAR(32),

    level INT NOT NULL,

    PRIMARY KEY (character_id, skill_name)
);
