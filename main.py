from pyrogram import Client, filters

import buttons
import config
import keyboard
import custom_filters
import quiz_db
bot = Client(
    "my_bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)
@bot.on_message(filters.command("start")| custom_filters.button_filter(buttons.start_button))
async def start(client, message):
    await message.reply("Привет, чтобы начат квиз нажми /quiz", reply_markup=keyboard.main_keyboard)

@bot.on_message(filters.command("help")| custom_filters.button_filter(buttons.help_button))
async def help(client, message):
    await message.reply("подсказки")

@bot.on_message(filters.command("quiz")| custom_filters.button_filter(buttons.quiz_button))
async def quiz(client, message):
    await message.reply("13")


print("Бот запускается...")
bot.run()
