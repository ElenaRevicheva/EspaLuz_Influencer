import telebot
import os
import random
import time
import threading
import requests

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# === /daily_promo command with dynamic generation ===
@bot.message_handler(commands=["daily_promo"])
def send_daily_promo(message):
    print("📣 /daily_promo triggered...")

    platforms = ["Instagram", "Facebook", "Twitter", "YouTube Shorts", "TikTok"]
    situations = [
        "My daughter couldn't say 'hello' in Spanish… until we met EspaLuz!",
        "Grandma used to be shy at the market — now she shops in perfect Spanish!",
        "My son asked, '¿Dónde está el baño?' faster than I did 😂",
        "We moved to Panama knowing no Spanish — now we speak daily, thanks to EspaLuz.",
        "I was lost in translation at the pharmacy… then EspaLuz saved the day!"
    ]
    hashtags = ["#EspaLuz", "#FamilyLearning", "#AIforFamilies", "#BilingualJourney", "#LearnTogether"]

    platform = random.choice(platforms)
    situation = random.choice(situations)
    tags = " ".join(random.sample(hashtags, 2))

    promo = f"📣 {platform} Post\n{situation}\nTry EspaLuz today: https://t.me/EspaLuzFamily_bot\n{tags}"

    bot.reply_to(message, promo)
    print("✅ Dynamic promo sent.")

# === /start welcome message ===
@bot.message_handler(commands=["start"])
def welcome(message):
    print("👋 /start triggered.")
    bot.reply_to(message, "👋 Welcome to Influencer EspaLuz!\nUse /daily_promo to get your fresh promo post for today.")

# === Webhook Killer for Railway polling ===
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
