from aiogram.dispatcher.filters.state import State, StatesGroup

class WaitQuery(StatesGroup):
  query = State()
  num_photos = State()

class WaitLink(StatesGroup):
  link = State()