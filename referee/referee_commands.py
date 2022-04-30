from psycopg2.extensions import connection


class RefereeCommands:

    def __init__(self, db: connection):
        self.db = db

    def info(cosa: str):
        if cosa == "niente":
            print("niente")
        else:
            print("qualcosa")
