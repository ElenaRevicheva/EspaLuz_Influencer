import telebot
import os
import random
import time
import threading
import requests
import schedule
from datetime import datetime
import pytz

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = "@EspaLuz"  # Your channel
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

MAKE_WEBHOOK_URL = "https://hook.us2.make.com/fx857yhr464o2xrtaxatxja8yqxhfli"

video_links = [
    "https://youtube.com/shorts/4l9B4Rc1SxY?feature=share",
    "https://youtube.com/shorts/drlbgFu68tI?feature=share"
]

# Image URLs for Instagram posts
image_urls = [
    "https://raw.githubusercontent.com/ElenaRevicheva/EspaLuz_Influencer/main/converted_4x5_second_image.jpg",
    "https://raw.githubusercontent.com/ElenaRevicheva/EspaLuz_Influencer/main/converted_image_4x5.jpg",
    "https://raw.githubusercontent.com/ElenaRevicheva/EspaLuz_Influencer/main/espaluz_qr_4x5.jpg",
]

# Rich story templates with emotional hooks
story_templates = [
    {
        "hook": "🚨 PANIC MODE ACTIVATED",
        "story": "Picture this: I'm at the pharmacy in Panama, my daughter has a fever, and I'm frantically pointing at medicine bottles like I'm playing charades. The pharmacist is speaking rapid-fire Spanish, I'm sweating bullets, and my daughter is crying...",
        "transformation": "Fast forward 3 months with EspaLuz: I walked into that SAME pharmacy, confidently asked for 'medicina para la fiebre infantil,' and even cracked a joke with the pharmacist. My daughter was amazed—and so was I! 🏆",
        "emotion": "💪 From panic to CONFIDENCE"
    },
    {
        "hook": "😭 THE GROCERY STORE MELTDOWN",
        "story": "My 8-year-old son wanted to buy his favorite cookies at the local tienda. He approached the counter with his pocket money, froze completely when the cashier spoke in Spanish, and ran back to me in tears. As a parent, watching your kid feel defeated like that... it breaks your heart.",
        "transformation": "Yesterday, that same little boy marched up to the counter, asked '¿Cuánto cuesta estas galletas?' with the biggest smile, and even said '¡Gracias!' without prompting. The cashier complimented his Spanish! 🍪✨",
        "emotion": "❤️ From tears to TRIUMPH"
    },
    {
        "hook": "🏠 THE NEIGHBOR SITUATION",
        "story": "Our sweet 70-year-old neighbor Doña Carmen kept bringing us homemade tamales and trying to chat. For MONTHS, all I could do was smile, nod, and feel terrible that I couldn't connect with this amazing woman who was trying so hard to welcome our family.",
        "transformation": "Last week, I surprised Doña Carmen by asking for her tamale recipe—in Spanish! We spent an hour laughing and cooking together. She hugged me and said I was 'como familia.' I literally cried happy tears. 🫔💕",
        "emotion": "🤗 From isolation to FAMILY"
    },
    {
        "hook": "🎂 THE BIRTHDAY PARTY DISASTER",
        "story": "My daughter got invited to her first local birthday party. She was SO excited... until she realized she'd be the only kid who couldn't speak Spanish. She begged me not to make her go. Seeing your child choose isolation over fun because of a language barrier? That's a wake-up call.",
        "transformation": "Three months later, she's not just attending parties—she's LEADING the games! Last weekend, she taught all the kids a Spanish song she learned through EspaLuz. She's become the bridge between worlds. 🌉🎉",
        "emotion": "🌟 From isolation to LEADERSHIP"
    },
    {
        "hook": "🚗 THE UBER AWKWARDNESS",
        "story": "Every Uber ride was 20 minutes of painful silence. Drivers would try to make conversation, I'd give one-word responses, and you could cut the awkwardness with a knife. I felt like I was being rude, but what else could I do?",
        "transformation": "Now Uber drivers and I chat about everything—family, food, local spots, even politics! Last week, a driver said I speak Spanish 'mejor que algunos panameños.' We became friends and he's taking our family to his favorite beach this weekend! 🏖️",
        "emotion": "🗣️ From silence to FRIENDSHIP"
    },
    {
        "hook": "🏥 THE DOCTOR'S OFFICE PANIC",
        "story": "Taking grandma to her doctor appointment was a nightmare. Medical terminology in Spanish? Forget about it. I was using Google Translate for everything, the doctor was frustrated, grandma was scared, and I felt like the worst grandson ever for not being able to help her properly.",
        "transformation": "Last month's appointment? I translated everything perfectly, asked detailed questions about her medications, and even advocated for a second opinion—all in fluent Spanish. Grandma squeezed my hand and said she felt safe. That's everything. 👵💙",
        "emotion": "🛡️ From helpless to HERO"
    }
]

# Compelling benefit points with social proof
benefit_sections = [
    {
        "title": "🎯 INSTANT REAL-WORLD HELP",
        "points": [
            "📸 Snap a photo of ANY text → Get instant translation + pronunciation",
            "🎙️ Speak naturally → EspaLuz understands your intent, not just words",
            "⚡ Real-time help in restaurants, stores, appointments—anywhere you need it"
        ]
    },
    {
        "title": "👨‍👩‍👧‍👦 FAMILY-FIRST APPROACH",
        "points": [
            "🧠 Remembers each family member's learning style and progress",
            "💝 Adapts to your emotions—patient when you're frustrated, excited when you succeed",
            "🎭 Creates personalized avatar videos that kids actually WANT to watch"
        ]
    },
    {
        "title": "🚀 BEYOND BASIC TRANSLATION",
        "points": [
            "🎨 Cultural context—learn WHY Spanish speakers say things certain ways",
            "🔊 Natural pronunciation coaching with instant feedback",
            "💬 Conversational practice that feels like talking to a bilingual friend"
        ]
    }
]

# Call-to-action variations
cta_options = [
    "🔥 Don't let language barriers steal another moment from your family. Try EspaLuz FREE today!",
    "💎 Your family's breakthrough moment is one conversation away. Start with EspaLuz now!",
    "⚡ Stop letting language hold your family back. EspaLuz is waiting to help—for FREE!",
    "🎯 Ready to turn your family's biggest struggle into your greatest strength? EspaLuz starts here:",
    "🌟 Your confident, bilingual family story starts with one click. Try EspaLuz FREE:"
]

# Social proof elements
social_proof = [
    "💬 'My kids now dream in Spanish!' - Maria, Panama City",
    "🏆 'We went from tourists to locals in 2 months' - The Johnson Family",
    "❤️ 'EspaLuz saved our family relationships' - Carlos, expat dad",
    "🌟 'Even abuela is using it now!' - Sofia, 3-generation household",
    "🎉 'Our Spanish is better than our neighbors who've lived here 5 years' - The Smiths"
]

# Hashtag combinations for different platforms
hashtag_sets = [
    ["#EspaLuz", "#FamilyFirst", "#BilingualJourney", "#PanamaLife", "#ExpatFamilies"],
    ["#LearnTogether", "#SpanishForFamilies", "#AITutor", "#ConfidentKids", "#CulturalBridge"],
    ["#FamilyLearning", "#SpanishSuccess", "#NoMoreBarriers", "#EmpoweredFamilies", "#BilingualHome"],
    ["#LanguageMagic", "#FamilyGoals", "#SpanishMadeEasy", "#ConnectedFamilies", "#CulturalFluency"]
]

def generate_promo_content():
    """Generate promo content without needing a message object"""
    print("🎬 Generating automated daily promo...")
    
    # Select random elements
    story = random.choice(story_templates)
    benefits = random.sample(benefit_sections, 2)  # Pick 2 benefit sections
    cta = random.choice(cta_options)
    proof = random.choice(social_proof)
    hashtags = " ".join(random.choice(hashtag_sets))
    video_url = random.choice(video_links)
    image_url = random.choice(image_urls)
    
    # Debug: Print which video and image were selected
    print(f"🎬 Selected video: {video_url}")
    print(f"🖼️ Selected image: {image_url}")

    # Build rich promo content
    promo = f"""{story['hook']} 🚨

{story['story']}

{story['transformation']}

{story['emotion']} — That's the EspaLuz difference! ✨

━━━━━━━━━━━━━━━━━━━━━━━

🔥 WHY 2,000+ FAMILIES CHOOSE ESPALUZ:

{benefits[0]['title']}
{''.join([f"   {point}" for point in benefits[0]['points']])}

{benefits[1]['title']}
{''.join([f"   {point}" for point in benefits[1]['points']])}

━━━━━━━━━━━━━━━━━━━━━━━

{proof}

{cta}
👇 https://t.me/EspaLuzFamily_bot

🎥 Long Story Short:
{video_url}

{hashtags}

P.S. Your family's Spanish breakthrough is closer than you think. Don't wait—every day without EspaLuz is a missed conversation, a lost connection, a moment your family could be thriving instead of just surviving. Start today. Your future bilingual selves will thank you! 💕"""

    return promo, story, video_url, image_url

def send_automated_daily_promo():
    """Automated version that posts to specific chat and webhook"""
    try:
        promo, story, video_url, image_url = generate_promo_content()
        
        # Send to Telegram channel
        bot.send_message(TELEGRAM_CHAT_ID, promo)
        print("✅ Automated promo sent to @EspaLuz channel.")
        
        # Send to Make.com webhook
        payload = {
            "promoText": promo,
            "videoURL": video_url,
            "imageURL": image_url,
            "videoTitle": f"EspaLuz Success Story: {story['emotion']}",
            "videoDescription": story['story'][:200] + "...",
            "automated": True,
            "timestamp": datetime.now(pytz.timezone('America/Panama')).isoformat()
        }
        response = requests.post(MAKE_WEBHOOK_URL, json=payload)
        print(f"📤 Automated promo sent to Make.com webhook. Response: {response.status_code}")
        
    except Exception as e:
        print(f"❌ Error in automated promo: {e}")

@bot.message_handler(commands=["daily_promo"])
def send_daily_promo(message):
    print("📣 /daily_promo triggered manually...")
    
    promo, story, video_url, image_url = generate_promo_content()

    # Reply to the user who triggered the command
    bot.reply_to(message, promo)
    
    # Also send to the @EspaLuz channel
    bot.send_message(TELEGRAM_CHAT_ID, promo)
    print("✅ Manual promo sent to Telegram chat and @EspaLuz channel.")

    try:
        payload = {
            "promoText": promo,
            "videoURL": video_url,
            "imageURL": image_url,
            "videoTitle": f"EspaLuz Success Story: {story['emotion']}",
            "videoDescription": story['story'][:200] + "...",
            "automated": False
        }
        response = requests.post(MAKE_WEBHOOK_URL, json=payload)
        print("📤 Sent promo to Make.com webhook. Response:", response.status_code)
    except Exception as e:
        print("❌ Failed to send to Make.com webhook:", e)

@bot.message_handler(commands=["start"])
def welcome(message):
    print("👋 /start triggered.")
    bot.reply_to(message, "👋 Welcome to Influencer EspaLuz!\nUse /daily_promo to get your fresh promo post for today.")

def schedule_checker():
    """Run scheduled tasks in a separate thread"""
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
        except Exception as e:
            print(f"❌ Schedule checker error: {e}")
            time.sleep(60)

def webhook_killer():
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/deleteWebhook"
    while True:
        try:
            res = requests.get(url)
            print("🛡️ Webhook deletion result:", res.json())
        except Exception as e:
            print("❌ Error deleting webhook:", e)
        time.sleep(30)

def force_single_instance():
    """Ensure only one bot instance is running"""
    try:
        # Aggressively clear any existing connections
        bot.remove_webhook()
        time.sleep(2)
        
        # Force delete webhook multiple times
        for i in range(3):
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/deleteWebhook"
            requests.get(url)
            time.sleep(1)
            
        print("🧹 Cleared all webhook connections")
        
        # Add random delay to avoid simultaneous startups
        import random
        delay = random.uniform(1, 5)
        print(f"⏳ Random startup delay: {delay:.1f} seconds")
        time.sleep(delay)
        
    except Exception as e:
        print(f"⚠️ Cleanup error: {e}")

def keep_alive():
    """Keep the bot running with better conflict resolution"""
    while True:
        try:
            print("🤖 Starting bot polling...")
            bot.polling(none_stop=True, timeout=30, long_polling_timeout=30)
        except Exception as e:
            if "409" in str(e):
                print("⚠️ Bot conflict detected - waiting longer before restart...")
                time.sleep(30)  # Wait longer for other instances to die
                force_single_instance()
            else:
                print(f"❌ Bot polling error: {e}")
            print("🔄 Restarting bot in 15 seconds...")
            time.sleep(15)

# Force cleanup at startup
force_single_instance()

# Schedule daily promo for 1:00 PM Panama time
schedule.every().day.at("13:00").do(send_automated_daily_promo)

print("⏰ Scheduled daily promo for 1:00 PM Panama time")

# Start background threads  
threading.Thread(target=schedule_checker, daemon=True).start()

print("🤖 Influencer EspaLuz is running with polling mode...")
print("📅 Next scheduled promo:", schedule.next_run())

# Run the bot with enhanced conflict resolution
keep_alive()
