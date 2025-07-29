from flask import Flask, request
import requests

TOKEN = "7596306669:AAGe6lNCg_nYnAK0unsrJyaCKtfo10sfWYY"
URL = f"https://api.telegram.org/bot{TOKEN}/"

app = Flask(__name__)

@app.route(f"/{TOKEN}", methods=["POST"])
def respond():
    update = request.get_json()
    if "message" in update and "text" in update["message"]:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"]["text"]
        send_message(chat_id, f"👋 مرحباً! وصلني: {text}")
    return {"ok": True}

def send_message(chat_id, text):
    requests.post(URL + "sendMessage", json={"chat_id": chat_id, "text": text})

@app.route("/")
def home():
    return "✅ البوت شغّال على Render!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
