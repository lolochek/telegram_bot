from aiogram import Bot, types
from aiogram.utils import executor
import asyncio
from aiogram.dispatcher import Dispatcher
from aiogram.types import (ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup,
                           InlineKeyboardButton, ParseMode, InlineKeyboardMarkup, Location)

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State

import config # импортируем файл config
import keyboard

import logging

storage = MemoryStorage() #FSM
bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot, storage=storage) # хранилище в RAM

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    )
class meinfo(StatesGroup):
    Q1 = State()
    Q2 = State()

@dp.message_handler(Command('me'), state=None)
async def enter_meinfo(message: types.Message):
    if message.chat.id == config.admin:
        await message.answer('начинаем настройку.\n'
                            '№1 Введите линк на ваш профиль')

        await meinfo.Q1.set()

@dp.message_handler(state=meinfo.Q1)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer1=answer)

    await message.answer('Линк сохранен.\n'
                         '№2 Введите текст.')
    await meinfo.Q2.set()

@dp.message_handler(state=meinfo.Q2)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer2=answer)

    await message.answer('Текст сохранен.')

    data = await state.get_data()
    answer1 = data.get('answer1')
    answer2 = data.get('answer2')

    joinedFile = open('link.txt', 'w', encoding='utf-8')
    joinedFile.write(answer1)

    joinedFile = open('text.txt', 'w', encoding='utf-8')
    joinedFile.write(answer2)

    await message.answer(f'Ваша ссылка на профиль: {answer1}\nВаш текст: \n{answer2}')

    await state.finish()

@dp.message_handler(commands=['start'], state=None)
async def welcome(message):
    joinedFile = open('user.txt', 'r')
    joinedUsers = set()
    for line in joinedFile:
        joinedUsers.add(line.strip())

    if not str(message.chat.id) in joinedUsers:
        joinedFile = open('user.txt', 'a')
        joinedFile.write(str(message.chat.id) + '\n')
        joinedUsers.add(str(message.chat.id))

    await bot.send_message(message.chat.id, f"Привет, *{message.from_user.first_name}*, бот пашет", reply_markup=keyboard.start, parse_mode='Markdown')

@dp.message_handler(commands=['rassilka'])
async def rassilka(message):
    if message.chat.id == config.admin:
        await bot.send_message(message.chat.id, f'*Рассылка началась*'
                               f'\nБот оповестит, когда рассылка закончится', parse_mode='Markdown')
        receive_users, block_users = 0, 0
        joinedFile = open('user.txt', 'r')
        joinedUsers = set()
        for line in joinedFile:
            joinedUsers.add(line.strip())
        joinedFile.close()
        for user in joinedUsers:
            try:
                await bot.send_photo(user, open('my_photo.jfif', 'rb'))
                receive_users += 1
            except:
                block_users += 1
            await asyncio.sleep(0.4)
        await bot.send_message(message.chat.id, f'*Рассылка была завершена*\n'
                               f'получили сообщение: {receive_users}\n'
                               f'заблокировали бота: {block_users}', parse_mode='Markdown')
    else:
        await bot.send_message(message.chat.id, f"Такой команды нет, это просто галлюцинация",
                         reply_markup=keyboard.start, parse_mode='Markdown')

@dp.message_handler(content_types=['text'])
async def get_welcome(message: types.Message):
    if message.text == 'Информация':
        await bot.send_message(message.chat.id, text='Информация\nБот создан специально для обучения', parse_mode='Markdown')

    if message.text == 'Статистика':
        await bot.send_message(message.chat.id, text='Хочешь посмотреть статистику ботика?', reply_markup=keyboard.stats, parse_mode='Markdown')

    if  message.text == 'Разработчик':
        link1 = open('link.txt', encoding='utf-8')
        link = link1.read()

        text1 = open('text.txt', encoding='utf-8')
        text = text1.read()
        await bot.send_message(message.chat.id, text=f'Создатель: {link}\n{text}', parse_mode='HTML')

    if message.text == 'Покажи пользователя':
        await bot.send_message(message.chat.id, text='Что вы хотите сделать дальше?', reply_markup=keyboard.show_user, parse_mode='Markdown')

    if message.text == 'Скинь картинку':
        await bot.send_photo(message.chat.id, open('../../pract_bot/spider.jpg', 'rb'), caption='бу')



@dp.message_handler(content_types=['location'])
async def handle_location(message: types.Message):
  if message.location:
    await bot.send_message(
      message.chat.id,
      f"Ваше текущее местоположение:\nШирота: {message.location.latitude}\nДолгота: {message.location.longitude}"
    )

@dp.callback_query_handler(text_contains='join')
async def join(call: types.CallbackQuery):
    if call.message.chat.id == config.admin:
        d = sum(1 for line in open('user.txt'))
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'Вот статистика бота: *{d}* человек', parse_mode='Markdown')
    else:
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='У тебя нет админки\nКуда ты полез', parse_mode='Markdown')

@dp.callback_query_handler(text_contains='cancle')
async def cancle(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Ты вернулся в главное меню. Жми опять кнопки', parse_mode='Markdown')



@dp.callback_query_handler(text_contains='my_id')
async def my_id(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f"Ваш id: *{call.message.chat.id}*\n\nВаш юзернейм: *{call.message.chat.username}*", parse_mode='Markdown')
@dp.callback_query_handler(text_contains='back_to_menu')
async def back_to_menu(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text='Вы отменили выбор.', parse_mode='Markdown')

if __name__ == '__main__':
    print('Бот запущен')
    executor.start_polling(dp)
