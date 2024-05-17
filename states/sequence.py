from aiogram.fsm.state import State, StatesGroup

class Adverts(StatesGroup):
    adverts = State()

class Info(StatesGroup):
    pic = State()
    model = State()
    memory = State()
    document = State()
    color = State()
    master = State()
    price = State()
    phone_number = State()