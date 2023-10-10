import logging
import json
import asyncio
import websockets


# Telegram Bot Token 
TELEGRAM_BOT_TOKEN = 'tokenn'

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
    uri = "wss://streaming.bitquery.io/graphql?api_key=keyy"
    
    try:
        async with websockets.connect(uri) as websocket:
            print('here 45')
            await websocket.send(subscription_query)
            
            while True:
                response = await websocket.recv()
                logging.info(f"Received update: {response}")

                # Parse the JSON response
                update = json.loads(response)

                await send_update_to_telegram_bots(update)
    except Exception as e:
        logging.error(e)


async def send_update_to_telegram_bots(update, context):
    print('here 64')
    bot = context.bot

    for chat_id in chat_ids:
        await bot.send_message(chat_id, f"Bitquery Update:\n\n{update}")


if __name__ == "__main__":
    asyncio.run(fetch_and_send_updates())