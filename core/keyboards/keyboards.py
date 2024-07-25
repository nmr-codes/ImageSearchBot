from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

kb = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
kb.add(
    KeyboardButton(text='🔍Search Photo'),
    #KeyboardButton(text='📥Download Video'),
    KeyboardButton(text='📫Our Channel'),
)

kb_photo = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
kb_photo.add(
    KeyboardButton(text='Search🔍'),
    KeyboardButton(text='🔙Main Menu')
)

ch_kb = [
  [InlineKeyboardButton(text="🔥OUR CHANNEL", url='https://t.me/Muhammad_Rasul_Nematxonov')]
]
channel_kb = InlineKeyboardMarkup(inline_keyboard=ch_kb)
