import logging
import json
import asyncio
import websockets

from telegram.ext import Updater, CommandHandler

# Telegram Bot Token (Replace with your bot's token)
TELEGRAM_BOT_TOKEN = 'bot token'

# List to store chat IDs dynamically
chat_ids = []

# GraphQL Subscription Query
subscription_query = """
subscription {
  EVM(network: eth) {
    Transfers(limit: {count: 10}, orderBy: {descending: Block_Time}) {
      Transfer {
        Amount
        Currency {
          Fungible
          Name
          ProtocolName
          Symbol
        }
        Data
        Id
        Receiver
        Sender
        Success
        Type
      }
    }
  }
}
"""


async def fetch_and_send_updates():
    print('here 42')
    uri = "wss://streaming.bitquery.io/graphql?"
    
    try:
        async with websockets.connect(uri) as websocket:
            await websocket.send(subscription_query)

            while True:
                response = await websocket.recv()
                logging.info(f"Received update: {response}")

                # Parse the JSON response
                update = json.loads(response)

                # You can process the update data here
                # For simplicity, we'll send it to all stored chat IDs
                await send_update_to_telegram_bots(update)
    except Exception as e:
        logging.error(e)


async def send_update_to_telegram_bots(update, context):
    print('here 64')
    bot = context.bot

    for chat_id in chat_ids:
        await bot.send_message(chat_id, f"Bitquery Update:\n\n{update}")


async def main():
    print('here 81')
    updater = Updater(TELEGRAM_BOT_TOKEN)

    dp = updater.dispatcher

    # Define a command handler for the "/start" command
    dp.add_handler(CommandHandler("start", lambda update, context: start(update, context, updater)))

    # Start fetching and sending updates from the WebSocket
    asyncio.create_task(fetch_and_send_updates())
    print('here 91')
    updater.start_polling()
    print('here 93')
    updater.idle()


async def start(update, context, bot):
    print('here 72')
    chat_id = update.message.chat_id

    if chat_id not in chat_ids:
        chat_ids.append(chat_id)

    await context.bot.send_message(chat_id, "Bot is running!")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
