from aiogram.types import Message

from core.keyboards.reply import (get_favorites_keyboard, get_anime_keyboard, get_first_keyboard,
                                  get_random_anime_keyboard, get_back)

from database.db import ConnectDB

from core.FSMstates.FSMstate import EditFavorites as EF
from aiogram.fsm.context import FSMContext


db = ConnectDB()


async def get_start(message: Message):
    start_text = (f'Привет {message.from_user.full_name}, я ваш личный телеграмм бот с базой данных аниме'
                  ' на любой вкус и цвет\n\n'
                  'Здесь ты можешь просматривать <b>НАЗВАНИЯ</b> аниме и их ссылки, также доступно избранное в которое'
                  'просто можно добавить понравившееся аниме\n\n'
                  'В недалеком будущем планируется расширять функциноал ведь это бот v.1.  '
                  'Далее в функционал будет включаться последовательно:\n'
                  '     1) Возможность ведения своего списка просмотренных/запланированных\n'
                  '     2) Категории по жанрам, тегам, рейтингу\n'
                  '     3) Полный функционал избранного (будут приходить уведомления о выходе новых серий'
                  ' или же нового сезона аниме в избранном, выбранные аниме можно заглушить\n'
                  '     4) Это делается с помощью парсинга определенных сайтов (также выход новых серий на'
                  ' разных сайтах разный) поэтому пишите <a href="https://t.me/Q_Br0_Q">МНЕ</a>'
                  ' с каких сайтов парсить (скорее всего платно)\n'
                  '     5) Добавление <b>САЙТОВ</b> в избранные чтобы отслеживать новые серии, '
                  ' а так же добавление любимой озвучки в избранное\n'
                  'P.S.: добавление самого аниме-файл не предусматривается, но возможно будет рассмотрен в будущем')
    id_us = message.from_user.id
    db.check_insert_users(id_us)
    await message.answer(start_text, reply_markup=get_first_keyboard(), disable_web_page_preview=True)


async def keyboard_handlers(message: Message, state: FSMContext):
    text = message.text
    current_state = await state.get_state()
    # print(message.from_user.id)

    if text == "Аниме" or ((current_state == EF.button_press_search.state or current_state == EF.answer_on_search)
                           and text == "Назад"):
        await message.answer(text='Создание кнопок', reply_markup=get_anime_keyboard())
    elif text == "Поиск аниме":
        await state.set_state(EF.button_press_search)
        await message.answer(text="Введите название аниме или его часть", reply_markup=get_back())
    elif text == "Избранное" or (current_state == EF.button_press_edit.state and text == "Назад"):
        await message.answer(text='Создание кнопок', reply_markup=get_favorites_keyboard())
    elif text == "Случайное аниме":
        await message.answer(text='Создание кнопок', reply_markup=get_random_anime_keyboard())
    elif text == "Назад":
        await message.answer(text='Создание кнопок', reply_markup=get_first_keyboard())


async def random_anime(message: Message):
    global db
    random_anime_result = db.get_randon_anime()
    await message.answer(text=f'<a href="{random_anime_result[1]}">'
                              f'{random_anime_result[0]} </a> ({random_anime_result[2]})',
                         parse_mode='HTML', disable_web_page_preview=True)


async def insert_favorite(message: Message):
    id_us = message.from_user.id
    global db
    int_id = db.get_id_from_favorite(id_us)
    if db.check_favorite_for_user(int_id):
        db.insert_favorites_anime(int_id)
        await message.answer(text="Добавлено в избранное!")
    else:
        await message.answer(text="У вас уже есть это аниме в избранном!")


async def get_favorite(message: Message, state: FSMContext):
    text = message.text
    if text == "Редактировать избранное":
        await state.set_state(EF.button_press_edit)
        await message.answer(text='Выбери номер аниме, которое нужно удалить', reply_markup=get_back())

    id_us = message.from_user.id
    count = 1
    global db
    list_anime = db.get_favorite_anime(id_us)
    result_text = "Вот ваш список избранного:\n"
    for i in list_anime:
        result_text += f'<a href="{i[3]}">{count}: {i[2]} </a> ({i[5]})\n'
        count += 1
    await message.answer(text=result_text, parse_mode='HTML', disable_web_page_preview=True)


async def delete_row_favorite(message: Message, state: FSMContext):
    global db
    try:
        id_delete = int(message.text)
        id_us = message.from_user.id
        count = 1
        list_anime = db.get_favorite_anime(id_us)
        for i in list_anime:
            if count == id_delete:
                db.delete_row(i[0])
                await message.answer(text=f'Аниме "{i[2]}" было удалено из вашего списка избранных',
                                     reply_markup=get_favorites_keyboard())
                break
            else:
                count += 1
        if count-1 < id_delete:
            await message.answer("Указанный порядковый номер выше, чем имеющееся количество записей",
                                 reply_markup=get_favorites_keyboard())
        await state.clear()
    except ValueError:
        await message.answer(text="Некорректные данные", reply_markup=get_favorites_keyboard())
        await state.clear()


async def get_search_anime(message: Message, state: FSMContext):
    global db
    text = message.text
    list_anime = db.get_search_anime(text)
    count = 1
    result_text = "Вот список того, что удалось найти:\n"
    if list_anime:
        for i in list_anime:
            result_text += f'<a href="{i[2]}">{count}: {i[1]}</a>\n'
            count += 1
        await message.answer(text=result_text)
        await message.answer(text='Выберите одно или несколько аниме которое хотите добавить в избранное, '
                                  '(если выбираете несколько сделайте это в таком формате\n'
                                  '"Пример: 1, 2, 3")', reply_markup=get_back(), disable_web_page_preview=True)
        await state.set_state(EF.answer_on_search)
        await state.update_data(answer_on_search=list_anime)
    else:
        await state.clear()
        await message.answer(text='Ничего не найдено', reply_markup=get_anime_keyboard())
        

async def insert_favorite_search_anime(message: Message, state: FSMContext):
    global db
    id_us = message.from_user.id
    int_id = db.get_id_from_favorite(id_us)

    # Получаем список аниме который необходимо добавить и какой нашли
    favorite_data = message.text.split(", ")
    list_anime = await state.get_data()
    for i in favorite_data:
        if i == "Назад":
            break
        try:
            i = int(i)
            anime_info = list_anime['answer_on_search'][i-1]
            if db.check_favorite_for_user(int_id, anime_info):
                db.insert_favorites_anime(int_id, anime_info)
                await message.answer(text="Добавлено в избранное!")
            else:
                await message.answer(text=f"У вас уже есть это аниме в избранном:"
                                          f" {list_anime['answer_on_search'][i-1][1]}")
        except ValueError:
            await message.answer(text="Некорректные данные")
            await state.clear()
            break
    await state.clear()
    await message.answer(text="Возврат к предыдущим кнопкам...", reply_markup=get_anime_keyboard())


async def get_at_work_anime(message: Message, state: FSMContext):
    global db
    all_anime = db.get_atwork_anime()
    result_text = "Ниже предоставлены аниме, которые находятся в работе: \n"
    count = 1
    for i in all_anime:
        result_text += f'{count}: <a href="{i[2]}">{i[1]}</a> ({i[3]})\n'
        count += 1
    await message.answer(text=result_text, disable_web_page_preview=True)
    await message.answer(text='Выберите одно или несколько аниме которое хотите добавить в избранное, '
                              '(если выбираете несколько сделайте это в таком формате\n'
                              '"Пример: 1, 2, 3")', reply_markup=get_back())
    await state.set_state(EF.answer_on_at_work)
    await state.update_data(answer_on_at_work=all_anime)


async def insert_favorite_at_work_anime(message: Message, state: FSMContext):
    global db
    id_us = message.from_user.id
    int_id = db.get_id_from_favorite(id_us)

    # Получаем список аниме который необходимо добавить и какой нашли
    favorite_data = message.text.split(", ")
    list_anime = await state.get_data()
    for i in favorite_data:
        if i == "Назад":
            break
        try:
            i = int(i)
            anime_info = list_anime['answer_on_at_work'][i - 1]

            if db.check_favorite_for_user(int_id, anime_info):
                db.insert_favorites_anime(int_id, anime_info)
                await message.answer(text="Добавлено в избранное!")
            else:
                await message.answer(text=f"У вас уже есть это аниме в избранном:"
                                          f" {list_anime['answer_on_at_work'][i - 1][2]}")
        except ValueError:
            await message.answer(text="Некорректные данные")
            await state.clear()
            break
    await state.clear()
    await message.answer(text="Возврат к предыдущим кнопкам...", reply_markup=get_anime_keyboard())


async def get_user_id(message: Message):
    print(message.from_user.id)
