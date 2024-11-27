from cgitb import text
from ctypes import resize
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

import crud_functions
from crud_functions import *

# crud_functions.initiate_db()
# for i in range(1, 5):
#     cursor.execute("INSERT INTO Products (id, title, description, price) VALUES (?, ?, ?, ?)",
#                    (i, f'Продукт {i}', f'Описание {i}', i * 100))

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kbi = InlineKeyboardMarkup( resize_keyboard = True)
buttoni1 = InlineKeyboardButton(text = 'Рассчитать норму калорий', callback_data = 'calories')
buttoni2 = InlineKeyboardButton(text = 'Формулы расчёта', callback_data = 'formulas')

kbi.insert(buttoni1)
kbi.insert(buttoni2)

ikb2 = InlineKeyboardMarkup(resize_keyboard = True)
ibutton1 = InlineKeyboardButton(text = 'Продукт1', callback_data="product_buying")
ibutton2 = InlineKeyboardButton(text = 'Продукт2', callback_data="product_buying")
ibutton3 = InlineKeyboardButton(text = 'Продукт3', callback_data="product_buying")
ibutton4 = InlineKeyboardButton(text = 'Продукт4', callback_data="product_buying")

ikb2.insert(ibutton1)
ikb2.insert(ibutton2)
ikb2.insert(ibutton3)
ikb2.insert(ibutton4)


@dp.message_handler(text = 'Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup = kbi )

@dp.callback_query_handler(text = 'product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()

@dp.callback_query_handler(text = 'formulas')
async def get_formulas(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()

@dp.message_handler(text = 'Купить')
async def get_buying_list(message):
    for prod in get_all_products():
        await message.answer(f'Название: {prod[1]} | Описание: {prod[2]} | Цена: {prod[3]}')
        with open(f'files\{prod[0]}.png', 'rb') as png:
            await message.answer_photo(png)
    await message.answer("Выберите продукт для покупки:", reply_markup = ikb2)
    

kb = ReplyKeyboardMarkup( resize_keyboard = True)
button1 = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text='Купить')
button4 = KeyboardButton(text='Регистрация')

kb.insert(button1)
kb.insert(button2)
kb.add(button3)
kb.add(button4)

class UserState(StatesGroup):  
    age = State() 
    growth = State()
    weight = State()

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = 1000


@dp.callback_query_handler(text = 'calories')
async def  set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await call.answer()

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth = message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight = message.text)
    data = await state.get_data()
    coll = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5
    await message.answer(f'{coll} калорий')
    await state.finish()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! я бот помогающий твоему здоровью', reply_markup = kb)

@dp.message_handler(text="Регистрация")
async def sign_up(message):
    await  message.answer('Введите имя пользователя (только латинский алфавит):', reply_markup=kb)
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if not is_included(message.text):
        await state.update_data(username=message.text)
        await message.answer('Введите свой email:')
        await RegistrationState.email.set()
    else:
        await message.answer('Пользователь существует, введите другое имя')
        await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer('Введите свой возраст:')
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    add_user(data['username'], data['email'], data['age'])
    await message.answer('Регистрация прошла успешно')
    await state.finish()



@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

