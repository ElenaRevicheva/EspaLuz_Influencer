import telebot
import json
import os
import random

# Load agent config
with open("agent.json", "r", encoding="utf-8") as f:
    agent_config = json.load(f)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# On start
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(
        message,
        "👋 ¡Hola! I’m Influencer EspaLuz. Use /daily_promo to get a new social promo idea every day!"
    )

# On /daily_promo
@bot.message_handler(commands=["daily_promo"])
def handle_daily_promo(message):
    examples = agent_config.get("postExamples", [])
    if examples:
        promo = random.choice(examples)
        bot.reply_to(message, promo)
    else:
        bot.reply_to(message, "⚠️ No promo examples available in config.")

# Start polling
bot.polling()
