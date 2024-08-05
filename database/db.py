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
            port=int(settings_bd.datadb.port),
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
            SELECT * FROM users
            """)
        result = self.cursor.fetchall()
        for i in result:
            print(f"{i}")

    def show_index_db(self):
        self.cursor.execute("SHOW CREATE TABLE favorite_anime;")

        indexes = self.cursor.fetchall()
        for index in indexes:
            print(index)

    def show_desc_table(self):
        self.cursor.execute("DESCRIBE users")
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
        # print(count_id)
        random_id = random.randint(1, count_id + 1)
        self.cursor.execute(f"""
                        SELECT * FROM anime
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
        print(f'Произошла ошибка в функции check_insert_user: {e}')

    def get_anime_with_id(self, id_anime):
        get_anime = """
            SELECT * FROM anime
            WHERE id = %s
        """
        self.cursor.execute(get_anime, (id_anime,))
        anime = self.cursor.fetchone()
        return anime

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

    def check_favorite_for_user(self, id_us, enother_data=None):
        # проверка избранного у определенного юзера

        check_user_query = """
            SELECT * FROM favorite_anime
            WHERE id_main_table = %s AND anime_name = %s AND anime_link = %s 
            AND user_id = %s;
        """
        if enother_data is None:
            self.cursor.execute(check_user_query, (self.data['anime'][0],
                                                   self.data['anime'][1], self.data['anime'][2], id_us))
        else:
            self.cursor.execute(check_user_query, (enother_data[0],
                                                   enother_data[1], enother_data[2], id_us))
        result_user = self.cursor.fetchone()
        return False if result_user else True

    def insert_favorites_anime(self, id_us, search_favorite=None):
        try:
            insert_anime_query = """
                INSERT INTO favorite_anime
                (id_main_table, anime_name, anime_link, user_id, anime_episodes)
                VALUES (%s, %s, %s, %s, %s);
                """
            if search_favorite is None:
                self.cursor.execute(insert_anime_query, (self.data['anime'][0],
                                                         self.data['anime'][1], self.data['anime'][2],
                                                         id_us, self.data['anime'][3]))
            else:
                self.cursor.execute(insert_anime_query, (search_favorite[0],
                                                         search_favorite[1], search_favorite[2],
                                                         id_us, search_favorite[3]))
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

    def delete_row(self, id_delete):
        try:
            delete_row_favorite = """
               DELETE FROM favorite_anime
               WHERE id = %s
            """
            self.cursor.execute(delete_row_favorite, (id_delete,))
            self.connection.commit()
        except mysql.connector.Error as e:
            print(f"Ошибка при удалении: {e}")

    """
    Функция поиска
    """
    def get_search_anime(self, search_text):
        search_anime = """
            SELECT * FROM anime
            WHERE anime_name LIKE %s
        """
        self.cursor.execute(search_anime, (f'%{search_text}%',))
        result = self.cursor.fetchall()
        return result

    # Работа с аниме со статусом в работе
    def get_atwork_anime(self):
        all_atwork = """
            SELECT * FROM anime
            WHERE status = True
            """
        self.cursor.execute(all_atwork)
        results = self.cursor.fetchall()
        return results

    def get_users_id(self):
        all_users = """
            SELECT user_id FROM users
        """
        self.cursor.execute(all_users)
        results = self.cursor.fetchall()
        return results

    """
    Данные функции что будут представлены ниже нигде не используются кроме как файла updatedb.py
    Все это будет выложено в репозиторий одном из коммитов, но в последующих коммитах их не будет.
    """

    def change_column(self):
        alter_table_query = """
            ALTER TABLE users MODIFY COLUMN user_id BIGINT;
            """
        try:
            self.cursor.execute(alter_table_query)
            self.connection.commit()
            print("Изменения в силе босс")
        except con.Error as err:
            print(f"Ошибка: {err}")

    def update_column_episodes_table_anime(self):
        alter_table_query = ("""
                                ALTER TABLE anime
                                ADD COLUMN anime_episodes VARCHAR(20);
                             """)
        try:

            self.cursor.execute(alter_table_query)
            self.connection.commit()

        except mysql.connector.Error as err:
            print(f"Ошибка в апдейте в создании колонки в таблице anime {err}")

    def update_column_episodes_table_favorites(self):
        alter_table_query = ("""
                                ALTER TABLE favorite_anime
                                ADD COLUMN anime_episodes VARCHAR(20);
                             """)
        try:

            self.cursor.execute(alter_table_query)
            self.connection.commit()

        except mysql.connector.Error as err:
            print(f"Ошибка в апдейте в создании колонки в таблице anime_favorite {err}")

    def update_column_status_table_anime(self):
        alter_table_query = ("""
                                ALTER TABLE anime
                                ADD COLUMN status BOOLEAN;
                             """)
        try:

            self.cursor.execute(alter_table_query)
            self.connection.commit()

        except mysql.connector.Error as err:
            print(f"Ошибка в апдейте в создании колонки в таблице anime {err}")

    def update_column_clear(self):
        alter_table_query = ("""
                                UPDATE anime SET anime_episodes = NULL;
                             """)
        try:

            self.cursor.execute(alter_table_query)
            self.connection.commit()

        except mysql.connector.Error as err:
            print(f"Ошибка в апдейте в отчистке столбца  {err}")

    def update_favorite_episodes(self):
        alter_table_query = """
                                UPDATE favorite_anime AS af
                                JOIN anime AS A
                                ON af.anime_name = a.anime_name
                                AND af.anime_link = a.anime_link
                                AND af.id_main_table = a.id
                                SET af.anime_episodes = a.anime_episodes 
                            """
        try:
            self.cursor.execute(alter_table_query)
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Ошибка в апдейте в добавлении эпизодов избранным {err}")

    def update_at_work_episodes(self):
        alter_table_query = """
                                ALTER TABLE at_work
                                ADD anime_episodes VARCHAR(20);
                            """
        try:
            self.cursor.execute(alter_table_query)
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Ошибка в апдейте в добавлении эпизодов в свежее {err}")

    def get_anime_Alya(self):
        alya_anime = """
            SELECT anime_episodes FROM anime
            WHERE anime_name = "Аля иногда кокетничает со мной по-русски"
        """
        self.cursor.execute(alya_anime)
        alya = self.cursor.fetchone()
        print(alya)

    def manual_data_change(self):
        change = """
            UPDATE anime
            SET anime_episodes = '1-4'
            WHERE anime_name = "Аля иногда кокетничает со мной по-русски"
            AND anime_link = 'https://tv3.darklibria.it/release/tokidoki-bosotto-russia-go-de-dereru-tonari-no-alya-san'
        """
        self.cursor.execute(change)
        self.connection.commit()
