from aiogram import Dispatcher, Bot
from decouple import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage

STAFF = ['1277330153']

TOKEN = config('TOKEN')
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)
