from aiogram import types, Dispatcher
from config import bot


async def start(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Бот запущен')

async def info(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                       text='''Это бот онлайн магазина \n
Вы можете посмотреть ассортимент товаров, а также сделать заказ''')

def register_commands(dp: Dispatcher):
    dp.register_message_handler(start, commands='start')
    dp.register_message_handler(info, commands='info')
