from pyrogram.types import ReplyKeyboardMarkup,  InlineKeyboardButton

import buttons

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [buttons.start_button],
        [buttons.quiz_button],
        [buttons.help_button],

    ],
    resize_keyboard=True
)
