from pyrogram import Client, filters
from pyrogram.types import Message

import config

bot = Client(
    "my_bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)
@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Привет, чтобы начат квиз нажми /quiz")

@bot.on_message(filters.command("help"))
async def help(client, message):
    await message.reply("подсказки")

@bot.on_message(filters.command("quiz"))
async def quiz(client, message):
    await message.reply("")


print("Бот запускается...")
bot.run()
