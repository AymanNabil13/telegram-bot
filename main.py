from flask import Flask, request
import requests
import os
import time
import threading

# ✅ نجيب التوكن من Environment Variables
TOKEN = os.getenv("TOKEN")
URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

# ✅ ضع هنا Chat ID مالتك حتى توصلك الصفقات
ADMIN_CHAT_ID = "ضع_الشات_آي_دي_هنا"

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ البوت شغال ويراقب السوق!"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    data = request.get_json()
    chat_id = data["message"]["chat"]["id"]
    text = data["message"]["text"]

    # ✅ أوامر المستخدم
    if text == "/start":
        reply = "👋 أهلاً بك في بوت التداول الآلي! 🚀\nيراقب الذهب والبيتكوين ويبعث فرص تلقائيًا."
    elif text == "/gold":
        price = get_gold_price()
        reply = f"✨ سعر الذهب الحالي: {price}$"
    elif text == "/btc":
        price = get_btc_price()
        reply = f"💰 سعر البيتكوين الحالي: {price}$"
    else:
        reply = "🤖 استخدم /gold أو /btc لمعرفة الأسعار."

    send_message(chat_id, reply)
    return {"ok": True}

# ✅ دوال إرسال الرسائل
def send_message(chat_id, text):
    requests.post(URL, json={"chat_id": chat_id, "text": text})

def send_signal(signal_text):
    """يبعث صفقة تنبيه تلقائي"""
    requests.post(URL, json={"chat_id": ADMIN_CHAT_ID, "text": f"🔥 صفقة تلقائية 🔥\n\n{signal_text}"})

# ✅ دوال الأسعار (Gold & BTC)
def get_gold_price():
    url = "https://api.metals.live/v1/spot"   # API مجاني
    r = requests.get(url).json()
    return r[0]['gold']  # يرجع سعر الذهب الحالي

def get_btc_price():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    r = requests.get(url).json()
    return float(r["price"])

# ✅ مهمة مراقبة السوق
def monitor_market():
    gold_alert_sent = False
    btc_alert_sent = False

    while True:
        try:
            gold_price = get_gold_price()
            btc_price = get_btc_price()

            print(f"📊 الذهب: {gold_price} | بيتكوين: {btc_price}")

            # شرط الذهب (مثال: إذا صعد فوق 3300 يبعث تنبيه)
            if gold_price > 3300 and not gold_alert_sent:
                send_signal(f"💰 ذهب اخترق 3300 ✅\n✨ شراء – هدف 3320 وستوب 3285")
                gold_alert_sent = True  

            # شرط البيتكوين (مثال: إذا صعد فوق 85000 يبعث تنبيه)
            if btc_price > 85000 and not btc_alert_sent:
                send_signal(f"💰 بيتكوين اخترق 85,000 ✅\n✨ شراء – هدف 87,000 وستوب 83,000")
                btc_alert_sent = True

        except Exception as e:
            print(f"⚠️ خطأ بالمراقبة: {e}")

        time.sleep(60)  # يفحص كل دقيقة

# ✅ نشغل مراقبة السوق بخيط (Thread) حتى ما توقف البوت
threading.Thread(target=monitor_market, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
