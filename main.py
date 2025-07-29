from flask import Flask, request
import requests
import os

TOKEN = "حط_التوكن_مال_بوتك_هنا"
URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ البوت شغّال!"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    data = request.get_json()
    chat_id = data["message"]["chat"]["id"]
    text = data["message"]["text"]

    # رد تلقائي
    send_message(chat_id, f"📩 استلمت رسالتك: {text}")
    return {"ok": True}

def send_message(chat_id, text):
    requests.post(URL, json={"chat_id": chat_id, "text": text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
