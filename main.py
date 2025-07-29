from flask import Flask, request
import requests
import os

# ناخذ التوكن من Environment Variables حتى يكون آمن
TOKEN = os.getenv("TOKEN")
URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ البوت شغال!"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    data = request.get_json()
    chat_id = data["message"]["chat"]["id"]
    text = data["message"]["text"]

    # الردود حسب الأوامر
    if text == "/start":
        reply = "👋 أهلاً بك في بوت Ayman Trading! 🚀"
    elif text == "/gold":
        reply = "✨ سعر الذهب حالياً: 3310$ للأونصة ✨"
    elif text == "/signals":
        reply = "📊 لا توجد إشارات الآن، تابع لاحقاً."
    else:
        reply = "🤖 الأمر غير معروف، جرب: /start أو /gold أو /signals"

    send_message(chat_id, reply)
    return {"ok": True}

# دالة لإرسال الرسائل
def send_message(chat_id, text):
    requests.post(URL, json={"chat_id": chat_id, "text": text})

# لتشغيل التطبيق على Render
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
