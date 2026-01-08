"""
🤖 ESPALUZ AI INFLUENCER CO-FOUNDER v2.0
=========================================
Upgraded from template-based to AI-generated content.
Now powered by Groq (Llama 3.3 70B) for real emotional intelligence.

PRESERVED:
- Make.com webhook trigger mechanism
- Daily scheduling via schedule library
- Telegram bot commands
- Payload structure for Make.com

UPGRADED:
- AI-generated stories (no more templates)
- Real emotional intelligence
- Fresh, unique content every day
- EspaLuz brand voice understanding

Author: Elena Revicheva & CTO AIPA
Version: 2.0.0
"""

import telebot
import os
import random
import time
import threading
import requests
import schedule
import json
from datetime import datetime
import pytz

# ============================================
# CONFIGURATION
# ============================================

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = "@EspaLuz"  # Your channel
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

MAKE_WEBHOOK_URL = "https://hook.us2.make.com/ecv7x7innu2g1r3olsqi12ca4uadkmi9"
EMOTIONAL_AI_WEBHOOK_URL = "https://hook.us2.make.com/ecv7x7innu2g1r3olsqi12ca4uadkmi9"

# AI Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# ============================================
# MEDIA ASSETS
# ============================================

video_links = [
    "https://youtube.com/shorts/-0bw32yzD4Y?si=zfbYJCyRkcVFKdpw",
    "https://youtube.com/shorts/I3H4V0G-ZtQ?si=D2sbtkGuQ-z87AKm",
    "https://youtube.com/shorts/O4a2g3cDDxA?si=AH6qC1f_zWAI2b4G",
    "https://youtu.be/z2gP6YyEoUs?si=AI7HgtEYxAqMqAFE",
    "https://youtu.be/scmnutn6Vs4?si=IqrMGHJZO0Cnx9M8",
    "https://youtube.com/shorts/Y2dhzKlv4J4?si=mSethuhB7-ebjs3q"
]

image_urls = [
    "https://raw.githubusercontent.com/ElenaRevicheva/EspaLuz_Influencer/main/espaluz_qr_4x5.jpg",
    "https://raw.githubusercontent.com/ElenaRevicheva/EspaLuz_Influencer/main/image1.jpg",
    "https://raw.githubusercontent.com/ElenaRevicheva/EspaLuz_Influencer/main/image2.jpg",
    "https://raw.githubusercontent.com/ElenaRevicheva/EspaLuz_Influencer/main/image3.jpg",
    "https://raw.githubusercontent.com/ElenaRevicheva/EspaLuz_Influencer/main/image4.jpg",
    "https://raw.githubusercontent.com/ElenaRevicheva/EspaLuz_Influencer/main/image5.jpg"
]

# ============================================
# ESPALUZ BRAND KNOWLEDGE (AI CONTEXT)
# ============================================

ESPALUZ_BRAND_KNOWLEDGE = """
# ESPALUZ - AI Spanish/English Tutor
## Brand Identity
EspaLuz is an AI-powered bilingual tutor on WhatsApp that uses emotional intelligence to help people learn Spanish and English. We're not just an app—we're a breakthrough companion that understands the emotional journey of language learning.

## ACTUAL PRODUCT FEATURES (use these!):
🗣️ **CONVERSATION MODE** - Type "conversation" for intelligent family conversation practice (MAIN FEATURE!)
🧠 **Emotional AI** - Analyzes emotions (frustrated, excited, homesick) and adapts responses
🎤 **Voice Messages** - Send voice in any language, get audio responses back
📸 **Photo Translation** - Send photos of menus, signs, documents for instant translation
🎥 **Personalized Video Responses** - Custom video explanations
👨‍👩‍👧‍👦 **Family Personalization** - Learns family names, preferences, dynamics
🌍 **19 Countries** - Cultural context for all Spanish-speaking countries
🌐 **Trilingual** - Russian, Spanish, AND English support

## PRICING (CORRECT!):
- 🆓 **7-DAY FREE TRIAL** - Full access to all features
- 💰 **$7.77/month via PayPal** - BONUS: 1 extra week FREE after subscription!
- PayPal link: https://www.paypal.com/webapps/billing/plans/subscribe?plan_id=P-38A73508FY163121MNCJXTYY

## Target Audiences (rotate between these):
1. **Expat Parents** - American/European families in Latin America (especially Panama!)
2. **Digital Nomads** - Remote workers needing professional Spanish
3. **Service Providers** - Tour guides, taxi drivers learning English to increase income
4. **Business Travelers** - Executives needing confident Spanish for negotiations
5. **Cultural Explorers** - Travelers seeking authentic local connections
6. **Healthcare Workers** - Nurses/doctors needing medical Spanish
7. **Entrepreneurs** - Starting businesses in Spanish-speaking markets
8. **Retirees** - Moving to Latin America for better quality of life
9. **Teachers** - Bilingual educators
10. **Immigrants** - Spanish speakers learning English in the US
11. **Russian Speakers** - Learning Spanish/English (trilingual support!)

## Emotional States to Address:
- **Frustration**: Can't communicate when it matters most
- **Embarrassment**: Made mistakes that felt humiliating
- **Isolation**: Feeling like an outsider despite living there
- **Anxiety**: Scared of speaking and making errors
- **Breakthrough**: Finally having a confident conversation
- **Connection**: Building real relationships through language
- **Empowerment**: Advocating for yourself and family
- **Homesickness**: Missing home, adapting to new culture

## Key Differentiators:
1. **Conversation Mode** - Practice real family conversations with intelligent AI
2. **Emotional Intelligence** - AI detects and adapts to your emotional state
3. **WhatsApp Native** - No app download, just message on WhatsApp
4. **Voice-First** - Send voice messages, get voice responses
5. **Photo Recognition** - Snap a photo, get instant translation
6. **Family-Aware** - Understands parent/child dynamics
7. **Cultural Context** - 19 Spanish-speaking countries
8. **Affordable** - $7.77/month with FREE trial

## Contact:
WhatsApp: +507 6662 3757
Website: https://espaluz-ai-language-tutor.lovable.app

## Tone of Voice:
- Warm, empathetic, understanding
- Shares real transformation stories
- Never judgmental about mistakes
- Celebrates small wins
- Uses emojis authentically (not excessively)
- Speaks to the emotional pain points
- Highlights FREE TRIAL and low price
"""

# ============================================
# AI STORY GENERATION
# ============================================

def generate_ai_story():
    """Generate a fresh story using Groq AI"""
    
    # Select random audience and emotional state for variety
    audiences = [
        "expat_parent", "digital_nomad", "service_provider", "business_traveler",
        "cultural_explorer", "healthcare_worker", "entrepreneur", "retiree", "teacher", "immigrant"
    ]
    
    emotional_states = [
        "desperate_frustration", "crushing_embarrassment", "breakthrough_euphoria",
        "empowering_confidence", "local_acceptance", "career_breakthrough", "family_connection"
    ]
    
    selected_audience = random.choice(audiences)
    selected_emotion = random.choice(emotional_states)
    
    # Current date for context
    current_date = datetime.now().strftime("%B %d, %Y")
    
    prompt = f"""You are the AI Marketing Co-Founder for EspaLuz, an AI Spanish/English tutor.

BRAND KNOWLEDGE:
{ESPALUZ_BRAND_KNOWLEDGE}

TODAY'S CONTENT ASSIGNMENT:
- Date: {current_date}
- Target Audience: {selected_audience.replace('_', ' ').title()}
- Emotional Arc: Start with {selected_emotion.replace('_', ' ')} → Transform to confidence/breakthrough

GENERATE A SOCIAL MEDIA STORY with these exact components:

1. **HOOK** (1 line with emoji): Attention-grabbing opening that stops the scroll
2. **STORY** (3-5 sentences): A specific, relatable scenario this audience faces. Use first-person perspective. Include sensory details and emotional honesty.
3. **TRANSFORMATION** (2-3 sentences): How EspaLuz helped solve this specific problem. Be specific about what the AI did.
4. **EMOTION** (1 line with emoji): The before → after emotional shift

RULES:
- Make it feel REAL, not generic
- Include specific details (cities, situations, exact feelings)
- Show vulnerability then triumph
- Make the reader think "That's EXACTLY what happened to me!"
- Keep total length under 250 words
- Don't mention the audience name explicitly
- CTA: https://wa.me/50766623757

Output as valid JSON with keys: hook, story, transformation, emotion, audience, emotional_state"""

    try:
        response = requests.post(
            GROQ_API_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.9,
                "max_tokens": 1000
            },
            timeout=30
        )
        
        if response.status_code == 200:
            content = response.json()['choices'][0]['message']['content']
            
            # Parse JSON from response
            # Handle markdown code blocks if present
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            
            story_data = json.loads(content.strip())
            story_data['audience'] = selected_audience
            story_data['emotional_state'] = selected_emotion
            
            print(f"🧠 AI generated story for: {selected_audience}")
            return story_data
        else:
            print(f"❌ Groq API error: {response.status_code} - {response.text}")
            return None
            
    except json.JSONDecodeError as e:
        print(f"❌ JSON parse error: {e}")
        print(f"Raw content: {content[:500] if 'content' in dir() else 'N/A'}")
        return None
    except Exception as e:
        print(f"❌ AI generation error: {e}")
        return None

# ============================================
# FALLBACK TEMPLATES (in case AI fails)
# ============================================

FALLBACK_STORIES = [
    {
        "hook": "🧠 AI THAT ACTUALLY GETS IT",
        "story": "I was having a meltdown trying to discipline my toddler in Spanish. I sent a frustrated voice message to EspaLuz: 'I don't know how to be firm but loving in Spanish!' The AI didn't just translate—it UNDERSTOOD I was a stressed parent and coached me through it.",
        "transformation": "EspaLuz analyzed my emotional state, gave me gentle parenting phrases in Spanish, and sent a personalized video showing me how to set boundaries with love. Now my daughter responds better, and I feel confident as a bilingual parent! 🎭💕",
        "emotion": "🤖 From robotic apps to EMOTIONAL AI",
        "audience": "expat_parent",
        "emotional_state": "desperate_frustration"
    },
    {
        "hook": "💻 REMOTE WORK BREAKTHROUGH",
        "story": "Client call disaster in Mexico City. My Spanish wasn't good enough for the business presentation, and I was losing a $50K contract. I felt like a fraud calling myself 'location independent' when I couldn't even communicate professionally.",
        "transformation": "EspaLuz's business Spanish module didn't just teach me phrases—it understood my professional anxiety and coached me through confident business communication. I nailed the follow-up presentation and landed the contract!",
        "emotion": "💼 From imposter syndrome to PROFESSIONAL CONFIDENCE",
        "audience": "digital_nomad",
        "emotional_state": "career_breakthrough"
    },
    {
        "hook": "🏥 LIFE-SAVING COMMUNICATION",
        "story": "Emergency room nurse in Miami. Spanish-speaking patient having chest pains, but I couldn't understand her symptoms description. I had to rely on Google Translate while she was in distress. I felt helpless when lives depended on clear communication.",
        "transformation": "EspaLuz created medical Spanish modules that understood the emotional weight of healthcare communication. It taught me not just medical terms, but how to provide comfort and confidence to scared patients. Now I'm the go-to nurse for Spanish-speaking emergencies.",
        "emotion": "🩺 From helpless to HEALTHCARE HERO",
        "audience": "healthcare_worker",
        "emotional_state": "empowering_confidence"
    }
]

# ============================================
# CONTENT GENERATION (preserves Make.com interface)
# ============================================

# Benefit sections (kept from original)
benefit_sections = [
    {
        "title": "🗣️ CONVERSATION MODE",
        "points": [
            "\n   ✅ Practice real family conversations",
            "\n   ✅ AI adapts to your emotional state",
            "\n   ✅ Perfect for expat families"
        ]
    },
    {
        "title": "🎤 VOICE & PHOTO MAGIC",
        "points": [
            "\n   ✅ Send voice messages, get audio back",
            "\n   ✅ Snap photos of menus for instant translation",
            "\n   ✅ Video responses for complex topics"
        ]
    },
    {
        "title": "🧠 EMOTIONALLY INTELLIGENT",
        "points": [
            "\n   ✅ Senses when you're frustrated and adapts",
            "\n   ✅ Understands homesickness & culture shock",
            "\n   ✅ Celebrates your wins with you"
        ]
    },
    {
        "title": "👨‍👩‍👧‍👦 FAMILY PERSONALIZATION",
        "points": [
            "\n   ✅ Learns your family's names",
            "\n   ✅ Understands parent/child dynamics",
            "\n   ✅ Cultural context for 19 countries"
        ]
    },
    {
        "title": "💰 TRY FREE, STAY CHEAP",
        "points": [
            "\n   ✅ 7-DAY FREE TRIAL - full access!",
            "\n   ✅ Only $7.77/month after",
            "\n   ✅ +1 BONUS week when you subscribe!"
        ]
    }
]

cta_options = [
    "👉 Start your FREE 7-day trial → https://wa.me/50766623757",
    "🚀 Try FREE for 7 days → https://wa.me/50766623757",
    "💬 Message EspaLuz now (FREE trial!) → https://wa.me/50766623757",
    "✨ Get your FREE trial today → https://wa.me/50766623757",
    "🆓 7 days FREE, then just $7.77/mo → https://wa.me/50766623757"
]

social_proof = [
    "💬 \"The conversation mode is AMAZING. It's like having a patient tutor 24/7!\" — Sarah, Panama City",
    "🌟 \"I just snap photos of menus and EspaLuz translates instantly!\" — Mike, Medellín",
    "🚀 \"Voice messages back and forth - it's like texting a bilingual friend.\" — Jennifer, Mexico City",
    "💼 \"My whole family uses it. It learns our names and everything!\" — David, Digital Nomad",
    "❤️ \"The emotional AI actually gets when I'm frustrated and helps me calm down.\" — Amanda, Costa Rica",
    "🆓 \"Started with the free trial, been subscribed for 6 months now. Worth every penny!\" — Carlos, Miami"
]

hashtag_sets = [
    ["#EspaLuz", "#LearnSpanish", "#BilingualFamily", "#ExpatsInPanama", "#LanguageLearning", "#SpanishTutor", "#AITutor"],
    ["#EspaLuz", "#DigitalNomadLife", "#RemoteWork", "#BusinessSpanish", "#LocationIndependent", "#ProfessionalGrowth"],
    ["#EspaLuz", "#EmotionalAI", "#LanguageBreakthrough", "#BilingualJourney", "#LearnEnglish", "#CulturalConnection"]
]


def generate_promo_content():
    """Generate promo content - NOW WITH AI! (preserves Make.com interface)"""
    print("🎬 Generating AI-powered daily promo...")
    
    # Try AI generation first
    story = generate_ai_story()
    
    # Fallback to templates if AI fails
    if story is None:
        print("⚠️ AI unavailable, using fallback template")
        story = random.choice(FALLBACK_STORIES)
    
    benefits = random.sample(benefit_sections, 2)
    cta = random.choice(cta_options)
    proof = random.choice(social_proof)
    hashtags = " ".join(random.choice(hashtag_sets))
    video_url = random.choice(video_links)
    image_url = random.choice(image_urls)
    
    print(f"🎬 Selected video: {video_url}")
    print(f"🖼️ Selected image: {image_url}")
    print(f"🎯 Audience: {story.get('audience', 'general')}")
    print(f"💭 Emotion: {story.get('emotional_state', 'general')}")

    # Build rich promo content (same format as before)
    promo = f"""{story['hook']} 🚨

{story['story']}

{story['transformation']}

{story['emotion']} — That's the EspaLuz difference! ✨

━━━━━━━━━━━━━━━━━━━━━━━

🔥 WHY 2,000+ PEOPLE CHOOSE ESPALUZ:

{benefits[0]['title']}
{''.join([f"   {point}" for point in benefits[0]['points']])}

{benefits[1]['title']}
{''.join([f"   {point}" for point in benefits[1]['points']])}

━━━━━━━━━━━━━━━━━━━━━━━

{proof}

{cta}

🎬 WATCH: See this transformation in action → {video_url}

{hashtags}

P.S. Your 7-day FREE trial is waiting. No credit card needed to start. Just message EspaLuz on WhatsApp and say "hi"—you'll be practicing conversations in minutes! 💕"""

    return promo, story, video_url, image_url


def send_automated_daily_promo():
    """Automated version that posts to Telegram and Make.com webhook (PRESERVED!)"""
    try:
        promo, story, video_url, image_url = generate_promo_content()
        
        # Send to Telegram channel
        bot.send_message(TELEGRAM_CHAT_ID, promo)
        print("✅ Automated promo sent to @EspaLuz channel.")
        
        # Send to Make.com webhook with emotional intelligence data (SAME STRUCTURE!)
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
            "cta": random.choice(cta_options),
            "hashtags": " ".join(random.choice(hashtag_sets)),
            "socialProof": random.choice(social_proof),
            
            # Audience & Emotional State
            "audience": story.get('audience', 'general_learner'),
            "emotional_state": story.get('emotional_state', 'general'),
            "target_market": story.get('audience', 'expat_parent'),
            
            # Content Metadata
            "content_type": "ai_generated_story",
            "ai_powered": True,
            "emotional_intensity": "high" if any(word in story['story'].lower() for word in ['disaster', 'crisis', 'breakthrough', 'miracle', 'lost', 'failed', 'couldn\'t']) else "medium",
            "viral_potential": "high" if story.get('emotional_state') in ['breakthrough_euphoria', 'empowering_confidence', 'business_growth', 'career_breakthrough'] else "medium",
            
            # Platform Optimization Hints
            "instagram_focus": "community_engagement" if story.get('audience') in ['expat_parent', 'cultural_explorer'] else "professional_growth",
            "linkedin_focus": "professional_growth" if story.get('audience') in ['digital_nomad', 'business_traveler', 'entrepreneur'] else "personal_development",
            "tiktok_focus": "viral_relatability" if story.get('emotional_state') in ['crushing_embarrassment', 'local_acceptance'] else "educational_content",
            "youtube_focus": "educational_inspiration" if story.get('audience') in ['service_provider', 'native_english_learner'] else "transformation_story"
        }
        response = requests.post(MAKE_WEBHOOK_URL, json=payload)
        print(f"📤 Automated promo sent to Make.com webhook. Response: {response.status_code}")
        
    except Exception as e:
        print(f"❌ Error in automated promo: {e}")


# ============================================
# TELEGRAM BOT COMMANDS (PRESERVED!)
# ============================================

@bot.message_handler(commands=["daily_promo"])
def send_daily_promo(message):
    """Manual trigger for daily promo"""
    print("📣 /daily_promo triggered manually...")
    
    promo, story, video_url, image_url = generate_promo_content()

    bot.reply_to(message, promo)
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
            "hook": story['hook'],
            "story": story['story'],
            "emotion": story['emotion'],
            "transformation": story['transformation'],
            "cta": random.choice(cta_options),
            "hashtags": " ".join(random.choice(hashtag_sets)),
            "socialProof": random.choice(social_proof),
            "audience": story.get('audience', 'general_learner'),
            "emotional_state": story.get('emotional_state', 'general'),
            "target_market": story.get('audience', 'expat_parent'),
            "content_type": "ai_generated_story",
            "ai_powered": True
        }
        response = requests.post(MAKE_WEBHOOK_URL, json=payload)
        print("📤 Sent promo to Make.com webhook. Response:", response.status_code)
    except Exception as e:
        print("❌ Failed to send to Make.com webhook:", e)


@bot.message_handler(commands=['start', 'hello'])
def welcome(message):
    bot.reply_to(message, "👋 ¡Hola! I'm the EspaLuz AI Influencer Co-Founder v2.0!\n\n🤖 Now powered by real AI for fresh, unique content every day.\n\nCommands:\n/daily_promo - Generate & post AI-powered promo\n/test_ai - Test AI story generation\n/test_time - Check current times")


@bot.message_handler(commands=['test_time'])
def test_time(message):
    panama_tz = pytz.timezone('America/Panama')
    utc_tz = pytz.timezone('UTC')
    
    now_utc = datetime.now(utc_tz)
    now_panama = datetime.now(panama_tz)
    server_time = datetime.now()
    
    response = f"""⏰ Time Check:

🖥️ Server (Railway): {server_time.strftime('%Y-%m-%d %H:%M:%S')}
🌍 UTC: {now_utc.strftime('%Y-%m-%d %H:%M:%S %Z')}
🇵🇦 Panama: {now_panama.strftime('%Y-%m-%d %H:%M:%S %Z')}

📅 Next scheduled promo: {schedule.next_run()}
⏰ Scheduled for: 4:55 PM Panama (21:55 UTC)"""
    
    bot.reply_to(message, response)


@bot.message_handler(commands=['test_ai'])
def test_ai(message):
    """Test AI story generation"""
    bot.reply_to(message, "🧠 Testing AI story generation...")
    
    story = generate_ai_story()
    
    if story:
        response = f"""✅ AI Generation Successful!

**Hook:** {story['hook']}

**Story:** {story['story'][:300]}...

**Audience:** {story.get('audience', 'N/A')}
**Emotion:** {story.get('emotional_state', 'N/A')}"""
    else:
        response = "❌ AI generation failed. Check GROQ_API_KEY."
    
    bot.reply_to(message, response)


@bot.message_handler(commands=['test_emotional_ai'])
def test_emotional_ai(message):
    """Test full emotional AI pipeline"""
    bot.reply_to(message, "🧠 Testing full AI Influencer pipeline...")
    
    try:
        promo, story, video_url, image_url = generate_promo_content()
        
        # Send to webhook for testing
        payload = {
            "text": promo,
            "videoURL": video_url,
            "imageURL": image_url,
            "hook": story['hook'],
            "story": story['story'],
            "emotion": story['emotion'],
            "transformation": story['transformation'],
            "audience": story.get('audience', 'general'),
            "emotional_state": story.get('emotional_state', 'general'),
            "test_mode": True
        }
        
        response = requests.post(EMOTIONAL_AI_WEBHOOK_URL, json=payload)
        print(f"🧠 Sent to Emotional AI webhook. Response: {response.status_code}")
        
        bot.reply_to(message, f"✅ Test complete!\n\n🎯 Audience: {story.get('audience')}\n💭 Emotion: {story.get('emotional_state')}\n📤 Webhook: {response.status_code}")
        
    except Exception as e:
        bot.reply_to(message, f"❌ Test failed: {e}")


# ============================================
# SCHEDULING & LIFECYCLE (PRESERVED!)
# ============================================

def schedule_checker():
    """Run scheduled tasks in a separate thread"""
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)
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
        bot.remove_webhook()
        time.sleep(2)
        
        for i in range(3):
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/deleteWebhook"
            requests.get(url)
            time.sleep(1)
            
        print("🧹 Cleared all webhook connections")
        
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
                time.sleep(30)
                force_single_instance()
            else:
                print(f"❌ Bot polling error: {e}")
            print("🔄 Restarting bot in 15 seconds...")
            time.sleep(15)


# ============================================
# STARTUP
# ============================================

if __name__ == "__main__":
    print("=" * 50)
    print("🤖 ESPALUZ AI INFLUENCER CO-FOUNDER v2.0")
    print("=" * 50)
    print("✨ Now powered by Groq AI (Llama 3.3 70B)")
    print("📤 Make.com webhook: PRESERVED")
    print("⏰ Daily scheduling: PRESERVED")
    print("=" * 50)
    
    # Force cleanup at startup
    force_single_instance()
    
    # Schedule daily promo for 4:55 PM Panama time (21:55 UTC)
    schedule.every().day.at("21:55").do(send_automated_daily_promo)
    
    print("⏰ Scheduled daily promo for 4:55 PM Panama time (21:55 UTC)")
    
    # Display timezone information
    panama_tz = pytz.timezone('America/Panama')
    current_panama_time = datetime.now(panama_tz)
    server_time = datetime.now()
    
    print(f"🌍 Server time: {server_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🇵🇦 Panama time: {current_panama_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    
    # Check AI availability
    if GROQ_API_KEY:
        print("✅ GROQ_API_KEY configured - AI generation enabled")
    else:
        print("⚠️ GROQ_API_KEY not set - will use fallback templates")
    
    # Start background threads
    threading.Thread(target=schedule_checker, daemon=True).start()
    
    print("🤖 EspaLuz AI Influencer Co-Founder v2.0 is running!")
    print(f"📅 Next scheduled promo: {schedule.next_run()}")
    
    # Run the bot
    keep_alive()
