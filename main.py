import os
import requests
import time
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TELEGRAM_TOKEN)
last_status = False

def check_model_y_stock():
    global last_status
    url = "https://www.tesla.com/tr_TR/inventory/new/my?arrangeby=plh&zip=&range=0"
    response = requests.get(url)

    if "Yeni Model Y" in response.text:
        if not last_status:
            bot.send_message(chat_id=CHAT_ID, text="🚗 Yeni Model Y stokta! https://www.tesla.com/tr_TR/inventory/new/my")
            last_status = True
    else:
        last_status = False

if __name__ == "__main__":
    while True:
        check_model_y_stock()
        time.sleep(600)