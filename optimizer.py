import os
import sqlite3


class DatabaseOptimizer:

    def __init__(self, db_path="logs/orion.db"):

        self.db_path = db_path


    def _connect(self):

        return sqlite3.connect(self.db_path)


    def database_size(self):

        if not os.path.exists(self.db_path):
            return 0

        return os.path.getsize(self.db_path)


    def analyze(self):

        conn = self._connect()

        try:

            conn.execute("ANALYZE")
            conn.commit()

            return {
                "status": "ok",
                "action": "analyze"
            }

        finally:

            conn.close()


    def vacuum(self):

        conn = self._connect()

        try:

            conn.execute("VACUUM")
            conn.commit()

            return {
                "status": "ok",
                "action": "vacuum"
            }

        finally:

            conn.close()


    def optimize(self):

        before = self.database_size()

        self.analyze()

        self.vacuum()

        after = self.database_size()

        change = after - before

        return {

            "status": "optimized",

            "size_before": before,

            "size_after": after,

            "change": change,

            "saved": max(0, before - after)

        }


    def info(self):

        size = self.database_size()

        return {

            "database": self.db_path,

            "size_bytes": size,

            "size_kb": round(size / 1024, 2)

        }
