import mysql.connector
import mysql.connector as con
import random
from core.settings import settings_bd


class ConnectDB:
    def __init__(self):
        self.connection = self.connect_db()

        self.cursor = self.connection.cursor()
        self.database_name = 'test_database_for_1vBOT'

        self.cursor.execute(f"USE {self.database_name}")
        self.data = {}

    @staticmethod
    def connect_db():
        return con.connect(
            host=settings_bd.datadb.host,
            user=settings_bd.datadb.user,
            password=settings_bd.datadb.password
        )

    def close(self):
        self.cursor.close()
        self.connection.close()

    """
    тут находятся функции для проверки работоспособности бд, данных и так далее
    """

    def is_connected(self):
        return self.connection is not None

    def get_data(self):
        return self.data

    def get_all_anime(self):
        self.cursor.execute("""
            SELECT * FROM anime
            """)
        self.data['anime'] = self.cursor.fetchall()
        print(self.cursor.fetchall())

    def get_all_favorite(self):
        self.cursor.execute("""
            SELECT * FROM favorite_anime
            """)
        result = self.cursor.fetchall()
        for i in result:
            print(f"{i}")

    def change_column(self):
        alter_table_query = """
            ALTER TABLE users MODIFY user_id BIGINT;
            """
        try:
            self.cursor.execute(alter_table_query)
            self.connection.commit()
            print("Изменения в силе босс")
        except con.Error as err:
            print(f"Ошибка: {err}")

    def show_index_db(self):
        self.cursor.execute("SHOW CREATE TABLE favorite_anime;")

        indexes = self.cursor.fetchall()
        for index in indexes:
            print(index)

    def show_desc_table(self):
        self.cursor.execute("DESCRIBE favorite_table;")
        result = self.cursor.fetchall()
        print(result)

    def clear_db(self):
        self.cursor.execute("TRUNCATE TABLE users")
        print("Чистка прошла успешна")

    """
    Вот до сюда админские функции
    """

    """
    Основные операции с базами данных
    """

    def get_randon_anime(self):
        self.cursor.execute(f"""
                        SELECT COUNT(id) FROM anime
                         """)
        count_id = self.cursor.fetchone()[0]
        print(count_id)
        random_id = random.randint(1, count_id + 1)
        self.cursor.execute(f"""
                        SELECT id, anime_name, anime_link FROM anime
                        WHERE id = {random_id}
                        """)
        result = self.cursor.fetchone()
        self.data['anime'] = result
        return result[1:]

    try:
        def check_insert_users(self, user_id):
            get_userid = """
                SELECT id FROM users 
                WHERE user_id = %s;
                """
            self.cursor.execute(get_userid, (user_id,))
            result = self.cursor.fetchone()
            if result:
                return result
            else:
                insert_user = """
                INSERT INTO users (user_id)
                VALUES (%s);
                """
                self.cursor.execute(insert_user, (user_id,))
                self.connection.commit()
                return self.cursor.lastrowid
    except Exception as e:
        print(f'Произошла ошибка в функцие check_insert_user: {e}')

    """ИЗБРАННОЕ"""
    def get_id_from_favorite(self, user_id):
        # получаю id юзера
        get_userid = """
            SELECT id FROM users 
            WHERE user_id = %s;
            """
        self.cursor.execute(get_userid, (user_id,))
        id_us = self.cursor.fetchone()[0]
        return id_us

    def check_favorite_for_user(self, id_us):
        # проверка избранного у определенного юзера
        check_user_query = """
            SELECT * FROM favorite_anime
            WHERE id_main_table = %s AND anime_name = %s AND anime_link = %s 
            AND user_id = %s;
            """
        self.cursor.execute(check_user_query, (self.data['anime'][0],
                                               self.data['anime'][1], self.data['anime'][2], id_us))
        result_user = self.cursor.fetchone()
        return False if result_user else True

    def insert_favorites_anime(self, id_us):
        try:

            insert_anime_query = """
                INSERT INTO favorite_anime
                (id_main_table, anime_name, anime_link, user_id)
                VALUES (%s, %s, %s, %s);
                """
            self.cursor.execute(insert_anime_query, (self.data['anime'][0],
                                                     self.data['anime'][1], self.data['anime'][2],
                                                     id_us))
            self.connection.commit()
        except mysql.connector.Error as e:
            print(f"Ошибка: {e}")

    def get_favorite_anime(self, user_id):
        all_favorites = """
            SELECT * FROM favorite_anime AS fa
            INNER JOIN users
            ON fa.user_id = users.id
            WHERE users.user_id = %s 
            """
        self.cursor.execute(all_favorites, (user_id,))
        results = self.cursor.fetchall()
        return results
