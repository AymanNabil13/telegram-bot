from flask import Flask, request
import requests
import os
import threading
import time

app = Flask(__name__)

# ✅ توكن البوت ناخذه من Render
TOKEN = os.getenv("TOKEN")
URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

# ✅ الـ Chat ID مالتك (حتى توصل إشعارات الصفقات)
ADMIN_ID = 386856110

# ✅ API Key مال GoldAPI (مباشرة من عندك)
GOLD_API_KEY = "goldapi-1x7h8smdp7fuk1-io"

def send_message(chat_id, text):
    """إرسال رسالة لتليجرام"""
    requests.post(URL, json={"chat_id": chat_id, "text": text})

@app.route('/')
def home():
    return "✅ البوت شغال عالمي ويراقب الذهب!"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    data = request.get_json()
    chat_id = data["message"]["chat"]["id"]
    text = data["message"]["text"]

    if text == "/start":
        reply = "👋 أهلاً بك في بوت التداول العالمي 🚀"
    elif text == "/gold":
        price = get_gold_price()
        reply = f"✨ سعر الذهب الآن عالميًا: {price}$"
    else:
        reply = "🤖 استخدم: /start أو /gold"

    send_message(chat_id, reply)
    return {"ok": True}

# ✅ دالة تجيب سعر الذهب لايف من GoldAPI
def get_gold_price():
    url = "https://www.goldapi.io/api/XAU/USD"
    headers = {"x-access-token": GOLD_API_KEY, "Content-Type": "application/json"}
    r = requests.get(url, headers=headers).json()
    return float(r["price"])

# ✅ دالة تراقب السوق وترسل صفقات كل 5 دقايق إذا أكو فرصة
def check_signals():
    while True:
        try:
            price = get_gold_price()
            print(f"✅ السعر الآن: {price}")

            # 🔥 هنا شروط الصفقات
            if price < 3310:
                send_message(ADMIN_ID, f"🚀 صفقة شراء ذهب ✅\nدخول: {price}\n🎯 هدف: {price + 7}\n🛑 ستوب: {price - 5}")
            elif price > 3335:
                send_message(ADMIN_ID, f"📉 صفقة بيع ذهب ✅\nدخول: {price}\n🎯 هدف: {price - 7}\n🛑 ستوب: {price + 5}")

        except Exception as e:
            print("⚠️ Error:", e)

        time.sleep(300)  # ⏳ يفحص كل 5 دقايق

# ✅ نخلي خيط الخلفية يشتغل بدون يوقف البوت
threading.Thread(target=check_signals, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
