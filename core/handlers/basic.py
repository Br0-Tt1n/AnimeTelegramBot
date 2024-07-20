import asyncio

from aiogram import Bot
from aiogram.types import Message

from core.keyboards.reply import (get_favorites_keyboard, get_anime_keyboard, get_first_keyboard)

from database.bd import ConnectDB


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


async def random_anime(message: Message):
    global db
    random_anime_result = db.get_randon_anime()
    await message.answer(text=f'<a href="{random_anime_result[1]}">{random_anime_result[0]}</a>', parse_mode='HTML')


async def get_let_anime(message: Message, bot: Bot):
    anime_name = ('Пример названия аниме ')
    await message.answer(anime_name)


async def get_user_id(message: Message):
    print(message.from_user.id)
