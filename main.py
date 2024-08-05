import logging
import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command

from core.settings import settings
from core.handlers.basic import (get_start, keyboard_handlers, random_anime, get_user_id, insert_favorite,
                                 get_favorite, delete_row_favorite, get_search_anime, insert_favorite_search_anime,
                                 get_at_work_anime, insert_favorite_at_work_anime)

from core.handlers.automatic import check_for_updates_new_series

from database.db import ConnectDB

from core.FSMstates.FSMstate import EditFavorites


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=settings.bots.bot_token, default=DefaultBotProperties(parse_mode='HTML'))

    db = ConnectDB()

    dp = Dispatcher()
    dp.startup.register(start_bot)
    dp.shutdown.register(end_bot)

    # здесь будут все функции бота
    dp.message.register(delete_row_favorite, EditFavorites.button_press_edit)
    dp.message.register(get_search_anime, EditFavorites.button_press_search)
    dp.message.register(insert_favorite_search_anime, EditFavorites.answer_on_search)
    dp.message.register(insert_favorite_at_work_anime, EditFavorites.answer_on_at_work)

    dp.message.register(get_start, Command(commands=['start', 'начать', 'run', 'поехали']))

    dp.message.register(keyboard_handlers, lambda message: any(cmd in message.text for cmd
                                                               in ["Аниме", "Избранное", "Назад", "Случайное аниме",
                                                                   "Поиск аниме"]))

    dp.message.register(random_anime, F.text == 'Рандом')
    dp.message.register(insert_favorite, F.text == 'Добавить в избранное')
    dp.message.register(get_favorite, F.text.in_({"Список избранных аниме", "Редактировать избранное"}))
    dp.message.register(get_at_work_anime, F.text == 'Свежее')

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

    # db.get_atwork_anime()

    # снёс таблицу atwork(понял что она ненужна, легче управлять всем этим с помощью добавления статуса в таблицу anime)
    asyncio.create_task(check_for_updates_new_series(bot))

    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Ошибка {e}")
    finally:
        db.close()
        await dp.storage.close()


async def start_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Bot включен')


async def end_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Bot выключен')


if __name__ == "__main__":
    asyncio.run(main())
