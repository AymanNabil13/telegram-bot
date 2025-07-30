import os
import requests
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
from openai import OpenAI
from dotenv import load_dotenv

# ✅ تحميل مفاتيح API من ملف .env
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
GOLD_KEY = os.getenv("GOLDAPI_KEY")

# ✅ إعداد البوتات
bot = Bot(token=TELEGRAM_TOKEN)
client = OpenAI(api_key=OPENAI_KEY)

# ✅ إعداد Flask
app = Flask(__name__)

# ✅ دالة سعر الذهب من GoldAPI
def get_gold_price():
    url = "https://www.goldapi.io/api/XAU/USD"
    headers = {"x-access-token": GOLD_KEY}
    r = requests.get(url, headers=headers)
    data = r.json()
    return data.get("price", "❌ ماكو سعر حالياً")

# ✅ أمر /start
def start(update, context):
    update.message.reply_text("👋 أهلاً بيك! البوت شغال مثل ChatGPT + صفقات 🔥")

# ✅ أمر /gold
def gold(update, context):
    price = get_gold_price()
    update.message.reply_text(f"✨ سعر الذهب الآن: {price} $ للأونصة ✨")

# ✅ رد GPT على أي رسالة
def chat_gpt(update, context):
    user_msg = update.message.text
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "انت خبير تداول تعطي صفقات قوية وتحليل مباشر."},
                {"role": "user", "content": user_msg}
            ]
        )
        reply = response.choices[0].message.content
        update.message.reply_text(reply)
    except Exception as e:
        update.message.reply_text(f"❌ خطأ: {e}")

@app.route(f'/{TELEGRAM_TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dp.process_update(update)
    return "ok"

@app.route('/')
def index():
    return "✅ البوت شغال 24/7"

# ✅ Dispatcher
from telegram.ext import Updater
updater = Updater(bot=bot, use_context=True)
dp = updater.dispatcher

# ✅ الأوامر والرسائل
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("gold", gold))
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, chat_gpt))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
