from pyrogram import Client, filters

import buttons
import config

bot = Client(
    "my_bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)
@bot.on_message(filters.command("start")| (buttons.start_button))
async def start(client, message):
    await message.reply("Привет, чтобы начат квиз нажми /quiz")

@bot.on_message(filters.command("help")| (buttons.help_button))
async def help(client, message):
    await message.reply("подсказки")

@bot.on_message(filters.command("quiz")| (buttons.quiz_button))
async def quiz(client, message):
    await message.reply("13")


print("Бот запускается...")
bot.run()
