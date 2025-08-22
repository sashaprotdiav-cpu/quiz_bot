from pyrogram import Client, filters

import buttons
import config
import keyboard
import custom_filters
import quiz_db


"""
Очень простой квиз-бот (True/False) «как для детей».

Как это работает в двух словах:
1) Пользователь жмёт /quiz (или кнопку «Начать квиз»)
2) Бот берёт ВСЕ вопросы из базы и показывает их по одному
3) Под каждым вопросом две кнопки: «правильно» и «неправильно»
4) За верный ответ +1 балл. В конце — итог и простая лента ответов из эмодзи
"""


# Очень простое «хранилище» состояния в памяти.
# Ключ — user_id, значение — словарь с текущим прогрессом по квизу.
user_quiz_state = {}


# Создаём объект бота с данными из config.py
bot = Client(
    "my_bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)


def _make_question_text(question: dict, index: int, total: int) -> str:
    """Делаем очень понятный текст вопроса.

    :param question: словарь с полями 'text' и 'is_true'
    :param index: номер вопроса (с нуля)
    :param total: сколько всего вопросов
    """
    number_for_human = index + 1
    return (
        f"Вопрос {number_for_human}/{total}:\n"
        f"{question['text']}\n\n"
        f"Нажмите кнопку ниже:"
    )


async def _send_question_or_finish(message, user_id: int) -> None:
    """Либо отправляем текущий вопрос, либо завершаем квиз.

    В самом конце показываем:
    - общий результат «X из N»
    - простую строку ответов из эмодзи: например «✅❌✅»
    """
    state = user_quiz_state.get(user_id)
    if not state:
        return

    questions = state["questions"]
    index = state["index"]
    total = len(questions)

    # Если вопросов больше нет — показываем итоги и очищаем состояние
    if index >= total:
        answers = state.get("answers", [])
        emoji_line = "".join("✅" if ok else "❌" for ok in answers)
        await message.reply(
            f"Квиз завершён!\n\nИтог: {state['score']} из {total}.\nВаши ответы: {emoji_line}"
        )
        user_quiz_state.pop(user_id, None)
        return

    # Иначе — показываем следующий вопрос
    text = _make_question_text(questions[index], index, total)
    await message.reply(text, reply_markup=keyboard.inline_answer_keyboard)


@bot.on_message(filters.command("start") | custom_filters.button_filter(buttons.start_button))
async def start(client, message):
    """Простое приветствие и подготовка базы с вопросами."""
    quiz_db.init_db()
    quiz_db.seed_base_questions()
    await message.reply(
        "Привет! Это простой квиз. Жми /quiz, чтобы начать.",
        reply_markup=keyboard.main_keyboard,
    )


@bot.on_message(filters.command("help") | custom_filters.button_filter(buttons.help_button))
async def help_(client, message):
    """Подсказка — как проходить квиз."""
    await message.reply(
        "Нажимайте кнопки под вопросом: 'правильно' или 'неправильно'. За верный ответ +1.")


@bot.on_message(filters.command("quiz") | custom_filters.button_filter(buttons.quiz_button))
async def quiz(client, message):
    """Старт квиза: берём вопросы из базы и отправляем первый."""
    quiz_db.init_db()
    quiz_db.seed_base_questions()

    questions = quiz_db.get_all_questions()
    if not questions:
        await message.reply("В базе нет вопросов. Добавьте их и попробуйте снова.")
        return

    user_id = message.from_user.id
    user_quiz_state[user_id] = {
        "questions": questions,  # список всех вопросов
        "index": 0,              # какой по счёту вопрос сейчас
        "score": 0,              # сколько правильных ответов
        "answers": [],           # список True/False по каждому ответу
    }

    await _send_question_or_finish(message, user_id)


@bot.on_callback_query(filters.regex(r"^(correct|incorrect)$"))
async def handle_answer(client, callback_query):
    """Принимаем ответ пользователя на текущий вопрос."""
    user_id = callback_query.from_user.id
    state = user_quiz_state.get(user_id)
    if not state:
        await callback_query.answer("Начните квиз командой /quiz", show_alert=True)
        return

    questions = state["questions"]
    index = state["index"]
    if index >= len(questions):
        await callback_query.answer("Квиз уже завершён")
        return

    current = questions[index]
    user_pressed_true = callback_query.data == "correct"
    is_correct = user_pressed_true == bool(current["is_true"])  # сверяем ответ

    # Обновляем очки и копим «ленту» ответов для финального экрана
    state["answers"].append(is_correct)
    if is_correct:
        state["score"] += 1
        await callback_query.answer("✅ Верно!")
    else:
        await callback_query.answer("❌ Неверно!")

    # Переходим к следующему вопросу
    state["index"] += 1
    await _send_question_or_finish(callback_query.message, user_id)


print("Бот запускается...")
bot.run()
