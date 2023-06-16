import requests
import json
import telegram
from telegram.ext import Updater, CommandHandler, filters, MessageHandler

# Bitquery API configuration
BITQUERY_API_URL = "https://graphql.bitquery.io"
BITQUERY_API_KEY = 'your key'

# Define the function to handle the /open command
def open_url(update, context):
    chat_id = update.message.chat_id
    address = update.message.text.split()[1]  # Extract the address from the command message
    response = query_bitquery(address)  # Send the address to Bitquery and get the response
    context.bot.send_message(chat_id=chat_id, text=response)  # Send the response to the user

def query_bitquery(address):
    payload = json.dumps({
        "query": "query MyQuery($address: String!) {\n  ethereum(network: ethereum) {\n    transfers(\n      options: {limit: 10, desc: \"block.height\"}\n      receiver: {is: $address}\n    ) {\n      block {\n        height\n      }\n      amount\n      receiver {\n        address\n      }\n      sender {\n        address\n      }\n      transaction {\n        hash\n      }\n      currency {\n        name\n      }\n    }\n  }\n}\n",
        "variables": "{\n  \"address\": \"" + address + "\"\n}"
    })
    headers = {
        'Content-Type': 'application/json',
        'X-API-KEY': 'your key'
    }

    response = requests.request("POST", BITQUERY_API_URL, headers=headers, data=payload)
    return response.text

# Set up the bot and token
bot = telegram.Bot(token='your key')

# Create an updater
updater = Updater(bot=bot)

# Set up the /open command handler
bot_message_handler = CommandHandler('start', open_url)
updater.dispatcher.add_handler(bot_message_handler)

# Start the bot
updater.start_polling()
