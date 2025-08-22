from pyrogram import emoji
from pyrogram.types import KeyboardButton, InlineKeyboardButton

start_button = KeyboardButton(f"{emoji.STAR}Старт")
quiz_button = KeyboardButton(f"{emoji.RED_QUESTION_MARK}Начать квиз")
help_button = KeyboardButton(f"{emoji.AMBULANCE}Подсказка")


true_button = InlineKeyboardButton("правильно", callback_data="correct")
false_button = InlineKeyboardButton("неправильно", callback_data="incorrect")