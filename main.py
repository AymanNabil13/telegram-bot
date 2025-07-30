from flask import Flask, request
import requests
import os
import openai

# 🔑 جلب مفاتيح الـ API من Environment Variables
TOKEN = os.getenv("TOKEN")            # توكن بوت تيليجرام
OPENAI_KEY = os.getenv("OPENAI_KEY")  # مفتاح OpenAI

openai.api_key = OPENAI_KEY

URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

app = Flask(__name__)

# 📌 دالة إرسال الرسائل لتليجرام
def send_message(chat_id, text):
    requests.post(URL, json={"chat_id": chat_id, "text": text})

# 🤖 دالة سؤال GPT
def ask_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return f"❌ خطأ في الاتصال بـ GPT: {str(e)}"

# ✅ الصفحة الرئيسية
@app.route('/')
def home():
    return "✅ البوت شغّال!"

# 🎯 استقبال رسائل تيليجرام
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    data = request.get_json()
    chat_id = data["message"]["chat"]["id"]
    text = data["message"].get("text", "")

    # ✅ أوامر محددة
    if text == "/start":
        reply = "👋 أهلاً بك في بوت Ayman Trading 🚀\nاكتب أي سؤال أو اطلب صفقة!"
    elif text == "/gold":
        reply = "✨ سعر الذهب حالياً: $3310 (تجريبي – سنربطه بالأسعار العالمية لاحقاً)"
    elif text == "/signals":
        reply = "📊 لا توجد إشارات حالياً – تابع لاحقاً."
    else:
        # 🔥 إذا ماكو أمر محدد → استخدم GPT
        reply = ask_gpt(text)

    send_message(chat_id, reply)
    return {"ok": True}

# 🚀 تشغيل السيرفر
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
