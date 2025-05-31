import telebot
import os
import random
import time
import threading
import requests

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

MAKE_WEBHOOK_URL = "https://hook.us2.make.com/fx857yhr46x4o2xrtaxatxja8yqxhfli"

VIDEO_URLS = [
    "https://www.dropbox.com/scl/fi/udxvy7b61fiib65lqfz23/video_cell.mp4?raw=1",
    "https://www.dropbox.com/scl/fi/1m5at6hbtxnomdfoks2x2/video_tv.mp4?raw=1"
]

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
    video_url = random.choice(VIDEO_URLS)

    promo = (
        f"📣 {platform} Post\n"
        f"{situation}\n"
        f"Try EspaLuz today: https://t.me/EspaLuzFamily_bot\n"
        f"{video_url}\n"
        f"{tags}"
    )

    bot.reply_to(message, promo)
    print("✅ Promo sent to Telegram chat.")

    try:
        payload = {
            "promoText": promo,
            "videoURL": video_url
        }
        response = requests.post(MAKE_WEBHOOK_URL, json=payload)
        print("📤 Sent promo to Make.com webhook. Response:", response.status_code)
    except Exception as e:
        print("❌ Failed to send to Make.com webhook:", e)

@bot.message_handler(commands=["start"])
def welcome(message):
    print("👋 /start triggered.")
    bot.reply_to(message, "👋 Welcome to Influencer EspaLuz!\nUse /daily_promo to get your fresh promo post for today.")

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
