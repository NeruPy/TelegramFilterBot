from telegram.ext import Application, CommandHandler, MessageHandler, filters
from handlers import start, set_filter, remove_filter, list_filters, info, exit_bot, handle_message, handle_private_message
from savelogic import save_user_filters,load_user_filters
from dotenv import load_dotenv
import os

def main() -> None:
    load_dotenv()
    # Вставьте ваш токен
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("setfilter", set_filter))
    application.add_handler(CommandHandler("removefilter", remove_filter))
    application.add_handler(CommandHandler("listfilters", list_filters))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(CommandHandler("exit", exit_bot))

    # Обработчики сообщений
    application.add_handler(MessageHandler(filters.ChatType.PRIVATE & ~filters.Command("start") & ~filters.Command("info") & ~filters.Command("exit"), handle_private_message))
    application.add_handler(MessageHandler(filters.ChatType.GROUP & ~filters.COMMAND, handle_message))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
