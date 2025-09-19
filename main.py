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

MAKE_WEBHOOK_URL = "https://hook.us2.make.com/fx857yhr46x4o2xrtaxatxja8yqxhfli"

# Emotional Intelligence Engine webhook (for testing)
EMOTIONAL_AI_WEBHOOK_URL = "https://hook.us2.make.com/ecv7x7innu2g1r3olsqi12ca4uadkmi9"

# Backup webhook for alternative social media posting (if Buffer fails)
BACKUP_WEBHOOK_URL = "https://hook.us2.make.com/backup-webhook-url-here"

video_links = [
    "https://www.dropbox.com/scl/fi/olrb8clvbwqvp857rivtp/AI_Spanish_Coach_For_Parents.mp4?rlkey=24etrdri4rfhh52sbzwxicvny&st=cmkiczl5&dl=1",
    "https://youtube.com/shorts/4l9B4Rc1SxY?feature=share",
    "https://youtube.com/shorts/drlbgFu68tI?feature=share"
]

# Image URLs for Instagram posts
image_urls = [
    "https://raw.githubusercontent.com/ElenaRevicheva/EspaLuz_Influencer/main/converted_4x5_second_image.jpg",
    "https://raw.githubusercontent.com/ElenaRevicheva/EspaLuz_Influencer/main/converted_image_4x5.jpg",
    "https://raw.githubusercontent.com/ElenaRevicheva/EspaLuz_Influencer/main/espaluz_qr_4x5.jpg",
]

# Rich story templates with emotional AI hooks
story_templates = [
    {
        "hook": "🧠 AI THAT ACTUALLY GETS IT",
        "story": "I was having a meltdown trying to discipline my toddler in Spanish. I sent a frustrated voice message to EspaLuz: 'I don't know how to be firm but loving in Spanish!' The AI didn't just translate—it UNDERSTOOD I was a stressed parent and coached me through it.",
        "transformation": "EspaLuz analyzed my emotional state, gave me gentle parenting phrases in Spanish, and sent a personalized video showing me how to set boundaries with love. Now my daughter responds better, and I feel confident as a bilingual parent! 🎭💕",
        "emotion": "🤖 From robotic apps to EMOTIONAL AI"
    },
    {
        "hook": "🎬 THE CONVERSATION MODE MIRACLE",
        "story": "My husband and I were fighting about money—in English. Our Spanish neighbors could hear everything through thin walls, but we couldn't explain or apologize because of the language barrier. I felt so embarrassed and isolated.",
        "transformation": "I used EspaLuz's new Conversation Mode to practice what I wanted to say. Voice message → instant analysis → Spanish coaching → personalized motivation video. I knocked on their door, apologized in perfect Spanish, and we're now close friends! 🏠✨",
        "emotion": "💬 From isolation to CONNECTION"
    },
    {
        "hook": "🎯 THE BEDTIME BREAKTHROUGH",
        "story": "Bedtime was a nightmare. My 5-year-old only wanted Spanish lullabies like the local kids, but I felt ridiculous trying to sing in broken Spanish. She'd get frustrated and cry, 'Mami, you don't sound right!' My heart broke every night.",
        "transformation": "EspaLuz created a personalized video just for our bedtime routine! It taught me the lullabies with perfect pronunciation and gave me confidence-building phrases. Now she requests MY Spanish lullabies over anyone else's! 🌙🎵",
        "emotion": "🎭 From embarrassment to PRIDE"
    },
    {
        "hook": "💔 THE SCHOOL MEETING DISASTER",
        "story": "Parent-teacher conference in Spanish? I was terrified. I sat there nodding like a bobblehead while the teacher explained my son's behavior issues. I had no idea what was happening, couldn't ask questions, and felt like the worst parent ever.",
        "transformation": "Before the next meeting, I practiced with EspaLuz's emotional AI. It detected my anxiety, coached me through education vocabulary, and gave me a personalized pep-talk video. I advocated for my son like a champion—in fluent Spanish! 📚🏆",
        "emotion": "🛡️ From helpless to ADVOCATE"
    },
    {
        "hook": "🏥 THE EMERGENCY ROOM PANIC",
        "story": "My daughter fell and needed stitches. In the ER, surrounded by rapid Spanish, I couldn't explain her allergies or medical history. The doctors were frustrated, my daughter was scared, and I was completely useless when she needed me most.",
        "transformation": "Now I carry confidence everywhere. EspaLuz's emotional coaching taught me medical Spanish through real conversations, not just vocabulary lists. Last week, I calmly handled my son's fever appointment and even comforted another scared parent! 🏥💪",
        "emotion": "⚡ From panic to PREPARED"
    },
    {
        "hook": "🎉 THE FAMILY REUNION TRANSFORMATION",
        "story": "My husband's family reunion in Mexico was coming up. 40+ relatives, all speaking Spanish, and me—the gringa who smiles and waves. I dreaded being the outsider again, watching my kids connect with their heritage while I stood silent.",
        "transformation": "EspaLuz understood my family role and coached me through cultural conversations. At the reunion, I shared stories, asked about family history, and even helped cook with the abuelas. My mother-in-law cried and said I was 'truly family now.' 👨‍👩‍👧‍👦💕",
        "emotion": "🌟 From outsider to FAMILIA"
    },
    {
        "hook": "🛒 THE MARKET CONFIDENCE BOOST",
        "story": "The local mercado intimidated me. Vendors speaking fast Spanish, haggling I couldn't understand, and me pointing at things like a tourist. I was paying double what locals paid and everyone knew I didn't belong.",
        "transformation": "EspaLuz's conversation practice prepared me for real market interactions. Now vendors greet me by name, I negotiate prices confidently, and last week one vendor taught me his grandmother's secret spice blend—in Spanish! 🌶️🎯",
        "emotion": "💰 From tourist to LOCAL"
    },
    {
        "hook": "💕 THE DATE NIGHT GAME-CHANGER",
        "story": "My husband wanted to take Spanish dance lessons together, but I was too embarrassed about my pronunciation. 'What if I mess up the steps AND the language?' I kept making excuses, and our connection was suffering.",
        "transformation": "EspaLuz's emotional AI gave me confidence-building exercises and dance-specific Spanish phrases. Now we salsa every Friday night, I flirt with him in Spanish, and our relationship is stronger than ever! 💃🕺",
        "emotion": "💃 From insecurity to ROMANCE"
    }
]

# Revolutionary benefit points with emotional AI focus
benefit_sections = [
    {
        "title": "🧠 WORLD'S FIRST EMOTIONAL AI COACH",
        "points": [
            "🎭 Detects your emotional state and adapts responses accordingly",
            "👨‍👩‍👧‍👦 Recognizes your family role (parent, spouse, child) for targeted support",
            "💕 Provides empathy and encouragement, not just cold translations",
            "🎯 Coaches you through real family situations with emotional intelligence"
        ]
    },
    {
        "title": "🎬 LIVE CONVERSATION MODE (JUST DEPLOYED!)",
        "points": [
            "🎙️ Send voice messages → Instant transcription + emotional analysis",
            "🔄 Real-time Spanish/English audio with perfect message flow",
            "💬 Two-way family conversations with live AI coaching",
            "⚡ No waiting, no apps—works directly in WhatsApp"
        ]
    },
    {
        "title": "🎥 PERSONALIZED MOTIVATIONAL VIDEOS",
        "points": [
            "🎨 Custom Spanish videos tailored to YOUR exact conversation topic",
            "💪 Custom English videos for your specific emotional state",
            "⏰ 15-20 second inspiration when you need encouragement most",
            "🎯 Uses your conversation context—not generic motivation"
        ]
    },
    {
        "title": "👨‍👩‍👧‍👦 FAMILY-CENTERED LEARNING",
        "points": [
            "🏠 Designed for expat families in Panama, Mexico, Spain",
            "🍼 Real parenting phrases for bedtime, meals, discipline",
            "💑 Relationship Spanish for couples building bilingual connections",
            "🌟 Builds family bonds through language, not just vocabulary"
        ]
    },
    {
        "title": "🆚 BEYOND EVERY OTHER APP",
        "points": [
            "❌ Others: 'Say this phrase' → ✅ EspaLuz: 'I understand you're frustrated. Here's how to connect...'",
            "❌ Others: Generic lessons → ✅ EspaLuz: 'As a parent in Panama, you're modeling resilience'",
            "❌ Others: Cold translation → ✅ EspaLuz: Warm emotional coaching with Spanish learning",
            "❌ Others: One-size-fits-all → ✅ EspaLuz: Personalized videos for YOUR family situation"
        ]
    }
]

# Truthful call-to-action variations with correct EspaLuz links
cta_options = [
    "🧠 Ready for an AI that actually understands your family's emotions?\n✅ Telegram: https://t.me/EspaLuzFamily_bot\n✅ WhatsApp: https://wa.me/50766623757\n🤖 AI Family Companion for Learning Spanish On-The-Go!",
    "💕 Your family deserves connection, not just translation. Start your emotional Spanish journey:\n✅ Try Telegram: https://t.me/EspaLuzFamily_bot\n✅ Try WhatsApp: https://wa.me/50766623757\n🎁 AI Family Companion - Start FREE!",
    "🎬 Experience the world's first emotionally intelligent Spanish coach:\n✅ Live Conversation Mode ✅ Personalized Videos ✅ Family-Focused AI\n📱 Telegram: https://t.me/EspaLuzFamily_bot\n📱 WhatsApp: https://wa.me/50766623757",
    "🌟 Stop settling for robotic language apps. EspaLuz understands your heart, not just your words.\n💙 Join expat families building deeper connections through Spanish.\n✅ Telegram: https://t.me/EspaLuzFamily_bot | ✅ WhatsApp: https://wa.me/50766623757",
    "👨‍👩‍👧‍👦 'It's not just Spanish lessons—it's family therapy that teaches Spanish.'\n🧠 Emotional AI + Conversation Mode + Personalized Videos = Your bilingual breakthrough\n🚀 Start FREE: ✅ Telegram: https://t.me/EspaLuzFamily_bot ✅ WhatsApp: https://wa.me/50766623757",
    "🎭 From frustrated parent to confident bilingual family—EspaLuz makes it possible.\n🤖 AI Family Companion for Learning Spanish On-The-Go\n📲 Choose your platform: ✅ Telegram: https://t.me/EspaLuzFamily_bot ✅ WhatsApp: https://wa.me/50766623757"
]

# Emotional AI social proof testimonials
social_proof = [
    "🧠 'The AI detected I was stressed about parenting and gave me exactly the Spanish phrases I needed to connect with my daughter. It's like having a bilingual therapist!' - Sarah, expat mom in Panama",
    "🎬 'Conversation Mode changed everything. I sent a panicked voice message about my son's school meeting, and EspaLuz coached me through the whole thing with personalized videos!' - Mike, Panama City",
    "💕 'My husband's family finally accepts me. EspaLuz understood I felt like an outsider and taught me cultural Spanish, not just words.' - Jennifer, married to Mexican national",
    "🎭 'The AI knew I was embarrassed about my pronunciation and sent me confidence-building exercises. Now I sing Spanish lullabies to my kids!' - Amanda, bilingual family",
    "⚡ 'EspaLuz detected my anxiety about medical appointments and prepared me with doctor-specific Spanish. I advocated for my mom like a pro!' - Carlos, caring for elderly parent",
    "🌟 'It's not just translation—it's emotional support. The AI celebrates my wins and encourages me through frustrations. Like having a Spanish-speaking best friend!' - Lisa, solo expat",
    "👨‍👩‍👧‍👦 'Our family went from language barriers to bilingual bonding. EspaLuz understood our dynamics and coached us all differently.' - The Rodriguez Family, 3 generations",
    "🎯 'I was paying tourist prices at the market until EspaLuz taught me confident haggling Spanish. Now vendors treat me like family!' - Tom, digital nomad in Mexico"
]

# Platform-specific hashtag sets for emotional AI positioning
hashtag_sets = [
    # Instagram/Facebook - Emotional AI Focus
    ["#EspaLuz", "#EmotionalAI", "#BilingualFamilies", "#ConversationMode", "#SpanishWithHeart", "#FamilyFirst", "#ExpatLife"],
    
    # TikTok - Trending + Features
    ["#EspaLuz", "#AICoach", "#SpanishTok", "#ExpatTok", "#BilingualJourney", "#FamilyGoals", "#LanguageLearning", "#EmotionalIntelligence"],
    
    # Twitter/X - Professional + Innovation
    ["#EspaLuz", "#EmotionalAI", "#ConversationMode", "#AIInnovation", "#SpanishLearning", "#ExpatFamilies", "#WhatsAppAI"],
    
    # YouTube - Educational + Family
    ["#EspaLuz", "#SpanishForFamilies", "#EmotionalAI", "#BilingualParenting", "#ConversationMode", "#ExpatLife", "#FamilyLearning"],
    
    # LinkedIn - Professional Expat Focus
    ["#EspaLuz", "#ExpatLife", "#BilingualProfessionals", "#EmotionalAI", "#WorkingAbroad", "#SpanishBusiness", "#GlobalFamilies"],
    
    # General Emotional Positioning
    ["#EspaLuz", "#EmotionalIntelligence", "#FamilyConnection", "#SpanishWithEmpathy", "#BilingualBonding", "#AIThatCares", "#HeartfeltLearning"],
    
    # Panama/Mexico Specific
    ["#EspaLuz", "#PanamaExpats", "#MexicoLife", "#SpainLife", "#LatinAmericaLife", "#ExpatFamilies", "#BilingualKids", "#CulturalIntegration"],
    
    # Feature-Specific
    ["#EspaLuz", "#ConversationMode", "#PersonalizedVideos", "#VoiceToText", "#WhatsAppLearning", "#NoAppNeeded", "#InstantTranslation"]
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
        
        # Send to Make.com webhook with emotional intelligence data
        payload = {
            "text": promo,
            "videoURL": video_url,
            "imageURL": image_url,
            "videoTitle": f"EspaLuz Success Story: {story['emotion']}",
            "videoDescription": story['story'][:200] + "...",
            "automated": True,
            "timestamp": datetime.now(pytz.timezone('America/Panama')).isoformat(),
            # Emotional Intelligence Data
            "hook": story['hook'],
            "story": story['story'],
            "emotion": story['emotion'],
            "transformation": story['transformation'],
            "cta": cta,
            "hashtags": " ".join(hashtags),
            "socialProof": proof
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
            "text": promo,
            "videoURL": video_url,
            "imageURL": image_url,
            "videoTitle": f"EspaLuz Success Story: {story['emotion']}",
            "videoDescription": story['story'][:200] + "...",
            "automated": False,
            # Emotional Intelligence Data
            "hook": story['hook'],
            "story": story['story'],
            "emotion": story['emotion'],
            "transformation": story['transformation'],
            "cta": cta,
            "hashtags": " ".join(hashtags),
            "socialProof": proof
        }
        response = requests.post(MAKE_WEBHOOK_URL, json=payload)
        print("📤 Sent promo to Make.com webhook. Response:", response.status_code)
    except Exception as e:
        print("❌ Failed to send to Make.com webhook:", e)

@bot.message_handler(commands=["start"])
def welcome(message):
    print("👋 /start triggered.")
    bot.reply_to(message, "👋 Welcome to Influencer EspaLuz!\nUse /daily_promo to get your fresh promo post for today.\nUse /test_time to check current times.")

@bot.message_handler(commands=["test_time"])
def test_time(message):
    """Test command to check current times and next scheduled run"""
    panama_tz = pytz.timezone('America/Panama')
    current_panama_time = datetime.now(panama_tz)
    server_time = datetime.now()
    next_run = schedule.next_run()
    
    time_info = f"""🕐 **TIME CHECK**
    
🌍 **Server time (Railway)**: {server_time.strftime('%Y-%m-%d %H:%M:%S %Z')}
🇵🇦 **Panama time**: {current_panama_time.strftime('%Y-%m-%d %H:%M:%S %Z')}
📅 **Next scheduled promo**: {next_run}
⏰ **Scheduled for**: 4:55 PM Panama time daily

*Note: Railway servers typically use UTC timezone.*"""
    
    bot.reply_to(message, time_info)
    print(f"📊 Time check requested by user: {message.from_user.username}")

@bot.message_handler(commands=["test_emotional_ai"])
def test_emotional_ai(message):
    """Test command for emotional AI engine"""
    print("🧠 /test_emotional_ai triggered...")
    
    promo, story, video_url, image_url = generate_promo_content()
    
    # Reply to the user who triggered the command
    bot.reply_to(message, f"🧠 **EMOTIONAL AI TEST**\n\nDetected emotion: {story['emotion']}\n\nContent generated and sent to Emotional AI webhook for testing!\n\nCheck Make.com for results.")
    
    try:
        payload = {
            "text": promo,
            "videoURL": video_url,
            "imageURL": image_url,
            "videoTitle": f"EspaLuz Success Story: {story['emotion']}",
            "videoDescription": story['story'][:200] + "...",
            "automated": False,
            "testMode": True,
            # Emotional Intelligence Data
            "hook": story['hook'],
            "story": story['story'],
            "emotion": story['emotion'],
            "transformation": story['transformation'],
            "cta": random.choice(cta_options),
            "hashtags": " ".join(random.choice(hashtag_sets)),
            "socialProof": random.choice(social_proof)
        }
        
        # Send to Emotional AI webhook (when URL is configured)
        if "REPLACE_WITH_NEW_WEBHOOK_URL" not in EMOTIONAL_AI_WEBHOOK_URL:
            response = requests.post(EMOTIONAL_AI_WEBHOOK_URL, json=payload)
            print(f"🧠 Sent to Emotional AI webhook. Response: {response.status_code}")
        else:
            print("⚠️ Emotional AI webhook URL not configured yet")
            
    except Exception as e:
        print(f"❌ Failed to send to Emotional AI webhook: {e}")

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

# Schedule daily promo for 4:55 PM Panama time (21:55 UTC since Panama is UTC-5)
schedule.every().day.at("21:55").do(send_automated_daily_promo)

# TEMPORARY: One-time test for tonight at 5:45 PM Panama time (22:45 UTC)
schedule.every().day.at("22:45").do(send_automated_daily_promo)

print("⏰ Scheduled daily promo for 4:55 PM Panama time (21:55 UTC)")
print("🧪 TEMPORARY: Test promo scheduled for 5:45 PM Panama time (22:45 UTC) - tonight only")

# Display timezone information for debugging
panama_tz = pytz.timezone('America/Panama')
current_panama_time = datetime.now(panama_tz)
server_time = datetime.now()

print(f"🌍 Server time (Railway): {server_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
print(f"🇵🇦 Panama time: {current_panama_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")

# Start background threads  
threading.Thread(target=schedule_checker, daemon=True).start()

print("🤖 Influencer EspaLuz is running with polling mode...")
print("📅 Next scheduled promo:", schedule.next_run())

# Run the bot with enhanced conflict resolution
keep_alive()
