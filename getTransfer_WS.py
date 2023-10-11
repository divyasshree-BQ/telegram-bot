import asyncio
import json
import websockets
import tracemalloc
from telegram import Update, ext
from telegram.ext import Updater, CommandHandler, CallbackContext

# Your bot token from the BotFather
BOT_TOKEN = 'tokenn'

# Define a function to send messages to the Telegram bot
def send_message(update: Update, message: str):
    update.message.reply_text(message)

# Split long text into smaller parts
def split_text(text, max_length):
    return [text[i:i + max_length] for i in range(0, len(text), max_length)]

# Function to send a long message as multiple smaller messages
def send_long_message(update: Update, long_message, max_message_length=4000):
    message_parts = split_text(long_message, max_message_length)
    for part in message_parts:
        send_message(update, part)

# websocket code
async def my_component(update):
    print("line 30")
    url = 'wss://streaming.bitquery.io/graphql'
    message = json.dumps({
        "type": "start",
        "id": "1",
        "payload": {
            "query": "subscription {\n  EVM {\n    Transfers {\n      Transfer {\n        Amount\n        __typename\n        Currency {\n          __typename\n          Symbol\n        }\n      }\n    }\n  }\n}",
            "variables": {}
        },
        "headers": {
            "X-API-KEY": "keyy"
        }
    })

    async def connect(update):
       
        async with websockets.connect(url, subprotocols=['graphql-ws']) as ws:
            await ws.send(message)

            while True:
                response = await ws.recv()
                response = json.loads(response)
                
                if response.get('type') == 'data':
                  
                    # Send the response to the Telegram chat
                    print("line 43-3")
                    response_text = f"{response['payload']['data']['EVM']['Transfers']}"
                    send_long_message(update, response_text)
                    #update.message.reply_text(f"{response['payload']['data']['EVM']['Transfers']}")

    await connect(update)

# Function to start the WebSocket connection and send updates to Telegram
async def start_websocket_and_send_updates(update):
    print("line 45")
    try:
        await my_component(update)
    except Exception as e:
       print(str(e))

# Command handler to start the WebSocket connection
def start(update: Update, context: CallbackContext):
    print("line 52")
    update.message.reply_text("Starting WebSocket connection...")
    asyncio.run(start_websocket_and_send_updates(update))

# Create and configure the Telegram bot
def main():
    tracemalloc.start()
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Register command handlers
    dp.add_handler(CommandHandler("start", start))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
