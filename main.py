import os
import requests
import telebot
import openai
from dotenv import load_dotenv
from flask import Flask, request

# ✅ تحميل المتغيرات من ملف .env
load_dotenv()

# ✅ قراءة المفاتيح
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GOLDAPI_KEY = os.getenv("GOLDAPI_KEY")

# ✅ تهيئة OpenAI و Telegram
openai.api_key = OPENAI_API_KEY
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# ✅ تهيئة Flask لاستضافة البوت
app = Flask(__name__)

# ✅ دالة تجيب سعر الذهب من GoldAPI
def get_gold_price():
    url = "https://www.goldapi.io/api/XAU/USD"  # ✅ USD ذهب
    headers = {
        "x-access-token": GOLDAPI_KEY,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    return data.get("price", "❌ ماكو سعر حالياً")

# ✅ رد على أوامر المستخدم
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 أهلاً بيك! أنا بوت التداول. أكتب /gold حتى أجيبلك سعر الذهب.")

@bot.message_handler(commands=['gold'])
def send_gold_price(message):
    price = get_gold_price()
    bot.reply_to(message, f"✨ سعر الذهب حالياً: ${price} للأونصة ✨")

@bot.message_handler(func=lambda message: True)
def chat_with_ai(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "انت خبير تداول تعطي صفقات قوية مع ستوبات صغيرة."},
                {"role": "user", "content": message.text}
            ]
        )
        reply = response.choices[0].message["content"]
        bot.reply_to(message, reply)
    except Exception as e:
        bot.reply_to(message, f"❌ خطأ: {e}")

# ✅ تشغيل البوت على الويب
@app.route(f'/{TELEGRAM_TOKEN}', methods=['POST'])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "OK", 200

@app.route('/')
def index():
    return "بوت التداول شغال ✅"

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url="https://YOUR-APP-NAME.onrender.com/" + TELEGRAM_TOKEN)  # 🔄 غير YOUR-APP-NAME برابط Render
    app.run(host="0.0.0.0", port=10000)
