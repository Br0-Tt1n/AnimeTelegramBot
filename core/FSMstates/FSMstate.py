from aiogram.fsm.state import StatesGroup, State


class EditFavorites(StatesGroup):
    button_press_edit = State()
    button_press_search = State()
    answer_on_search = State()
    answer_on_at_work = State()
