import logging
import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import Message

from core.settings import settings
from core.handlers.basic import (get_start, keyboard_handlers, random_anime, get_user_id, insert_favorite,
                                 get_favorite)

from database.db import ConnectDB


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=settings.bots.bot_token, default=DefaultBotProperties(parse_mode='HTML'))

    db = ConnectDB()

    dp = Dispatcher()
    dp.startup.register(start_bot)
    dp.shutdown.register(end_bot)

    # здесь будут все функции бота
    dp.message.register(get_start, Command(commands=['start', 'начать', 'run', 'поехали']))

    dp.message.register(keyboard_handlers, lambda message: any(cmd in message.text for cmd
                                                               in ["Аниме", "Избранное", "Назад", "Случайное аниме"]))

    dp.message.register(random_anime, F.text == 'Рандом')
    dp.message.register(insert_favorite, F.text == 'Добавить в избранное')
    dp.message.register(get_favorite, F.text == "Список избранных аниме")

    dp.message.register(get_user_id, F.text)

    # Проверка всех имеющихся записей
    # db.get_all_favorite()

    #  Изменение размера ячейки у определенной колонки
    # db.change_column()

    #  Просмотр индекса таблицы
    # db.show_index_db()

    # Отчистка всех данных бд
    # db.clear_db()

    # db.show_desc_table()

    try:
        await dp.start_polling(bot)
    except Exception as e:
        print(f"Ошибка {e}")
    finally:
        db.close()
        await dp.storage.close()


async def start_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Bot включен')


async def end_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Bot выключен')


if __name__ == "__main__":
    asyncio.run(main())
