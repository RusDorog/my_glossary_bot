import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

from cards import CARDS
from database import save_message

# Состояния для диалогов
WAITING_QUESTION = 1
WAITING_CASE = 2

# ---------- Вспомогательные функции ----------
def get_main_menu_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("🃏 Карта дня", callback_data="card"),
            InlineKeyboardButton("💀 Задать вопрос", callback_data="question")
        ],
        [
            InlineKeyboardButton("🔥 Прислать кейс", callback_data="case"),
            InlineKeyboardButton("📢 Наш канал", url="https://t.me/glossary_official")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Приветственное сообщение с главным меню."""
    text = (
        "🖤 Добро пожаловать в «Глоссарий Тьмы».\n\n"
        "Я — не гадалка. Я — твоё слепое пятно.\n"
        "Никаких «любит-не-любит». Только карта дня как чек-лист ошибок, деньги, риски и чёрный юмор.\n\n"
        "Что ты здесь получишь:\n"
        "🃏 Карту дня — с конкретным действием, а не предсказанием\n"
        "💀 Возможность задать анонимный вопрос — и получить честный разбор\n"
        "🔥 Право прислать свой кейс — и увидеть его в канале (анонимно)\n\n"
        "Слабакам не сюда. Остальным — нажимай кнопку ниже."
    )
    await update.message.reply_text(text, reply_markup=get_main_menu_keyboard())

async def card_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправить случайную карту с заданием."""
    card = random.choice(CARDS)
    text = (
        f"🎴 Твоя карта дня — **{card['name']}**\n\n"
        f"{card['description']}\n\n"
        f"📌 Твоё задание на сегодня:\n{card['task']}\n\n"
        "Сделай это. Прямо сейчас. Не откладывай.\n"
        "Карта не врёт. Она просто показывает то, что ты упорно не замечаешь."
    )
    keyboard = [
        [InlineKeyboardButton("🔮 Ещё раз", callback_data="card")],
        [InlineKeyboardButton("🏠 В меню", callback_data="menu")]
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def question_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало диалога для вопроса."""
    text = (
        "💀 Опиши свою ситуацию.\n\n"
        "Честно. Без воды. Я прочитаю и отвечу в канале — анонимно.\n"
        "Никто не узнает, что это ты. Даже я не буду знать, кто написал.\n\n"
        "Отправь текст одним сообщением. Для отмены введи /cancel."
    )
    await update.message.reply_text(text)
    return WAITING_QUESTION

async def question_receive(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получить текст вопроса и сохранить."""
    user_text = update.message.text
    save_message(update.effective_user.id, "question", user_text)
    await update.message.reply_text(
        "✅ Твой вопрос улетел в Тьму.\n\n"
        "Я разберу его в одном из ближайших постов. Следи за каналом.\n"
        "А пока — вернись в меню и возьми карту дня.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 В меню", callback_data="menu")]])
    )
    return ConversationHandler.END

async def case_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало диалога для кейса."""
    text = (
        "🔥 Опиши свою ситуацию — ту, в которой ты застрял.\n\n"
        "Деньги, работа, отношения, страх, решение. Всё, что хочешь разобрать.\n"
        "Я выберу самый жёсткий кейс и разберу его в канале. Анонимно. Без имён.\n\n"
        "Отправь текст одним сообщением. Для отмены введи /cancel."
    )
    await update.message.reply_text(text)
    return WAITING_CASE

async def case_receive(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получить текст кейса и сохранить."""
    user_text = update.message.text
    save_message(update.effective_user.id, "case", user_text)
    await update.message.reply_text(
        "✅ Твой кейс принят.\n\n"
        "Если я выберу его для разбора — ты увидишь себя в канале. Узнаешь — по картам и по ситуации.\n"
        "А пока — вернись в меню. Там ждёт твоя карта дня.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 В меню", callback_data="menu")]])
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отмена диалога."""
    await update.message.reply_text(
        "Диалог отменён. Возвращайся в меню.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 В меню", callback_data="menu")]])
    )
    return ConversationHandler.END

# ---------- Обработчики нажатий на inline-кнопки ----------
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    if data == "card":
        card = random.choice(CARDS)
        text = (
            f"🎴 Твоя карта дня — **{card['name']}**\n\n"
            f"{card['description']}\n\n"
            f"📌 Твоё задание на сегодня:\n{card['task']}\n\n"
            "Сделай это. Прямо сейчас. Не откладывай."
        )
        keyboard = [
            [InlineKeyboardButton("🔮 Ещё раз", callback_data="card")],
            [InlineKeyboardButton("🏠 В меню", callback_data="menu")]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data == "menu":
        text = "Главное меню. Выбери действие:"
        await query.edit_message_text(text, reply_markup=get_main_menu_keyboard())

    elif data == "question":
        # Начинаем диалог вопроса через команду /question, но здесь можно просто вызвать вопрос
        # Чтобы не усложнять, предложим пользователю ввести /question
        await query.edit_message_text(
            "Используй команду /question, чтобы задать вопрос.\nИли нажми /start для возврата."
        )

    elif data == "case":
        await query.edit_message_text(
            "Используй команду /case, чтобы прислать кейс.\nИли нажми /start для возврата."
        )