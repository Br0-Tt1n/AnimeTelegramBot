import asyncio

from aiogram import Bot
from aiogram.types import Message

from core.keyboards.reply import (get_favorites_keyboard, get_anime_keyboard, get_first_keyboard,
                                  get_random_anime_keyboard)

from database.db import ConnectDB


db = ConnectDB()


async def get_start(message: Message, bot: Bot):
    start_text = (f'Привет {message.from_user.full_name}, я ваш личный телеграмм бот с базой данных аниме'
                  ' на любой вкус и цвет\n\n'
                  'Здесь ты можешь просматривать <b>НАЗВАНИЯ</b> аниме их описание и рейтинг\n\n'
                  'В недалеком будущем планируется расширять функцинал ведь это бот v.1.  '
                  'Далее в функционал будет включаться последовательно:\n'
                  '     1) Возможность ведения своего списка просмотренных/запланированных\n'
                  '     2) Категории по жанрам, тегам, рейтингу\n'
                  '     3) Полный функционал избранного (будут приходить уведомления о выходе новых серий'
                  ' или же нового сезона аниме в избранном, выбранные аниме можно заглушить\n'
                  '     4) Это делается с поомщью парсинга определенных сайтов (также выход новых серий на'
                  ' разных сайтах разный) поэтому пишите **** с каких сайтов парсить\n'
                  '     5) Добавление <b>САЙТОВ</b> в избранные чтобы отслеживать выход аниме именно на выбранных, '
                  ' а так же добавление любимой озвучки в избранное\n'
                  'P.S.: добавление самого аниме-файл не предусматривается, но возможно будет рассмотрен в будущем')
    id_us = message.from_user.id
    db.check_insert_users(id_us)
    await message.answer(start_text, reply_markup=get_first_keyboard())


async def keyboard_handlers(message: Message):
    text = message.text
    print(message.from_user.id)
    if text == "Аниме":
        await message.answer(text='Создание кнопок', reply_markup=get_anime_keyboard())
    elif text == "Избранное":
        await message.answer(text='Создание кнопок', reply_markup=get_favorites_keyboard())
    elif text == "Назад":
        await message.answer(text='Создание кнопок', reply_markup=get_first_keyboard())
    elif text == "Случайное аниме":
        await message.answer(text='Создание кнопок', reply_markup=get_random_anime_keyboard())


async def random_anime(message: Message):
    global db
    random_anime_result = db.get_randon_anime()
    await message.answer(text=f'<a href="{random_anime_result[1]}">'
                              f'{random_anime_result[0]}</a>', parse_mode='HTML', disable_web_page_preview=True)


async def insert_favorite(message: Message):
    id_us = message.from_user.id
    global db
    int_id = db.get_id_from_favorite(id_us)
    if db.check_favorite_for_user(int_id):
        db.insert_favorites_anime(int_id)
        await message.answer(text="Добавлено в избранное!")
    else:
        await message.answer(text="У вас уже есть это аниме в избранном!")


async def get_favorite(message: Message):
    id_us = message.from_user.id
    count = 1
    global db
    list_anime = db.get_favorite_anime(id_us)
    result_text = "Вот ваш список избранного:\n"
    for i in list_anime:
        result_text += f'<a href="{i[3]}">{count}: {i[2]}</a>\n'
        count += 1
    await message.answer(text=result_text, parse_mode='HTML', disable_web_page_preview=True)


async def get_user_id(message: Message):
    print(message.from_user.id)
