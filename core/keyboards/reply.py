from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardRemove, Message, ContentType
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_first_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()

    keyboard_builder.button(text="Аниме")
    keyboard_builder.button(text="Избранное")
    keyboard_builder.adjust(2)

    return keyboard_builder.as_markup(resize_keyboard=True,
                                      one_time_keyboard=False,
                                      input_field_placeholder='Что хочешь увидеть?')


def get_anime_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()

    keyboard_builder.button(text="Случайное аниме")
    keyboard_builder.button(text="В разработке")
    keyboard_builder.button(text="Назад")
    keyboard_builder.adjust(2)

    return keyboard_builder.as_markup(resize_keyboard=True,
                                      one_time_keyboard=False,
                                      input_field_placeholder='Выбери вариант поиска')


def get_favorites_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()

    keyboard_builder.button(text="Список избранных аниме")
    keyboard_builder.button(text="В разработке")
    keyboard_builder.button(text="Назад")
    keyboard_builder.adjust(2)

    return keyboard_builder.as_markup(resize_keyboard=True,
                                      one_time_keyboard=False,
                                      input_field_placeholder='Что хочешь сделать?')

