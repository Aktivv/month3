from handlers import commands, FSM_reg, FSM_order
import buttons
from config import dp, bot, STAFF
from aiogram.utils import executor
import logging
from db import main_db


async def on_startup(_):
    for i in STAFF:
        await bot.send_message(chat_id=i, text='Bot started', reply_markup=buttons.start_buttons)
        await main_db.sql_create()


async def on_shutdown(_):
    for i in STAFF:
        await bot.send_message(chat_id=i, text='Bot stopped')

commands.register_commands(dp)
FSM_reg.register_fsm_order(dp)
FSM_order.register_fsm_for_user(dp)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
