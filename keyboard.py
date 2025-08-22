from pyrogram.types import ReplyKeyboardMarkup,  InlineKeyboardMarkup

import buttons

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [buttons.start_button],
        [buttons.quiz_button],
        [buttons.help_button],

    ],
    resize_keyboard=True
)
inline_answer_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [buttons.true_button, buttons.false_button]
    ]
)

