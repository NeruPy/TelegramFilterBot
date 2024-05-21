from telegram import Update, ChatMember
from telegram.ext import CallbackContext
from savelogic import save_user_filters,load_user_filters
from utils import is_bot_in_chat

# Словарь для хранения информации о пользователях и их фильтрах в каждом чате
user_filters = load_user_filters()
# Словарь для хранения уже отправленных уведомлений
sent_notifications = {}
bot_active = True

async def start(update: Update, context: CallbackContext) -> None:
    global bot_active
    bot_active = True
    start_text = (
        'Привет! Я бот для фильтрации и организации информации.\n\n'
        'Вот что нужно сделать, чтобы использовать мои функции:\n'
        '1. Добавьте меня в чат.\n'
        '2. Используйте команды для настройки фильтров.\n\n'
        'Доступные команды:\n'
        '/start - Показать это сообщение\n'
        '/setfilter <ключевое слово> - Добавить фильтр для ключевого слова\n'
        '/removefilter <ключевое слово> - Удалить фильтр для ключевого слова\n'
        '/listfilters - Показать все ваши текущие фильтры\n'
        '/info - Показать информацию о создателе бота\n'
        '/exit - Выход из чат-бота с сохранением фильтров\n\n'
        'Пожалуйста, используйте команды только в чатах, куда добавлен бот.'
    )
    await update.message.reply_text(start_text)

async def exit_bot(update: Update, context: CallbackContext) -> None:
    global bot_active
    if not bot_active:
        return
    bot_active = False
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    await context.bot.send_message(chat_id=user_id, text="Бот отключен. Для запуска бота введите команду /start.")
    save_user_filters(user_filters)

async def set_filter(update: Update, context: CallbackContext) -> None:
    if update.message is None or update.message.from_user is None:
        return
    if not bot_active:
        return
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    args = context.args  # Получаем аргументы команды

    if not args:
        await context.bot.send_message(chat_id=user_id, text="Вы не указали ключевое слово для установки фильтра.")
        return

    filter_keywords = ' '.join(args).lower()

    if update.message.chat.type == 'private':
        await context.bot.send_message(chat_id=user_id, text="Извините, я не могу обрабатывать эту команду в личных сообщениях.")
        return

    if not await is_bot_in_chat(chat_id, context):
        await context.bot.send_message(chat_id=user_id, text="Пожалуйста, добавьте меня в чат перед настройкой фильтров.")
        return

    if chat_id not in user_filters:
        user_filters[chat_id] = {}

    if user_id in user_filters[chat_id]:
        if filter_keywords in user_filters[chat_id][user_id]:
            await context.bot.send_message(chat_id=user_id, text=f'Фильтр "{filter_keywords}" уже существует.')
        else:
            user_filters[chat_id][user_id].append(filter_keywords)
            await context.bot.send_message(chat_id=user_id, text=f'Фильтр установлен: {filter_keywords}')
    else:
        user_filters[chat_id][user_id] = [filter_keywords]
        await context.bot.send_message(chat_id=user_id, text=f'Фильтр установлен: {filter_keywords}')

    save_user_filters(user_filters)

async def remove_filter(update: Update, context: CallbackContext) -> None:
    if update.message is None or update.message.from_user is None:
        return
    if not bot_active:
        return
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    args = context.args  # Получаем аргументы команды

    if not args:
        await context.bot.send_message(chat_id=user_id, text="Вы не указали ключевое слово для удаления фильтра.")
        return

    filter_keywords = ' '.join(args).lower()

    if update.message.chat.type == 'private':
        await context.bot.send_message(chat_id=user_id, text="Извините, я не могу обрабатывать эту команду в личных сообщениях.")
        return

    if not await is_bot_in_chat(chat_id, context):
        await context.bot.send_message(chat_id=user_id, text="Пожалуйста, добавьте меня в чат перед удалением фильтров.")
        return

    if chat_id in user_filters and user_id in user_filters[chat_id] and filter_keywords in user_filters[chat_id][user_id]:
        user_filters[chat_id][user_id].remove(filter_keywords)
        await context.bot.send_message(chat_id=user_id, text=f'Фильтр "{filter_keywords}" удален.')
        if not user_filters[chat_id][user_id]:  # Если больше нет фильтров, удаляем пользователя из словаря
            del user_filters[chat_id][user_id]
    else:
        await context.bot.send_message(chat_id=user_id, text=f'Фильтр "{filter_keywords}" не найден.')

    save_user_filters(user_filters)

async def info(update: Update, context: CallbackContext) -> None:
    if not bot_active:
        return
    group_info = "Б9123-09.03.04, Жизневым В.Е."
    await context.bot.send_message(chat_id=update.message.from_user.id, text=f"Данный чат-бот создан студентом группы {group_info}")

async def list_filters(update: Update, context: CallbackContext) -> None:
    if update.message is None or update.message.from_user is None:
        return
    if not bot_active:
        return
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id

    if update.message.chat.type == 'private':
        await context.bot.send_message(chat_id=user_id, text="Извините, я не могу обрабатывать эту команду в личных сообщениях.")
        return

    if not await is_bot_in_chat(chat_id, context):
        await context.bot.send_message(chat_id=user_id, text="Пожалуйста, добавьте меня в чат перед просмотром фильтров.")
        return

    if chat_id in user_filters and user_id in user_filters[chat_id] and user_filters[chat_id][user_id]:
        filters_list = '\n'.join(user_filters[chat_id][user_id])
        await context.bot.send_message(chat_id=user_id, text=f'Ваши текущие фильтры:\n{filters_list}')
    else:
        await context.bot.send_message(chat_id=user_id, text='У вас нет установленных фильтров.')
        
async def handle_message(update: Update, context: CallbackContext) -> None:
    if update.message is None or update.message.chat_id is None:
        print("No message or chat_id")
        return
    if not context.bot_data.get("bot_active", True):
        return
    chat_id = update.message.chat_id
    message_id = update.message.message_id
    message_text = update.message.text.lower()

    if chat_id in user_filters:
        print("User filters exist")
        for user_id, filters in user_filters[chat_id].items():
            for keyword in filters:
                if keyword in message_text:
                    print("Keyword found")
                    # Генерируем уникальный идентификатор уведомления
                    notification_id = f"{chat_id}_{message_id}_{keyword}"
                    # Проверяем, было ли уже отправлено уведомление с этим идентификатором
                    if notification_id not in sent_notifications:
                        print("Notification not sent yet")
                        user = await context.bot.get_chat_member(chat_id, user_id)
                        if user and user.status != "left":
                            print("Forwarding message...")
                            # Получаем информацию о чате и отправителе
                            chat_info = await context.bot.get_chat(chat_id)
                            user_info = update.message.from_user
                            # Формируем текст для сообщения
                            forward_text = (
                                f"Сообщение из чата \"{chat_info.title}\" от {user_info.first_name}(@{user_info.username}):\n\n"
                                f"{update.message.text}"
                            )
                            # Пересылаем сообщение с припиской из какого чата оно пришло
                            await context.bot.send_message(chat_id=user_id, text=forward_text)
                            # Добавляем идентификатор уведомления в словарь уже отправленных уведомлений
                            sent_notifications[notification_id] = True

# Функция для обработки сообщений только в личных сообщениях
async def handle_private_message(update: Update, context: CallbackContext) -> None:
    if not bot_active:
        return
    if update.message.text.lower() not in ['/start', '/info', '/exit']:
        await update.message.reply_text('Извините, я могу реагировать только на команду /start, /info или /exit.')