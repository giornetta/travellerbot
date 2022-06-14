# Traveller RPG Telegram Bot

If you want to host your own bot, please refer to the following steps:

### Requirements

- PostgresSQL 14.3+
- Python 3.8+
- A bot token granted by `@BotFather` on Telegram.

### Configuration and Deployment

First off, you'll need to create a `.env` file in the main directory of the project, filling out all the necessary parameters:

- `TELEGRAM_TOKEN`: token to access your own bot
- `DB_NAME`: name of your PostgreSQL database
- `DB_USER`: your PostgreSQL username
- `DB_PASS`: password to access your PostgreSQL database
- `EQUIP_PATH`: path to the json file containing all supported equipments, you can fill this with `data/equipment.json`
- `MAP_PATH`: path to the json file containing all supported worlds and sectors, you can fill this with `data/map.json`
- `CONV_PATH`: path to the pickle file that will contain the states of player's conversations
- `CACHE_PATH`: path to the pickle file that will contain cached actions

After filling out this configuration file, make sure to create the required PostgreSQL schema using:

```
psql -d <db_name> -a -f schema.sql
```

You can install every required dependency with

```
pip3 install requirements.txt
```

You're now ready to run your own instance of Traveller Bot by running `python3 __main__.py`!
