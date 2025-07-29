from flask import Flask, request
import requests
import os

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

    # ✅ الردود حسب الأوامر
    if text == "/start":
        reply = "👋 أهلاً بك في بوت Ayman Trading! 🚀"
    elif text == "/gold":
        reply = "✨ سعر الذهب حالياً: 3310$ للأونصة"
    elif text == "/signals":
        reply = "📊 لا توجد إشارات الآن، تابع لاحقاً."
    else:
        reply = "🤔 لم
