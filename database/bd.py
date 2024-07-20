import mysql.connector as con
import random
from core.settings import settings_bd


class ConnectDB:
    def __init__(self):
        self.connection = self.connect_db()

        self.cursor = self.connection.cursor()
        self.database_name = 'test_database_for_1vBOT'

        self.cursor.execute(f"USE {self.database_name}")

    @staticmethod
    def connect_db():
        return con.connect(
            host=settings_bd.datadb.host,
            user=settings_bd.datadb.user,
            password=settings_bd.datadb.password
        )

    def get_randon_anime(self):
        self.cursor.execute(f"""
                        SELECT COUNT(id) FROM anime
                         """)
        count_id = self.cursor.fetchone()[0]
        # print(count_id)
        random_id = random.randint(1, count_id+1)
        self.cursor.execute(f"""
                        SELECT anime_name, anime_link FROM anime
                        WHERE id = {random_id}
                        """)
        return self.cursor.fetchone()

    def get_all(self):
        self.cursor.execute("""
            SELECT * FROM anime
            """)
        print(self.cursor.fetchall())

    def close(self):
        self.cursor.close()
        self.connection.close()

    def is_connected(self):
        return self.connection is not None
