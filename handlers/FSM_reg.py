from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import buttons
from db import main_db


class Reg_product(StatesGroup):
    name = State()
    article = State()
    size = State()
    count = State()
    price = State()
    photo = State()
    submit = State()


async def fsm_start(message: types.Message):
    await Reg_product.name.set()
    await message.answer(text="Введите имя товара:",
                         reply_markup=buttons.cancel)


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await Reg_product.next()
    await message.answer(text='Введите артикул:')


async def load_article(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['article'] = message.text

    await Reg_product.next()
    await message.answer(text='Введите размеры товара:')


async def load_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text

    await Reg_product.next()
    await message.answer(text='Введите количество товара:')


async def load_count(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['count'] = message.text

    await Reg_product.next()
    await message.answer(text='Введите цену:')


async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text

    await Reg_product.next()
    await message.answer(text='Отправьте фотографию товра:')


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id

    keyboard = InlineKeyboardMarkup(row_width=2)
    yes_button = InlineKeyboardButton(text='Yes', callback_data='confirm_yes')
    no_button = InlineKeyboardButton(text='No', callback_data='confirm_no')
    keyboard.add(yes_button, no_button)

    await Reg_product.next()
    await message.answer_photo(photo=data['photo'],
                               caption=f"Имя товара - {data['name']}\n"
                                       f"Артикул - {data['article']}\n"
                                       f"Размеры - {data['size']}\n"
                                       f"Количество - {data['count']}\n"
                                       f"Цена - {data['price']}"
                                       f"Данные верны?",
                               reply_markup=keyboard)


async def submit(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'confirm_yes':
        async with state.proxy() as data:
            await main_db.sql_insert_store(
                name=data['name'],
                article=data['article'],
                size=data['size'],
                count=data['count'],
                price=data['price'],
                photo=data['photo']
            )
            await callback_query.message.answer('Отлично! Регистрация пройдена.', reply_markup=buttons.start_buttons)
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


def register_fsm_order(dp: Dispatcher):
    dp.register_message_handler(cancel_fsm, Text(equals='Отмена', ignore_case=True), state='*')
    dp.register_message_handler(fsm_start, commands=['registration'])
    dp.register_message_handler(load_name, state=Reg_product.name)
    dp.register_message_handler(load_article, state=Reg_product.article)
    dp.register_message_handler(load_size, state=Reg_product.size)
    dp.register_message_handler(load_count, state=Reg_product.count)
    dp.register_message_handler(load_price, state=Reg_product.price)
    dp.register_message_handler(load_photo, state=Reg_product.photo, content_types=['photo'])
    dp.register_callback_query_handler(submit, state=Reg_product.submit)
