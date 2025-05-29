import telebot
import os
import json
import random
import time
import threading
import requests

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

USED_PROMOS_FILE = "used_promos.json"

PROMO_POOL = [
    "📱 Instagram / Facebook\n👩‍👧 “Mom, how do I say ‘I’m sick’ in Spanish?”\nI froze… until we found EspaLuz, our AI tutor for the whole family.\nNow even grandma is speaking with confidence. 💬💛\nTry it free: https://t.me/EspaLuzFamily_bot\n#EspaLuz #FamilySpanish #BilingualJourney",
    "🎬 YouTube Shorts Caption\nScene: Grandma lost in the market 🧓🛒\nVoice: “We thought she’d never learn. Now she shops solo in Spanish!”\n🎉 Meet EspaLuz — your bilingual family tutor: https://t.me/EspaLuzFamily_bot\n#EspaLuz #Shorts #LearnTogether",
    "🐦 Twitter Post\n“EspaLuz taught my 6yo ‘¿Dónde está el baño?’ faster than I could find it.” 🚽😂\nBilingual AI that teaches while you live life. https://t.me/EspaLuzFamily_bot\n#ParentingWithAI #EspaLuz",
    "📘 Facebook Post\nWhen we moved to Panama, none of us spoke Spanish.\nNow my daughter chats with our neighbors in the park — thanks to EspaLuz.\nTry it with your family → https://t.me/EspaLuzFamily_bot 💛 #FamilyLearning #EspaLuz"
]

def load_used_promos():
    if not os.path.exists(USED_PROMOS_FILE):
        with open(USED_PROMOS_FILE, "w") as f:
            json.dump([], f)
    with open(USED_PROMOS_FILE, "r") as f:
        return json.load(f)

def save_used_promos(used_promos):
    with open(USED_PROMOS_FILE, "w") as f:
        json.dump(used_promos, f, indent=2)

@bot.message_handler(commands=["daily_promo"])
def send_daily_promo(message):
    print("📣 /daily_promo triggered...")
    used_promos = load_used_promos()

    if len(used_promos) >= len(PROMO_POOL):
        bot.reply_to(message, "🎉 All current promos have been used! Please add more to the list.")
        return

    remaining_promos = [p for p in PROMO_POOL if p not in used_promos]
    promo = random.choice(remaining_promos)

    bot.reply_to(message, promo)
    used_promos.append(promo)
    save_used_promos(used_promos)
    print("✅ Promo sent and saved.")

@bot.message_handler(commands=["start"])
def welcome(message):
    print("👋 /start triggered.")
    bot.reply_to(message, "👋 Welcome to Influencer EspaLuz!\nUse /daily_promo to get your fresh promo post for today.")

# 🔪 Webhook Killer for Railway (polling only)
def webhook_killer():
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/deleteWebhook"
    while True:
        try:
            res = requests.get(url)
            print("🛡️ Webhook deletion result:", res.json())
        except Exception as e:
            print("❌ Error deleting webhook:", e)
        time.sleep(30)

threading.Thread(target=webhook_killer, daemon=True).start()

print("🤖 Influencer EspaLuz is running in polling mode...")
bot.polling(none_stop=True, timeout=30)
