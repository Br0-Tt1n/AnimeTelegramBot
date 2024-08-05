import asyncio
import aiohttp
import json

from database.db import ConnectDB
from aiogram import Bot

import subprocess

db = ConnectDB()


async def new_series_notification(bot: Bot):
    global db
    subprocess.run(['python', 'core/Parser/work_parser.py'], capture_output=True)

    try:
        with open('core/Parser/save_data/anime_new_series.json', 'r', encoding='utf-8') as f:
            list_new_series = json.load(f)
    except Exception as e:
        print(Exception)
        return

    with open('core/Parser/save_data/anime_new_series.json', 'w', encoding='utf-8'):
        pass

    if not list_new_series:
        return

    users_id = db.get_users_id()
    for user_id in users_id:
        result_id = user_id[0]
        int_id = db.get_id_from_favorite(result_id)
        for anime in list_new_series:
            if not db.check_favorite_for_user(int_id, anime['anime']):
                await bot.send_message(result_id, text=f'Вышла новая {anime['anime'][3]} серия аниме:'
                                                       f' <a href="{anime['anime'][2]}">'
                                                       f'{anime['anime'][1]} </a>')


async def check_for_updates_new_series(bot: Bot):
    async with aiohttp.ClientSession() as session:
        while True:
            await new_series_notification(bot)
            await asyncio.sleep(1800)
