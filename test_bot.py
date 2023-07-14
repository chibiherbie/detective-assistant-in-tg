from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import config_bot
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
# from telegram import ChatAction


# Обработчик команды /get_link
async def get_link(update: Update, context: CallbackContext):
    # Получаем ссылку на чат из аргументов команды
    # chat_link = context.args[0]

    # Извлекаем ID чата из ссылки
    chat_id = '-1001589363065'

    # Отправляем нужное действие бота, чтобы пользователь видел, что что-то происходит
    # context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    # Получаем информацию о чате
    chat = context.bot.get_chat(chat_id)

    # Получаем итератор сообщений в чате
    messages = context.bot.fetch_chat_history(chat_id, limit=10)

    # Перебираем первые 10 сообщений и отправляем ссылки на них
    for message in messages:
        message_link = f"https://t.me/c/{chat_id}/{message.message_id}"
        context.bot.send_message(update.effective_chat.id, message_link)


if __name__ == '__main__':
    application = ApplicationBuilder().token(config_bot.TOKEN_BOT).build()

    start_handler = CommandHandler('start', get_link)
    application.add_handler(start_handler)

    application.run_polling()
