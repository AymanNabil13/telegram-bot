from flask import Flask, request
import requests
import os
from openai import OpenAI

# 🟢 نجيب المفاتيح من Environment Variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_KEY)

# 🟢 رابط Telegram API
TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ البوت شغال 100%"

# 🟢 Webhook لمعالجة رسائل Telegram
@app.route(f"/{TELEGRAM_TOKEN}", methods=['POST'])
def telegram_webhook():
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"]

        # 🔥 لو المستخدم كتب شي نبعثه إلى GPT ونجيب رد
        reply = ask_gpt(text)

        send_message(chat_id, reply)

    return {"ok": True}

# 🟢 دالة ترسل رسالة للتيليجرام
def send_message(chat_id, text):
    payload = {"chat_id": chat_id, "text": text}
    requests.post(TELEGRAM_URL, json=payload)

# 🟢 دالة تسأل GPT
def ask_gpt(user_text):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "انت مساعد تداول ذكي تعطي صفقات قوية وستوبات صغيرة وتحليل مع الاسباب"},
                {"role": "user", "content": user_text}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ خطأ في الاتصال بـ GPT: {str(e)}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
