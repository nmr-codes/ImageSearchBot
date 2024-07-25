from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InputFile
import requests
import logging

from config import BOT_TOKEN
from core.states.states import WaitQuery, WaitLink
from functions.image_search import get_photos, API_KEY
from functions.downloader import Downloader
from core.keyboards.keyboards import kb, kb_photo, channel_kb


# Bot va Dispatcher
bot = Bot(BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


#-----------------VARIABLES STARTED--------------#
HELP_TEXT = """▶️List of commands<blockquote>
<strong>/start</strong> - <i>Update bot</i>
<strong>/description</strong> - <i>Description of our bot</i>
<strong>/help</strong> - <i>List of commands</i>
</blockquote>
"""

#-----------------VARIABLES ENDED--------------#

#-----------------OTHER FUNCTIONS STARTED--------------#
async def on_startup(_):
    print('Bot run successfully✓')

#-----------------OTHER FUNCTIONS ENDED--------------#

#-----------------COMMAND HANDLERS STARTED--------------#
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer(
        text='Welcome to our bot!',
        reply_markup=kb,
    )

@dp.message_handler(commands=['description'])
async def cmd_description(message: types.Message):
    await message.answer(
        "This bot can send photos.\nJust click the <strong>Search Photo</strong> button.",
        parse_mode='HTML',
    )

@dp.message_handler(commands=['help'])
async def cmd_help(message: types.Message):
    await message.answer(HELP_TEXT, parse_mode='HTML')

@dp.message_handler(Text(equals='🔍Search Photo'))
async def send_kb_photo(message: types.Message):
    await message.answer(
        text='▶️Tap the <strong>Search</strong> button and receive your photo✓',
        parse_mode='HTML',
        reply_markup=kb_photo,
    )

#-----------------SEARCHING PHOTO STATE STARTED------------------#
@dp.message_handler(Text(equals='Search🔍'))
async def cmd_search_photo(message: types.Message):
    await message.reply(
        text='🔍What are you going to search: ',
    )
    await WaitQuery.query.set()


@dp.message_handler(state=WaitQuery.query)
async def cmd_get_query(message: types.Message, state: FSMContext):
  query = message.text
  photos = get_photos(query, API_KEY)
  num_photos = len(photos)
  await state.update_data(query=query)
  await WaitQuery.num_photos.set()
  await message.answer(f'Congratulations, Results found🚨✓\n📝Your Query: {query}\n📋Number of results: {num_photos}\n❓How many do you want (1-{num_photos}): ')


@dp.message_handler(state=WaitQuery.num_photos)
async def process_query(message: types.Message, state: FSMContext):
    number = int(message.text)
    data = await state.get_data()
    query = data.get('query')
    photos = get_photos(query, API_KEY)
    if photos[:number]:
        for photo in photos[:number]:
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=photo,
            )
        await message.answer(
            '▶️Thanks for your attention.',
            reply_markup=kb,
        )
    else:
        await message.answer(
          text=f'There are only {number} pictures. Please, try again and enter the correct number.',
          reply_markup=kb_photo
        )
    await state.finish()
#-----------------SEARCHING PHOTO STATE ENDED------------------#


#-----------------DOWNLOADING VIDEO STATE STARTED------------------#
@dp.message_handler(Text(equals='📥Download Video'))
async def down_vid(message: types.Message):
  await message.answer('Send me the link of video from You Tube (Only video link, not shorts): ')
  await WaitLink.link.set()

@dp.message_handler(state=WaitLink.link)
async def get_link(message: types.Message, state: FSMContext):
  link = message.text
  dn = Downloader(link)
  dn.download()
  title = dn.title
  await bot.send_video(
    chat_id = message.chat.id,
    video = InputFile(filename=f"{title}.mp4"),
    caption = "Video downloaded successfully✓"
  )

#-----------------DOWNLOADING VIDEO STATE ENDED------------------#

@dp.message_handler(Text(equals='🔙Main Menu'))
async def send_kb_photo(message: types.Message):
    await message.answer(
        text='🔙You are in the main menu',
        parse_mode='HTML',
        reply_markup=kb,
    )

@dp.message_handler(Text(equals='📫Our Channel'))
async def cmd_description(message: types.Message):
    await message.answer(
        text="👇NEWS AND UPDATES ARE IN OUR CHANNEL👇",
        parse_mode='HTML',
        reply_markup=channel_kb,
    )
    

#-----------------MAIN EXECUTION--------------#
if __name__ == '__main__':
    executor.start_polling(
        dp,
        skip_updates=True,
        on_startup=on_startup
    )