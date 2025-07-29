from flask import Flask, request
import requests
import os
import threading
import time

# نجيب التوكن من Environment Variables
TOKEN = os.getenv("TOKEN")
URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

# ضع هنا الـ Chat ID مالتك
CHAT_ID = "386856110"  # ← هذا ID مالك

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ البوت شغّال!"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    data = request.get_json()
    chat_id = data["message"]["chat"]["id"]
    text = data["message"]["text"]

    # الأوامر اليدوية
    if text == "/start":
        reply = "👋 أهلاً بك في بوت Ayman Trading 🚀"
    elif text == "/gold":
        reply = "✨ سعر الذهب حالياً: 3310$ للأونصة ✨"
    elif text == "/signals":
        reply = "📊 لا توجد إشارات حالياً."
    else:
        reply = "🤖 الأمر غير معروف، جرّب: /start أو /gold أو /signals"

    send_message(chat_id, reply)
    return {"ok": True}

def send_message(chat_id, text):
    """إرسال رسالة إلى التلغرام"""
    requests.post(URL, json={"chat_id": chat_id, "text": text})

# 🔔 إشعارات أوتوماتيكية كل 5 دقايق للتجربة
def send_auto_signals():
    while True:
        time.sleep(300)  # ⏳ 300 ثانية = 5 دقائق
        send_message(CHAT_ID, "🚀 صفقة تجريبية 🔥 – هذا إشعار كل 5 دقايق للتجربة")

# تشغيل الثريد الخاص بالتنبيهات
threading.Thread(target=send_auto_signals, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
