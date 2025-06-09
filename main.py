import os
import requests
import time
import threading
from flask import Flask
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = Bot(token=TELEGRAM_TOKEN)
app = Flask(__name__)
last_status = False

@app.route("/")
def home():
    return "Bot aktif"

@app.route("/ping")
def ping():
    return "pong"

def check_model_y_stock_loop():
    global last_status
    while True:
        try:
            url = "https://www.tesla.com/tr_TR/inventory/new/my?arrangeby=plh&zip=&range=0"
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=30)
            if "Yeni Model Y" in response.text:
                if not last_status:
                    bot.send_message(chat_id=CHAT_ID, text="🚗 Yeni Model Y stokta!")
                    last_status = True
            else:
                last_status = False
            print("Stok kontrol edildi.")
        except Exception as e:
            print(f"Hata: {e}")
        time.sleep(30)

if __name__ == "__main__":
    threading.Thread(target=check_model_y_stock_loop).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
