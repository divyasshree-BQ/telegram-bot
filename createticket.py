import telegram
from telegram.ext import Updater, CommandHandler, filters, MessageHandler

# Define the function to handle the /open command
def open_url(update, context):
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text=""" New Dataset: https://docs.bitquery.io/ 
        Create a ticket here: https://support.bitquery.io/ 
        Search an address: https://explorer.bitquery.io/""")

# ... Rest of the code ...





# Set up the bot and token
bot = telegram.Bot(token='key')

# Create an updater
updater = Updater(bot=bot)

# Set up the /open command handler
bot_message_handler = CommandHandler('start', open_url)
updater.dispatcher.add_handler(bot_message_handler)

# Start the bot
updater.start_polling()
