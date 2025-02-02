# кнопки
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

start = ReplyKeyboardMarkup(resize_keyboard=True) # основа

info = KeyboardButton('Информация')
stats = KeyboardButton('Статистика')
razrab = KeyboardButton('Разработчик')
show_user = KeyboardButton('Покажи пользователя')
send_photo = KeyboardButton('Скинь картинку')
show_location = KeyboardButton('Геолокация', request_location=True, callback_data='location')
start.add(info, stats)
start.add(razrab)
start.add(show_user, show_location)
start.add(send_photo)

stats = InlineKeyboardMarkup()
stats.add(InlineKeyboardButton('Да', callback_data='join'))
stats.add(InlineKeyboardButton('Нет', callback_data='cancle'))

show_user = InlineKeyboardMarkup()
show_user.add(InlineKeyboardButton('Хочу увидеть id', callback_data='my_id'))
show_user.add(InlineKeyboardButton('Вернуться обратно', callback_data='back_to_menu'))


