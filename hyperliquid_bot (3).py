import time
import requests
from telegram import Bot

# Telegram bot config
TOKEN = "7734434132:AAE7mvTywGpo4EHq9GpBTVXZZ-lcWhbBze4"
CHAT_ID = 998450504
bot = Bot(token=TOKEN)

# Wallet and API config
wallet_address = "0x8bff50aad8b4e06c5e148eaeb9d7aef69e26cdc3"
API_URL = "https://api.hyperliquid.xyz/info"

# Previous position tracking
last_position_count = 0

def get_positions(wallet):
    headers = {"Content-Type": "application/json"}
    payload = {
        "method": "user",
        "params": {
            "user": wallet,
            "verbose": True
        }
    }
    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        positions = data.get("user", {}).get("perpPositions", [])
        return positions
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

def main():
    global last_position_count
    print("Bot is running...")

    while True:
        positions = get_positions(wallet_address)
        if len(positions) > last_position_count:
            msg = f"New position opened in wallet:\n{wallet_address}"
            bot.send_message(chat_id=CHAT_ID, text=msg)
            last_position_count = len(positions)
        time.sleep(30)

if __name__ == "__main__":
    main()