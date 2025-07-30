from flask import Flask, request
from openai import OpenAI
import os
import requests

TOKEN = os.getenv("TOKEN")  # توكن بوت تيليجرام
OPENAI_KEY = os.getenv("OPENAI_KEY")  # مفتاح OpenAI API

client = OpenAI(api_key=OPENAI_KEY)
app = Flask(__name__)

URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

@app.route('/')
def home():
    return "✅ البوت شغّال!"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    data = request.get_json()
    chat_id = data["message"]["chat"]["id"]
    text = data["message"]["text"]

    # ✅ لو المستخدم طلب تحليل أو صفقه
    if text.startswith("صفقه") or text.startswith("/signal"):
        reply = ai_reply(text)
    else:
        reply = "🤖 اكتب (صفقه ذهب) أو (تحليل) حتى أساعدك."

    send_message(chat_id, reply)
    return {"ok": True}

def ai_reply(user_text):
    """ يرسل النص إلى GPT ويرجع الرد """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "انت محلل أسواق تعطي صفقات مؤكدة وستوبات صغيرة."},
            {"role": "user", "content": user_text}
        ]
    )
    return response.choices[0].message.content

def send_message(chat_id, text):
    """ يرسل الرسالة إلى تليجرام """
    requests.post(URL, json={"chat_id": chat_id, "text": text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
