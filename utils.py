from telegram import ChatMember
from telegram.ext import CallbackContext

async def is_bot_in_chat(chat_id: int, context: CallbackContext) -> bool:
    """
    Проверяет, добавлен ли бот в чат как участник или администратор.

    Args:
        chat_id (int): Идентификатор чата.
        context (CallbackContext): Контекст, предоставляемый библиотекой telegram.ext.

    Returns:
        bool: True, если бот является участником или администратором чата, иначе False.
    """
    try:
        bot_member = await context.bot.get_chat_member(chat_id, context.bot.id)
        return bot_member.status in [ChatMember.ADMINISTRATOR, ChatMember.MEMBER]
    except Exception as e:
        print(f"Ошибка проверки бота в чате: {e}")
        return False