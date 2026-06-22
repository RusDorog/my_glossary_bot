import logging
from telegram import BotCommand, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, filters

from config import BOT_TOKEN
from database import init_db
from handlers import (
    start, card_command, question_start, question_receive,
    case_start, case_receive, cancel, button_callback,
    WAITING_QUESTION, WAITING_CASE
)

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

def main():
    # Инициализация БД
    init_db()

    # Создание приложения
    application = Application.builder().token(BOT_TOKEN).build()

    # Команды для меню Telegram
    commands = [
        BotCommand("start", "Главное меню"),
        BotCommand("card", "Карта дня"),
        BotCommand("question", "Задать анонимный вопрос"),
        BotCommand("case", "Прислать кейс"),
        BotCommand("cancel", "Отменить текущий диалог"),
    ]
    application.bot.set_my_commands(commands)

    # Регистрация обработчиков команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("card", card_command))

    # Диалог для вопроса
    question_conv = ConversationHandler(
        entry_points=[CommandHandler("question", question_start)],
        states={
            WAITING_QUESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, question_receive)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(question_conv)

    # Диалог для кейса
    case_conv = ConversationHandler(
        entry_points=[CommandHandler("case", case_start)],
        states={
            WAITING_CASE: [MessageHandler(filters.TEXT & ~filters.COMMAND, case_receive)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(case_conv)

    # Обработчик inline-кнопок
    application.add_handler(CallbackQueryHandler(button_callback))

    # Запуск бота
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()