from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import buttons
from config import STAFF, bot

order = str()


class Reg_order(StatesGroup):
    article = State()
    size = State()
    count = State()
    phone_number = State()
    submit = State()



async def fsm_start(message: types.Message):
    await Reg_order.article.set()
    await message.answer(text="Введите артикул:",
                         reply_markup=buttons.cancel)


async def load_article(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['article'] = message.text

    await Reg_order.next()
    await message.answer(text='Введите размеры товара:')


async def load_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text

    await Reg_order.next()
    await message.answer(text='Введите количество товара:')


async def load_count(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['count'] = message.text

    await Reg_order.next()
    await message.answer(text='Введите ваш номер телефона:')


async def load_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_number'] = message.text

    keyboard = InlineKeyboardMarkup(row_width=2)
    yes_button = InlineKeyboardButton(text='Yes', callback_data='confirm_yes')
    no_button = InlineKeyboardButton(text='No', callback_data='confirm_no')
    keyboard.add(yes_button, no_button)

    await Reg_order.next()
    await message.bot.send_message(chat_id=message.chat.id,
                                   text=f"Артикул - {data['article']}\n"
                                       f"Размеры - {data['size']}\n"
                                       f"Количество - {data['count']}\n"
                                       f"Номер телефона - {data['phone_number']}\n"
                                        f"Данные верны?",
                                   reply_markup=keyboard)

async def submit(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'confirm_yes':
        async with state.proxy() as data:
            for i in STAFF:
                await bot.send_message(chat_id=i,
                             text=f"Артикул - {data['article']}\n"
                                           f"Размеры - {data['size']}\n"
                                           f"Количество - {data['count']}\n"
                                           f"Номер телефона - {data['phone_number']}\n")

        await callback_query.message.answer('Отлично! Регистрация заказа пройдена.', reply_markup=buttons.start_buttons)
        await state.finish()
    elif callback_query.data == 'confirm_no':
        await callback_query.message.answer('Отменено!')
        await state.finish()

    else:
        await callback_query.message.answer(text='Нажмите на кнопку!', reply_markup=buttons.start_buttons)


async def cancel_fsm(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer(text='Отменено')


def register_fsm_for_user(dp: Dispatcher):
    dp.register_message_handler(cancel_fsm, Text(equals='Отмена', ignore_case=True), state='*')
    dp.register_message_handler(fsm_start, commands=['order'])
    dp.register_message_handler(load_article, state=Reg_order.article)
    dp.register_message_handler(load_size, state=Reg_order.size)
    dp.register_message_handler(load_count, state=Reg_order.count)
    dp.register_message_handler(load_number, state=Reg_order.phone_number)
    dp.register_callback_query_handler(submit, state=Reg_order.submit)
