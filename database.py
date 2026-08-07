import sqlite3
import os


class Database:

    def __init__(self, path="logs/orion.db"):

        os.makedirs("logs", exist_ok=True)

        self.conn = sqlite3.connect(path)

        self.cursor = self.conn.cursor()

        self.initialize()


    def initialize(self):

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT,
                data TEXT,
                created_at TEXT
            )
        """)

        self.conn.commit()


    def execute(
        self,
        query,
        params=()
    ):

        self.cursor.execute(
            query,
            params
        )

        self.conn.commit()

        return self.cursor


    def close(self):

        self.conn.close()
