from flask import Flask, request
import requests
import os
import threading
import time

app = Flask(__name__)

# ناخذ التوكن من الـ Environment
TOKEN = os.getenv("TOKEN")
URL = f"https://api.telegram.org/bot{TOKEN}"

# معرف التلغرام مالك (حتى يدزلك صفقات مباشرة)
ADMIN_ID = 386856110   # <-- هذا الـ ID مالك الي دزيته الي

def send_message(chat_id, text):
    """إرسال رسالة لتلغرام"""
    requests.post(f"{URL}/sendMessage", json={"chat_id": chat_id, "text": text})

@app.route('/')
def home():
    return "✅ البوت شغال!"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    data = request.get_json()
    chat_id = data["message"]["chat"]["id"]
    text = data["message"]["text"]

    if text == "/start":
        reply = "👋 أهلا بك في بوت Ayman Trading 🚀"
    elif text == "/gold":
        reply = "✨ سعر الذهب حالياً: 3310$ للأونصة ✨"
    elif text == "/signals":
        reply = "📊 لا توجد إشارات حالياً، تابع لاحقاً."
    else:
        reply = "🤖 الأمر غير معروف، جرب: /start أو /gold أو /signals"

    send_message(chat_id, reply)
    return {"ok": True}

# --- 🔥 ارسال صفقات تلقائية كل 5 دقايق ---
def auto_signals():
    while True:
        send_message(ADMIN_ID, "🚨 صفقة جديدة: شراء الذهب من 3310 بهدف 3330 🎯")
        time.sleep(300)  # 5 دقايق

threading.Thread(target=auto_signals, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
