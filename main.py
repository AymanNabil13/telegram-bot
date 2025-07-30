from flask import Flask, request
import requests
import os
import threading
import time

app = Flask(__name__)

TOKEN = os.getenv("TOKEN")
URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

# ✅ Chat ID مالتك
ADMIN_ID = 386856110

# ✅ API Key مال GOLDAPI
GOLD_API_KEY = "goldapi-1x7h8smdp7fuk1-io"

# 🏹 متغيرات الصفقة الحية
active_trade = None  # ماكو صفقة بالبداية

def send_message(chat_id, text):
    """إرسال رسالة لتلغرام"""
    requests.post(URL, json={"chat_id": chat_id, "text": text})

@app.route('/')
def home():
    return "✅ البوت شغّال!"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    data = request.get_json()
    chat_id = data["message"]["chat"]["id"]
    text = data["message"]["text"]

    if text == "/start":
        reply = "👋 أهلاً بك! البوت رح يرسللك فقط أقوى الصفقات ويعلّق عليها تلقائيًا."
    elif text == "/gold":
        price = get_gold_price()
        reply = f"✨ سعر الذهب الآن عالميًا: {price}$"
    else:
        reply = "🤖 استخدم: /start أو /gold"
    send_message(chat_id, reply)
    return {"ok": True}

# ✅ دالة تجيب سعر الذهب لايف
def get_gold_price():
    url = "https://www.goldapi.io/api/XAU/USD"
    headers = {"x-access-token": GOLD_API_KEY, "Content-Type": "application/json"}
    r = requests.get(url, headers=headers).json()
    return float(r["price"])

# ✅ دالة تفتح صفقة قوية إذا صار كسر حقيقي
def open_trade(trade_type, entry, target, stop, reason):
    global active_trade
    active_trade = {
        "type": trade_type,
        "entry": entry,
        "target": target,
        "stop": stop,
        "reason": reason,
        "status": "open"
    }
    send_message(ADMIN_ID,
        f"🚀 **صفقة { 'شراء' if trade_type == 'buy' else 'بيع' } قوية** ✅\n"
        f"📊 **سبب الدخول:** {reason}\n\n"
        f"✅ دخول: {entry}\n🎯 هدف: {target}\n🛑 ستوب: {stop}\n\n"
        f"💬 سأتابع الصفقة معك كل دقيقة…"
    )

# ✅ دالة لمراقبة الصفقة المفتوحة
def monitor_trade(price):
    global active_trade
    if active_trade and active_trade["status"] == "open":
        trade = active_trade
        if trade["type"] == "buy":
            if price >= trade["target"]:
                send_message(ADMIN_ID, "🎯 **الهدف تحقق!** ✅ صفقة شراء ناجحة 🔥")
                trade["status"] = "closed"
            elif price <= trade["stop"]:
                send_message(ADMIN_ID, "❌ **ضرب الستوب. نغلق الصفقة بخسارة صغيرة.**")
                trade["status"] = "closed"
            else:
                send_message(ADMIN_ID, f"✅ **الصفقة ما زالت ماشية…** السعر الحالي {price}$")
        elif trade["type"] == "sell":
            if price <= trade["target"]:
                send_message(ADMIN_ID, "🎯 **الهدف تحقق!** ✅ صفقة بيع ناجحة 🔥")
                trade["status"] = "closed"
            elif price >= trade["stop"]:
                send_message(ADMIN_ID, "❌ **ضرب الستوب. نغلق الصفقة بخسارة صغيرة.**")
                trade["status"] = "closed"
            else:
                send_message(ADMIN_ID, f"✅ **الصفقة ما زالت ماشية…** السعر الحالي {price}$")

# ✅ مراقبة السعر وفتح صفقات قوية فقط
def check_signals():
    global active_trade
    while True:
        try:
            price = get_gold_price()
            print(f"✅ السعر الآن: {price}")

            # 💥 لو ماكو صفقة مفتوحة، نبحث عن فرصة قوية
            if not active_trade or active_trade["status"] == "closed":
                # 🟢 شرط شراء قوي
                if price < 3310:
                    open_trade("buy", entry=price, target=price+8, stop=price-4,
                               reason="كسر دعم مهم + شمعة انعكاس صاعدة 🔥")
                # 🔴 شرط بيع قوي
                elif price > 3340:
                    open_trade("sell", entry=price, target=price-8, stop=price+4,
                               reason="اختراق مقاومة قوية وفشل بالتثبيت 🚨")

            else:
                # ✍️ إذا عندنا صفقة مفتوحة، نتابعها
                monitor_trade(price)

        except Exception as e:
            print("⚠️ Error:", e)

        time.sleep(60)  # ⏳ كل دقيقة يشيّك ويعلّق

# ✅ نشغّل الثريد الخلفي
threading.Thread(target=check_signals, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
