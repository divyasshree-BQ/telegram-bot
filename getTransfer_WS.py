import asyncio
import json
import websockets
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Your bot token from the BotFather
BOT_TOKEN = 'tokennn'

# Define a function to send messages to the Telegram bot
def send_message(update: Update, message: str):
    update.message.reply_text(message)

# Your existing code for WebSocket connection
async def my_component():
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

    async def connect():
        async with websockets.connect(url, subprotocols=['graphql-ws']) as ws:
            await ws.send(message)

            while True:
                response = await ws.recv()
                response = json.loads(response)
                
                if response.get('type') == 'data':
                    print(response['payload']['data']['EVM']['Transfers'])
                  

    await connect()

# Function to start the WebSocket connection and send updates to Telegram
async def start_websocket_and_send_updates(context: CallbackContext):
    try:
        await my_component()
    except Exception as e:
        send_message(context.bot, f"An error occurred: {str(e)}")

# Command handler to start the WebSocket connection
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Starting WebSocket connection...")
    context.job_queue.run_once(start_websocket_and_send_updates, 0)

# Create and configure the Telegram bot
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Register command handlers
    dp.add_handler(CommandHandler("start", start))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
