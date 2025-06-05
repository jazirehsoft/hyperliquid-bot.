import time
import requests
from telegram import Bot

# اطلاعات ربات تلگرام
TOKEN = "7734434132:AAE7mvTywGpo4EHq9GpBTVXZZ-lcWhbBze4"
CHAT_ID = 998450504
bot = Bot(token=TOKEN)

# آدرس کیف پول
wallet_address = "0x8bff50aad8b4e06c5e148eaeb9d7aef69e26cdc3"
API_URL = "https://api.hyperliquid.xyz/info"

# ذخیره وضعیت قبلی
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
        print(f"❌ دریافت اطلاعات با خطا مواجه شد: {e}")
        return []

def main():
    global last_position_count
    print("🤖 ربات در حال اجراست...")

    while True:
        positions = get_positions(wallet_address)
        if len(positions) > last_position_count:
            bot.send_message(
                chat_id=CHAT_ID,
                text=f"🚨 پوزیشن جدید در ولت:
{wallet_address}"
            )
            last_position_count = len(positions)
        time.sleep(30)

if __name__ == "__main__":
    main()
