import logging
from typing import List, Tuple, cast

from telegram import *
from telegram.ext import *

print('Bot Start')
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with 5 inline buttons attached."""
    await update.message.reply_text("Бот запущен")


async def list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.chat_data['messages']) == 0:
         await update.message.reply_text('Ваш список задач пуст.\nПополнить список - /add')
    else:
        mes_string = []
        for i, item in enumerate(context.chat_data['messages']):
            print(f'{i} - {item['body']} | Статус: {item['status']}')
            mes_string.append(f'{i + 1} - {item['body']} | Статус: {item['status']}\n')
        print(mes_string)
        await update.message.reply_text(f'{''.join(mes_string)}')



async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    if len(context.chat_data['messages']) == 0:
         await update.message.reply_text('Вам нечего удалять! Ваш список задач пуст.\nПополнить список - /add')
    else:
        await update.message.reply_text(
            f'Удалено элементов - {len(context.chat_data['messages'])}'
        )
        context.chat_data['messages'] = []

    

async def add(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Введите задачу:")
    user_text_data = update.message.text
    if 'messages' not in context.chat_data:
        context.chat_data['messages'] = []
    if user_text_data == '/add':
        pass
    else:
        context.chat_data['messages'].append({'body': update.message.text, 'status': 'Не выполнен'})
        await update.message.reply_text(f'Задача номер {len(context.chat_data['messages'])} добавлена - {user_text_data}')
        print('Сохранено')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    await update.message.reply_text(
        "Use /start to test this bot. Use /clear to clear the stored data so that you can see "
        "what happens, if the button data is not available. "
    )












def main() -> None:
    """Run the bot."""
    # We use persistence to demonstrate how buttons can still work after the bot was restarted
    persistence = PicklePersistence(filepath="data")
    # Create the Application and pass it your bot's token.
    application = (
        Application.builder()
        .token("7357384133:AAHExv_5iYJjxOIPZ8JQNV1rRg52Fj7ahrU")
        .persistence(persistence)
        .arbitrary_callback_data(True)
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("clear", clear))
    application.add_handler(CommandHandler("list", list))
    application.add_handler(MessageHandler(filters.TEXT, add))


    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()