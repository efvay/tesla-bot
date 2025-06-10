import os
import requests
import time
import threading
from flask import Flask
from telegram import Bot
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = Bot(token=TELEGRAM_TOKEN)
app = Flask(__name__)
last_status = False
last_notified_unavailable = datetime.now() - timedelta(hours=6)  # İlk çalışmada bildirim göndermesin diye

@app.route("/")
def home():
    return "Bot aktif"

@app.route("/ping")
def ping():
    return "pong"

def check_model_y_stock_loop():
    global last_status, last_notified_unavailable

    while True:
        try:
            url = "https://www.tesla.com/tr_TR/inventory/new/my?arrangeby=plh&zip=&range=0"
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/125.0.0.0 Safari/537.36"
                ),
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive"
            }
            response = requests.get(url, headers=headers, timeout=30)

            if "Yeni Model Y" in response.text:
                if not last_status:
                    bot.send_message(chat_id=CHAT_ID, text="🚗 Yeni Model Y stokta!")
                    last_status = True
            else:
                last_status = False
                now = datetime.now()
                if now - last_notified_unavailable >= timedelta(hours=6):
                    bot.send_message(chat_id=CHAT_ID, text="Model Y şu anda stokta değil.")
                    last_notified_unavailable = now

            print("Stok kontrol edildi.")
        except Exception as e:
            print(f"Hata: {e}")
        
        time.sleep(300)

if __name__ == "__main__":
    threading.Thread(target=check_model_y_stock_loop, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
