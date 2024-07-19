from aiogram.fsm.state import State, StatesGroup

class SearchingState(StatesGroup):
    query = State()

class ItemsState(StatesGroup):
    items=State()
    index=State()