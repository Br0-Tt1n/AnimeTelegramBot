import mysql.connector as con
from core.settings import settings_bd


connection = con.connect(
    host=settings_bd.datadb.host,
    user=settings_bd.datadb.user,
    password=settings_bd.datadb.password
)

if connection.is_connected():
    print("Успешно подключено к локальной базе данных!")
    cursor = connection.cursor()

    database_name = 'test_database_for_1vBOT'

    connection.database = database_name
    print(f"Подключено к базе данных '{database_name}' успешно")

    cursor.execute("""
        CREATE TABLE favorite_anime (
            id INT AUTO_INCREMENT PRIMARY KEY,
            id_main_table INT,
            anime_name VARCHAR(500),
            anime_link VARCHAR(500),
            user_id int,
            FOREIGN KEY (id_main_table) REFERENCES anime (id) ON UPDATE CASCADE,
            FOREIGN KEY (anime_name) REFERENCES anime (anime_name),
            FOREIGN KEY (anime_link) REFERENCES anime (anime_link),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """)
    print("Таблица favorite_anime успешно создана")

    cursor.close()
    connection.close()

else:
    print("Не удалось подключиться к базе данных.")
