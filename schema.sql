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

    referee_id BIGINT NOT NULL REFERENCES users(id),
    scene_id INT DEFAULT 0
);

ALTER TABLE users ADD CONSTRAINT fkActiveAdventure FOREIGN KEY(active_adventure) REFERENCES adventures(id);

CREATE TABLE characters (
    id SERIAL PRIMARY KEY,
    char_name VARCHAR(32) NOT NULL,
    sex CHAR NOT NULL CHECK (sex = 'M' OR sex = 'F'),
    alive BOOLEAN NOT NULL DEFAULT TRUE,
    age INT NOT NULL,

    user_id BIGINT NOT NULL REFERENCES users(id),
    adventure_id CHAR(6) NOT NULL REFERENCES adventures(id),

    strength INT NOT NULL,
    dexterity INT NOT NULL,
    endurance INT NOT NULL,
    intelligence INT NOT NULL,
    education INT NOT NULL,
    social_standing INT NOT NULL,

    str_mod INT NOT NULL DEFAULT 0,
    dex_mod INT NOT NULL DEFAULT 0,
    end_mod INT NOT NULL DEFAULT 0,
    int_mod INT NOT NULL DEFAULT 0,
    edu_mod INT NOT NULL DEFAULT 0,
    soc_mod INT NOT NULL DEFAULT 0,
    credits BIGINT NOT NULL,

    equipped_armor INT,
    equipped_reflec INT,
    drawn_weapon INT,
    stance SMALLINT NOT NULL CHECK (stance BETWEEN 0 AND 2),
    rads INT NOT NULL,
    wounded BOOLEAN NOT NULL,
    fatigued BOOLEAN NOT NULL,
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

CREATE TABLE scene(
    id SERIAL PRIMARY KEY,
    scene_name VARCHAR(32)
);

CREATE TABLE npcs(
    id SERIAL PRIMARY KEY,
    npc_name VARCHAR(32) NOT NULL,

    strength INT NOT NULL,
    dexterity INT NOT NULL,
    endurance INT NOT NULL,
    intelligence INT NOT NULL,
    education INT NOT NULL,
    social_standing INT NOT NULL,
    career VARCHAR(32) NOT NULL,
    rank INT NOT NULL,
    armor INT NOT NULL,
    weapon INT NOT NULL,
    ally BOOLEAN NOT NULL DEFAULT FALSE,

    scene INT REFERENCES scene(id),
    pos INT NOT NULL DEFAULT 0 --scene position
);

CREATE TABLE careers(
    char_id SERIAL REFERENCES characters(id),
    career VARCHAR(32),
    rank INT NOT NULL,

    PRIMARY KEY (char_id, career)
);

CREATE TABLE shop (
    adventure_id CHAR(6) REFERENCES adventures(id),
    equipment_id INT,
    PRIMARY KEY(adventure_id,equipment_id)
);
