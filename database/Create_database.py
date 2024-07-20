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
    cursor.execute(f"CREATE DATABASE {database_name};")
    print(f"База данных успешно завершена!")

    connection.database = database_name
    print(f"Подключено к базе данных '{database_name}' успешно")

    cursor.execute("""
        CREATE TABLE anime (
            id INT AUTO_INCREMENT PRIMARY KEY,
            anime_name VARCHAR(500),
            anime_link VARCHAR(5000)
        );
    """)
    print("Таблица anime успешно создана")

    cursor.close()
    connection.close()

else:
    print("Не удалось подключиться к базе данных.")
