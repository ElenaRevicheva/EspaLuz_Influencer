"""
🤖 ESPALUZ AI MARKETING CO-FOUNDER v3.1
========================================
A TRUE AI Co-Founder with:
- Memory System (tracks all posts, avoids repetition)
- Strategic Calendar (day themes, holidays, seasons)
- Intelligent Rotation (systematic audience cycling)
- Self-Review (AI quality checks before posting)
- Performance Insights (weekly summaries)

PRESERVED:
- Make.com webhook trigger mechanism
- Daily scheduling via schedule library
- Telegram bot commands

Author: Elena Revicheva & CTO AIPA
Version: 3.1.0 - Dual campaign (EspaLuz + AI Marketing Engine)
"""

import telebot
import os
import random
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
import time
import threading
import requests
import schedule
import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import pytz

# ============================================
# CONFIGURATION
# ============================================

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = "@EspaLuz"
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

MAKE_WEBHOOK_URL = "https://hook.us2.make.com/ecv7x7innu2g1r3olsqi12ca4uadkmi9"
EMOTIONAL_AI_WEBHOOK_URL = MAKE_WEBHOOK_URL

# AI Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Memory file
MEMORY_FILE = "content_memory.json"
PANAMA_TZ = pytz.timezone('America/Panama')

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

marketing_engine_image_urls = [
    "https://raw.githubusercontent.com/ElenaRevicheva/EspaLuz_Influencer/main/marketing_engine_architecture.png",
    "https://raw.githubusercontent.com/ElenaRevicheva/EspaLuz_Influencer/main/marketing_engine_workflow.png",
]

# ============================================
# MEMORY SYSTEM - Tracks All Content
# ============================================

class ContentMemory:
    """Persistent memory for tracking all generated content"""
    
    def __init__(self, filepath: str = MEMORY_FILE):
        self.filepath = filepath
        self.memory = self._load()
    
    def _load(self) -> Dict:
        """Load memory from file"""
        try:
            if os.path.exists(self.filepath):
                with open(self.filepath, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️ Memory load error: {e}")
        
        return {
            "posts": [],
            "audiences_used": [],
            "emotions_used": [],
            "themes_used": [],
            "locations_used": [],
            "weekly_stats": {},
            "total_posts": 0,
            "created_at": datetime.now(PANAMA_TZ).isoformat()
        }
    
    def _save(self):
        """Save memory to file"""
        try:
            with open(self.filepath, 'w') as f:
                json.dump(self.memory, f, indent=2, default=str)
        except Exception as e:
            print(f"❌ Memory save error: {e}")
    
    def add_post(self, post_data: Dict):
        """Record a new post"""
        post_record = {
            "id": len(self.memory["posts"]) + 1,
            "date": datetime.now(PANAMA_TZ).isoformat(),
            "day_of_week": datetime.now(PANAMA_TZ).strftime("%A"),
            "audience": post_data.get("audience", "unknown"),
            "emotion": post_data.get("emotional_state", "unknown"),
            "theme": post_data.get("theme", "general"),
            "location": post_data.get("location", "unknown"),
            "hook": post_data.get("hook", "")[:100],
            "story_hash": hashlib.md5(post_data.get("story", "").encode()).hexdigest()[:8],
            "story_preview": post_data.get("story", "")[:200]
        }
        
        self.memory["posts"].append(post_record)
        self.memory["total_posts"] += 1
        
        # Track recent usage (last 14 days)
        self._update_recent_usage(post_record)
        self._save()
        
        print(f"🧠 Memory: Recorded post #{post_record['id']} ({post_record['audience']}/{post_record['emotion']})")
    
    def _update_recent_usage(self, post_record: Dict):
        """Update recent usage tracking"""
        # Keep only last 14 entries for rotation tracking
        self.memory["audiences_used"].append(post_record["audience"])
        self.memory["audiences_used"] = self.memory["audiences_used"][-14:]
        
        self.memory["emotions_used"].append(post_record["emotion"])
        self.memory["emotions_used"] = self.memory["emotions_used"][-14:]
        
        self.memory["locations_used"].append(post_record["location"])
        self.memory["locations_used"] = self.memory["locations_used"][-14:]
    
    def get_recent_audiences(self, days: int = 7) -> List[str]:
        """Get audiences used in recent days"""
        return self.memory["audiences_used"][-days:]
    
    def get_recent_emotions(self, days: int = 7) -> List[str]:
        """Get emotions used in recent days"""
        return self.memory["emotions_used"][-days:]
    
    def get_recent_locations(self, days: int = 7) -> List[str]:
        """Get locations used in recent days"""
        return self.memory["locations_used"][-days:]
    
    def get_weekly_summary(self) -> str:
        """Generate a weekly summary"""
        recent_posts = self.memory["posts"][-7:]
        if not recent_posts:
            return "No posts this week yet."
        
        audiences = [p["audience"] for p in recent_posts]
        emotions = [p["emotion"] for p in recent_posts]
        
        summary = f"""📊 WEEKLY CONTENT SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━
📝 Posts this week: {len(recent_posts)}
👥 Audiences covered: {', '.join(set(audiences))}
💭 Emotional arcs: {', '.join(set(emotions))}
📈 Total all-time posts: {self.memory['total_posts']}
━━━━━━━━━━━━━━━━━━━━━━━"""
        return summary
    
    def check_similarity(self, new_story: str) -> bool:
        """Check if new story is too similar to recent posts"""
        new_hash = hashlib.md5(new_story.encode()).hexdigest()[:8]
        recent_hashes = [p["story_hash"] for p in self.memory["posts"][-30:]]
        return new_hash in recent_hashes


# Initialize global memory
memory = ContentMemory()

# ============================================
# STRATEGIC CALENDAR - Day Themes & Holidays
# ============================================

class StrategicCalendar:
    """Calendar-aware content strategy"""
    
    # Day of week themes
    DAY_THEMES = {
        "Monday": {
            "theme": "motivation",
            "focus": "Fresh start energy, new week new goals",
            "emotions": ["breakthrough", "empowerment"],
            "hashtag_boost": "#MondayMotivation #NewWeekNewGoals"
        },
        "Tuesday": {
            "theme": "transformation",
            "focus": "Success stories, before/after journeys",
            "emotions": ["breakthrough", "connection"],
            "hashtag_boost": "#TransformationTuesday #SuccessStory"
        },
        "Wednesday": {
            "theme": "wisdom",
            "focus": "Tips, insights, educational content",
            "emotions": ["empowerment", "general"],
            "hashtag_boost": "#WisdomWednesday #LanguageTips"
        },
        "Thursday": {
            "theme": "throwback",
            "focus": "Journey stories, progress reflection",
            "emotions": ["connection", "breakthrough"],
            "hashtag_boost": "#ThrowbackThursday #JourneyStory"
        },
        "Friday": {
            "theme": "celebration",
            "focus": "Wins, achievements, feel-good stories",
            "emotions": ["joy", "breakthrough"],
            "hashtag_boost": "#FridayFeeling #WeekendVibes"
        },
        "Saturday": {
            "theme": "family",
            "focus": "Family moments, weekend activities",
            "emotions": ["connection", "joy"],
            "hashtag_boost": "#FamilyTime #WeekendFun"
        },
        "Sunday": {
            "theme": "reflection",
            "focus": "Thoughtful content, preparation for week",
            "emotions": ["connection", "empowerment"],
            "hashtag_boost": "#SundayThoughts #WeekAhead"
        }
    }
    
    # Holiday/Event awareness
    SPECIAL_DAYS = {
        # Format: (month, day): {"name": "", "theme": "", "focus": ""}
        (1, 1): {"name": "New Year", "theme": "fresh_start", "focus": "New year, new language goals!"},
        (2, 14): {"name": "Valentine's Day", "theme": "connection", "focus": "Language of love, connecting with loved ones"},
        (3, 8): {"name": "International Women's Day", "theme": "empowerment", "focus": "Empowering women through language"},
        (5, 5): {"name": "Cinco de Mayo", "theme": "cultural", "focus": "Celebrating Mexican culture and Spanish language"},
        (5, 10): {"name": "Mother's Day (MX)", "theme": "family", "focus": "Connecting with mamá in her language"},
        (6, 16): {"name": "Father's Day", "theme": "family", "focus": "Bonding with papá through language"},
        (9, 15): {"name": "Hispanic Heritage Month Start", "theme": "cultural", "focus": "Celebrating Hispanic heritage"},
        (10, 12): {"name": "Día de la Hispanidad", "theme": "cultural", "focus": "Spanish language worldwide"},
        (11, 2): {"name": "Día de los Muertos", "theme": "cultural", "focus": "Honoring traditions through language"},
        (12, 25): {"name": "Christmas", "theme": "family", "focus": "Holiday family connections"},
        (12, 31): {"name": "New Year's Eve", "theme": "reflection", "focus": "Reflecting on language journey"}
    }
    
    @classmethod
    def get_today_strategy(cls) -> Dict:
        """Get content strategy for today"""
        now = datetime.now(PANAMA_TZ)
        day_name = now.strftime("%A")
        month_day = (now.month, now.day)
        
        strategy = {
            "date": now.strftime("%Y-%m-%d"),
            "day_of_week": day_name,
            "day_theme": cls.DAY_THEMES.get(day_name, cls.DAY_THEMES["Monday"]),
            "special_day": cls.SPECIAL_DAYS.get(month_day),
            "is_weekend": day_name in ["Saturday", "Sunday"],
            "week_number": now.isocalendar()[1]
        }
        
        # Check for upcoming special days (within 3 days)
        for i in range(1, 4):
            future_date = now + timedelta(days=i)
            future_key = (future_date.month, future_date.day)
            if future_key in cls.SPECIAL_DAYS:
                strategy["upcoming_special"] = {
                    "days_away": i,
                    **cls.SPECIAL_DAYS[future_key]
                }
                break
        
        return strategy


# ============================================
# INTELLIGENT ROTATION - Systematic Cycling
# ============================================

class IntelligentRotation:
    """Ensures variety in content by systematic rotation"""
    
    ALL_AUDIENCES = [
        "expat_parent", "digital_nomad", "service_provider", "business_traveler",
        "cultural_explorer", "healthcare_worker", "entrepreneur", "retiree", 
        "teacher", "immigrant", "russian_speaker"
    ]
    
    ALL_EMOTIONS = [
        "frustration", "embarrassment", "breakthrough", "connection",
        "empowerment", "isolation", "anxiety", "joy"
    ]
    
    ALL_LOCATIONS = [
        "Panama City", "Medellín", "Mexico City", "Madrid", "Barcelona",
        "Buenos Aires", "Lima", "San José", "Bogotá", "Cartagena",
        "Cancún", "Playa del Carmen", "Quito", "Santiago"
    ]
    
    @classmethod
    def select_audience(cls, recent_used: List[str], day_theme: Dict) -> str:
        """Select audience ensuring variety"""
        # Filter out recently used (last 5)
        available = [a for a in cls.ALL_AUDIENCES if a not in recent_used[-5:]]
        
        if not available:
            available = cls.ALL_AUDIENCES
        
        # Weight by day theme
        theme = day_theme.get("theme", "general")
        weighted = available.copy()
        
        if theme == "family":
            weighted.extend(["expat_parent", "retiree"] * 2)
        elif theme == "transformation":
            weighted.extend(["digital_nomad", "entrepreneur", "service_provider"] * 2)
        elif theme == "motivation":
            weighted.extend(["entrepreneur", "business_traveler", "immigrant"] * 2)
        
        return random.choice(weighted)
    
    @classmethod
    def select_emotion(cls, recent_used: List[str], day_theme: Dict) -> str:
        """Select emotion ensuring variety and day alignment"""
        preferred_emotions = day_theme.get("emotions", ["breakthrough", "empowerment"])
        
        # 70% chance to use day-themed emotion, 30% other
        if random.random() < 0.7 and preferred_emotions:
            return random.choice(preferred_emotions)
        
        # Filter out recently overused emotions
        emotion_counts = {e: recent_used.count(e) for e in cls.ALL_EMOTIONS}
        least_used = sorted(emotion_counts.items(), key=lambda x: x[1])[:4]
        
        return random.choice([e[0] for e in least_used])
    
    @classmethod
    def select_location(cls, recent_used: List[str]) -> str:
        """Select location ensuring variety"""
        available = [loc for loc in cls.ALL_LOCATIONS if loc not in recent_used[-7:]]
        
        if not available:
            available = cls.ALL_LOCATIONS
        
        return random.choice(available)


# ============================================
# ESPALUZ BRAND KNOWLEDGE
# ============================================

ESPALUZ_BRAND_KNOWLEDGE = """
# ESPALUZ - AI Spanish/English Tutor
## Brand Identity
EspaLuz is an AI-powered bilingual tutor on WhatsApp that uses emotional intelligence to help people learn Spanish and English.

## ACTUAL PRODUCT FEATURES:
🗣️ **CONVERSATION MODE** - Type "conversation" for intelligent family conversation practice
🧠 **Emotional AI** - Analyzes emotions (frustrated, excited, homesick) and adapts
🎤 **Voice Messages** - Send voice in any language, get audio responses back
📸 **Photo Translation** - Send photos of menus, signs, documents for instant translation
🎥 **Personalized Video Responses** - Custom video explanations
👨‍👩‍👧‍👦 **Family Personalization** - Learns family names, preferences, dynamics
🌍 **19 Countries** - Cultural context for all Spanish-speaking countries
🌐 **Trilingual** - Russian, Spanish, AND English support

## PRICING:
- 🆓 **7-DAY FREE TRIAL** - Full access to all features
- 💰 **$7.77/month via PayPal** - BONUS: 1 extra week FREE after subscription!

## Contact:
WhatsApp: +507 6662 3757
Website: https://espaluz-ai-language-tutor.lovable.app
"""

# ============================================
# AI STORY GENERATION WITH CONTEXT
# ============================================

def generate_ai_story(strategy: Dict, audience: str, emotion: str, location: str, memory: ContentMemory) -> Optional[Dict]:
    """Generate story with full context awareness"""
    
    current_date = datetime.now(PANAMA_TZ).strftime("%B %d, %Y")
    day_theme = strategy["day_theme"]
    special_day = strategy.get("special_day")
    
    # Build context about what to avoid
    recent_themes = memory.get_recent_audiences(5)
    avoid_context = ""
    if recent_themes:
        avoid_context = f"\n\nAVOID these recently used themes: {', '.join(recent_themes)}"
    
    # Special day context
    special_context = ""
    if special_day:
        special_context = f"\n\nSPECIAL DAY: Today is {special_day['name']}! Theme: {special_day['focus']}"
    
    prompt = f"""You are the AI Marketing Co-Founder for EspaLuz, an AI Spanish/English tutor.

BRAND KNOWLEDGE:
{ESPALUZ_BRAND_KNOWLEDGE}

TODAY'S STRATEGIC CONTEXT:
- Date: {current_date} ({strategy['day_of_week']})
- Day Theme: {day_theme['theme'].upper()} - {day_theme['focus']}
- Hashtag Boost: {day_theme['hashtag_boost']}
{special_context}

CONTENT ASSIGNMENT:
- Target Audience: {audience.replace('_', ' ').title()}
- Emotional Arc: {emotion.replace('_', ' ').title()} → Confidence/Breakthrough
- Location Setting: {location}
{avoid_context}

GENERATE A SOCIAL MEDIA STORY with these components:

1. **HOOK** (1 line with emoji): Attention-grabbing opening aligned with {day_theme['theme']} theme
2. **STORY** (3-5 sentences): Specific, relatable scenario in {location}. First-person. Sensory details.
3. **TRANSFORMATION** (2-3 sentences): How EspaLuz helped. Be specific about features used.
4. **EMOTION** (1 line with emoji): The {emotion} → breakthrough emotional shift
5. **THEME** (1 word): Main theme of the story (e.g., "parenting", "career", "travel", "healthcare")

RULES:
- Make it feel REAL and SPECIFIC to {location}
- Include local cultural details
- Show genuine vulnerability then triumph
- Mention specific EspaLuz features (conversation mode, voice messages, photo translation)
- Keep total length under 250 words
- CTA: https://wa.me/50766623757

Output as valid JSON with keys: hook, story, transformation, emotion, theme, audience, emotional_state, location"""

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
                "max_tokens": 1200
            },
            timeout=30
        )
        
        if response.status_code == 200:
            content = response.json()['choices'][0]['message']['content']
            
            # Parse JSON
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            
            story_data = json.loads(content.strip())
            story_data['audience'] = audience
            story_data['emotional_state'] = emotion
            story_data['location'] = location
            story_data['day_theme'] = day_theme['theme']
            story_data['hashtag_boost'] = day_theme['hashtag_boost']
            
            print(f"🧠 AI generated story: {audience} in {location} ({emotion})")
            return story_data
        else:
            print(f"❌ Groq API error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ AI generation error: {e}")
        return None


def self_review_story(story_data: Dict, memory: ContentMemory) -> Dict:
    """AI reviews its own content for quality"""
    
    # Check for repetition
    if memory.check_similarity(story_data.get('story', '')):
        print("⚠️ Self-review: Story too similar to recent post, regenerating...")
        return {"approved": False, "reason": "similarity"}
    
    # Check story length
    story_length = len(story_data.get('story', ''))
    if story_length < 100:
        print("⚠️ Self-review: Story too short")
        return {"approved": False, "reason": "too_short"}
    
    # Check for required elements
    required_keywords = ['espaluz', 'spanish', 'english', 'language']
    story_lower = story_data.get('story', '').lower() + story_data.get('transformation', '').lower()
    
    if not any(kw in story_lower for kw in required_keywords):
        print("⚠️ Self-review: Missing brand keywords")
        return {"approved": False, "reason": "missing_brand"}
    
    print("✅ Self-review: Content approved!")
    return {"approved": True, "reason": "passed_all_checks"}


# ============================================
# FALLBACK TEMPLATES
# ============================================

FALLBACK_STORIES = [
    {
        "hook": "🧠 AI THAT ACTUALLY GETS IT",
        "story": "I was having a meltdown trying to discipline my toddler in Spanish. I sent a frustrated voice message to EspaLuz: 'I don't know how to be firm but loving in Spanish!' The AI didn't just translate—it UNDERSTOOD I was a stressed parent and coached me through it.",
        "transformation": "EspaLuz analyzed my emotional state, gave me gentle parenting phrases in Spanish, and helped me through conversation mode. Now my daughter responds better, and I feel confident as a bilingual parent!",
        "emotion": "🤖 From robotic apps to EMOTIONAL AI",
        "theme": "parenting",
        "audience": "expat_parent",
        "emotional_state": "frustration",
        "location": "Panama City"
    }
]

# ============================================
# CONTENT ASSEMBLY
# ============================================

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
    ["#EspaLuz", "#LearnSpanish", "#BilingualFamily", "#ExpatsInPanama", "#LanguageLearning"],
    ["#EspaLuz", "#DigitalNomadLife", "#RemoteWork", "#BusinessSpanish", "#LocationIndependent"],
    ["#EspaLuz", "#EmotionalAI", "#LanguageBreakthrough", "#BilingualJourney", "#LearnEnglish"]
]


def generate_promo_content():
    """Generate promo content with full AI Co-Founder intelligence"""
    print("=" * 50)
    print("🤖 AI MARKETING CO-FOUNDER v3.1 - Generating Content")
    print("=" * 50)
    
    # Get strategic context
    strategy = StrategicCalendar.get_today_strategy()
    print(f"📅 Date: {strategy['date']} ({strategy['day_of_week']})")
    print(f"🎯 Theme: {strategy['day_theme']['theme'].upper()}")
    
    if strategy.get("special_day"):
        print(f"🎉 Special Day: {strategy['special_day']['name']}")
    
    # Intelligent rotation
    audience = IntelligentRotation.select_audience(
        memory.get_recent_audiences(),
        strategy["day_theme"]
    )
    emotion = IntelligentRotation.select_emotion(
        memory.get_recent_emotions(),
        strategy["day_theme"]
    )
    location = IntelligentRotation.select_location(
        memory.get_recent_locations()
    )
    
    print(f"👥 Selected: {audience} | 💭 {emotion} | 📍 {location}")
    
    # Generate with AI (with retry)
    story = None
    for attempt in range(3):
        story = generate_ai_story(strategy, audience, emotion, location, memory)
        
        if story:
            # Self-review
            review = self_review_story(story, memory)
            if review["approved"]:
                break
            else:
                print(f"🔄 Retry {attempt + 1}/3: {review['reason']}")
                story = None
    
    # Fallback if AI fails
    if story is None:
        print("⚠️ AI unavailable, using fallback template")
        story = random.choice(FALLBACK_STORIES)
    
    # Record in memory
    memory.add_post(story)
    
    # Assemble final content
    benefits = random.sample(benefit_sections, 2)
    cta = random.choice(cta_options)
    proof = random.choice(social_proof)
    base_hashtags = random.choice(hashtag_sets)
    
    # Add day-themed hashtags
    day_hashtags = strategy["day_theme"].get("hashtag_boost", "")
    hashtags = " ".join(base_hashtags) + " " + day_hashtags
    
    video_url = random.choice(video_links)
    image_url = random.choice(image_urls)
    
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

    print("✅ Content generated successfully!")
    print("=" * 50)

    return promo, story, video_url, image_url


def get_campaign_type_for_date(dt: datetime) -> str:
    """
    Odd calendar day (1,3,5,...) → classic EspaLuz tutoring content.
    Even calendar day (2,4,6,...) → AI Marketing Engine / AIdeazz positioning content.
    Uses the calendar day in Panama time when dt is timezone-aware.
    """
    if dt.tzinfo is None:
        dt = PANAMA_TZ.localize(dt)
    else:
        dt = dt.astimezone(PANAMA_TZ)
    return "espaluz" if dt.day % 2 == 1 else "marketing_engine"


MARKETING_ENGINE_FALLBACK = [
    {
        "hook": "🚀 ONE ENGINE, EVERY CHANNEL — BUILT FOR FOUNDERS",
        "story": "We kept shipping content across Telegram, WhatsApp, and the web—but nothing measured outcomes. The AI Marketing Engine ties agents, scheduling, and proof together so growth work compounds instead of evaporating.",
        "transformation": "From scattered promos to a single orchestrated pipeline: brand voice, calendars, resilience on Oracle, and client-ready demos—without replacing your Make.com social flow.",
        "emotion": "⚡ From busywork to **leverage**",
        "theme": "marketing_engine",
        "audience": "founder",
        "emotional_state": "ambition",
        "location": "Panama City",
    }
]


def generate_ai_marketing_engine_story(strategy: Dict, audience: str, emotion: str, location: str, memory: ContentMemory) -> Optional[Dict]:
    """Groq-generated story for the AI Marketing Engine / AIdeazz narrative."""
    current_date = strategy["date"]
    day_theme = strategy["day_theme"]

    prompt = f"""You are the AI Marketing Co-Founder promoting the **AI Marketing Engine** behind AIdeazz: multi-agent orchestration, SEO/content pipelines, Oracle deployment, and real client outcomes (EspaLuz is the flagship case study).

BRAND KNOWLEDGE (ENGINE):
- Full-stack marketing automation: Telegram/WhatsApp agents, CTO AIPA, roadmap-driven SEO, resilience docs.
- Differentiator: not generic "AI copy" — measured loops, deployment on Oracle, integrations (Make.com preserved for distribution).
- CTAs: https://aideazz.xyz and the public roadmap in GitHub (AIPA_AITCF).

TODAY'S CONTEXT:
- Date: {current_date} ({strategy['day_of_week']})
- Day Theme: {day_theme['theme'].upper()} — {day_theme['focus']}

CONTENT ASSIGNMENT:
- Audience lens: {audience.replace('_', ' ').title()}
- Emotional arc: {emotion.replace('_', ' ').title()}
- Setting: {location}

GENERATE A SOCIAL POST STORY with:
1. **HOOK** (1 line, emoji): bold, founder-focused
2. **STORY** (3-5 sentences): concrete problem → how the engine solves it; mention orchestration or outcomes
3. **TRANSFORMATION** (2-3 sentences): what changes when marketing is engine-driven (measurement, deploy, compounding)
4. **EMOTION** (1 line, emoji): shift from chaos to clarity
5. **THEME** (1 word): e.g. "orchestration", "leverage", "pipeline"

RULES:
- Do NOT pretend to be the Spanish tutor product; this post sells the **marketing engine** and AIdeazz capabilities.
- You may reference EspaLuz briefly as proof.
- Under 220 words for story+transformation combined.
- Output valid JSON: hook, story, transformation, emotion, theme, audience, emotional_state, location"""

    try:
        response = requests.post(
            GROQ_API_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.85,
                "max_tokens": 1200,
            },
            timeout=30,
        )
        if response.status_code != 200:
            print(f"❌ Groq API error (marketing): {response.status_code}")
            return None
        content = response.json()["choices"][0]["message"]["content"]
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        story_data = json.loads(content.strip())
        story_data["audience"] = audience
        story_data["emotional_state"] = emotion
        story_data["location"] = location
        story_data["day_theme"] = day_theme["theme"]
        story_data["hashtag_boost"] = day_theme.get("hashtag_boost", "")
        print(f"🧠 AI marketing-engine story: {audience} / {location}")
        return story_data
    except Exception as e:
        print(f"❌ AI marketing generation error: {e}")
        return None


def self_review_marketing_story(story_data: Dict, memory: ContentMemory) -> Dict:
    if memory.check_similarity(story_data.get("story", "")):
        return {"approved": False, "reason": "similarity"}
    if len(story_data.get("story", "")) < 80:
        return {"approved": False, "reason": "too_short"}
    blob = (story_data.get("story", "") + story_data.get("transformation", "")).lower()
    keywords = ("market", "engine", "ai", "brand", "content", "oracle", "autom", "client", "founder", "pipeline", "agent")
    if sum(1 for k in keywords if k in blob) < 2:
        return {"approved": False, "reason": "missing_engine_keywords"}
    return {"approved": True, "reason": "passed"}


def generate_marketing_engine_content(image_url_override: Optional[str] = None):
    """Promo bundle for even calendar days — AI Marketing Engine narrative (Make webhook shape unchanged).

    If ``image_url_override`` is set (e.g. when firing one post per asset), that URL is used instead of random.
    """
    print("=" * 50)
    print("🎯 AI MARKETING ENGINE CAMPAIGN — Generating Content")
    print("=" * 50)

    strategy = StrategicCalendar.get_today_strategy()
    audience = IntelligentRotation.select_audience(memory.get_recent_audiences(), strategy["day_theme"])
    emotion = IntelligentRotation.select_emotion(memory.get_recent_emotions(), strategy["day_theme"])
    location = IntelligentRotation.select_location(memory.get_recent_locations())

    story = None
    for attempt in range(3):
        story = generate_ai_marketing_engine_story(strategy, audience, emotion, location, memory)
        if story:
            review = self_review_marketing_story(story, memory)
            if review["approved"]:
                break
            print(f"🔄 Marketing retry {attempt + 1}/3: {review['reason']}")
            story = None

    if story is None:
        print("⚠️ Marketing AI unavailable or failed review — using fallback")
        story = dict(random.choice(MARKETING_ENGINE_FALLBACK))

    memory.add_post(story)

    me_benefits = [
        {
            "title": "🧩 ORCHESTRATED AGENTS",
            "points": [
                "\n   ✅ CTO AIPA + domain bots share one roadmap",
                "\n   ✅ Scheduling, outreach, and proof in one loop",
                "\n   ✅ Oracle-ready deployment patterns",
            ],
        },
        {
            "title": "📈 CONTENT THAT COMPOUNDS",
            "points": [
                "\n   ✅ SEO + sitemap pipelines (AIdeazz site)",
                "\n   ✅ Resilience docs + health checks",
                "\n   ✅ Case-study ready narrative (EspaLuz)",
            ],
        },
    ]
    benefits = random.sample(me_benefits, 2)
    cta = random.choice(
        [
            "👉 See the stack → https://aideazz.xyz",
            "📎 Roadmap & engine docs → GitHub **AIPA_AITCF** (AI Marketing Engine full roadmap)",
            "🌐 AIdeazz hub → https://aideazz.xyz",
        ]
    )
    proof = "💡 *Built by Elena Revicheva & CTO AIPA — shipping on Oracle alongside EspaLuz.*"
    hashtags = "#AIdeazz #AIMarketingEngine #BuildInPublic #MLOps #FounderTools " + strategy["day_theme"].get("hashtag_boost", "")

    video_url = random.choice(video_links)
    image_url = (
        image_url_override
        if image_url_override
        else random.choice(marketing_engine_image_urls)
    )

    promo = f"""{story['hook']} 🚨

{story['story']}

{story['transformation']}

{story['emotion']} — That's the **AI Marketing Engine** difference. ✨

━━━━━━━━━━━━━━━━━━━━━━━

🔥 WHY FOUNDERS WATCH THIS STACK:

{benefits[0]['title']}
{''.join(benefits[0]['points'])}

{benefits[1]['title']}
{''.join(benefits[1]['points'])}

━━━━━━━━━━━━━━━━━━━━━━━

{proof}

{cta}

🎬 Clip: {video_url}

{hashtags}

🔗 *EspaLuz (live product):* https://wa.me/50766623757 — try the tutor; this post is about the **engine** behind the brand."""

    print("✅ Marketing engine content generated!")
    print("=" * 50)
    return promo, story, video_url, image_url


def generate_scheduled_promo_bundle():
    """Same alternation for cron and manual /daily_promo (Panama calendar day)."""
    now = datetime.now(PANAMA_TZ)
    if get_campaign_type_for_date(now) == "espaluz":
        p, s, v, i = generate_promo_content()
        return p, s, v, i, "espaluz"
    p, s, v, i = generate_marketing_engine_content()
    return p, s, v, i, "marketing_engine"


def _local_repo_image_path(image_url: str) -> Optional[str]:
    """If the file named in the URL exists in cwd (repo root), upload that bytes to Telegram."""
    base = image_url.rsplit("/", 1)[-1]
    if os.path.isfile(base):
        return base
    return None


def send_channel_promo_with_image(promo: str, image_url: str) -> None:
    """Post to @EspaLuz with the image visible (photo + caption). Continuation message if caption exceeds 1024 chars."""
    local = _local_repo_image_path(image_url)
    cap = promo[:1024] if len(promo) > 1024 else promo
    if local:
        with open(local, "rb") as f:
            bot.send_photo(TELEGRAM_CHAT_ID, f, caption=cap)
    else:
        bot.send_photo(TELEGRAM_CHAT_ID, image_url, caption=cap)
    if len(promo) > 1024:
        bot.send_message(TELEGRAM_CHAT_ID, promo[1024:])


def test_marketing_engine_image_assets() -> None:
    """One-off: verify both marketing PNGs upload to Telegram (short caption, no AI, no memory, no webhook).

    Scheduled posting is unchanged: odd calendar days = EspaLuz, even = marketing engine (one post/day).
    """
    for url in marketing_engine_image_urls:
        name = url.rsplit("/", 1)[-1]
        cap = f"✅ Image check: {name}\n(asset test only — not the daily schedule)"
        print(f"📸 Sending test photo: {name}")
        send_channel_promo_with_image(cap, url)
        time.sleep(2)
    print("✅ Both asset checks sent to channel.")


def fire_two_marketing_image_posts() -> None:
    """Two full AI marketing-engine posts: one per ``marketing_engine_image_urls`` (order preserved).

    Each run: generate copy with Groq (or fallback), ``memory`` update, Telegram **photo + caption**,
    then **Make.com** webhook with the same rich payload shape as scheduled marketing days so your
    scenario can post to Instagram, LinkedIn, etc.

    This is a **manual one-off**. It does **not** replace or disable the daily cron: odd calendar day =
    EspaLuz, even day = marketing engine (one post/day) — that keeps running on schedule.
    """
    for idx, url in enumerate(marketing_engine_image_urls):
        print(f"📸 Full AI post {idx + 1}/2 — image: {url}")
        promo, story, video_url, image_url = generate_marketing_engine_content(image_url_override=url)
        send_channel_promo_with_image(promo, image_url)
        print(f"✅ Telegram photo+caption sent ({image_url.rsplit('/', 1)[-1]}).")

        payload: Dict[str, Any] = {
            "text": promo,
            "videoURL": video_url,
            "imageURL": image_url,
            "videoTitle": f"AI Marketing Engine: {story['emotion']}",
            "videoDescription": story["story"][:200] + "...",
            "automated": False,
            "manual_two_marketing_post_batch": True,
            "batch_index": idx + 1,
            "batch_total": len(marketing_engine_image_urls),
            "timestamp": datetime.now(PANAMA_TZ).isoformat(),
            "hook": story["hook"],
            "story": story["story"],
            "emotion": story["emotion"],
            "transformation": story["transformation"],
            "cta": random.choice(cta_options),
            "hashtags": " ".join(random.choice(hashtag_sets)),
            "socialProof": random.choice(social_proof),
            "audience": story.get("audience", "general_learner"),
            "emotional_state": story.get("emotional_state", "general"),
            "location": story.get("location", "unknown"),
            "day_theme": story.get("day_theme", "general"),
            "content_type": "marketing_engine_v3",
            "campaign_type": "marketing_engine",
            "ai_powered": True,
            "has_memory": True,
            "strategic_calendar": True,
        }
        response = requests.post(MAKE_WEBHOOK_URL, json=payload)
        print(f"📤 Make.com webhook {idx + 1}/2. Response: {response.status_code}")
        time.sleep(3)

    print("✅ Done: two full marketing posts → Telegram + Make. Daily auto schedule unchanged.")


# ============================================
# AUTOMATED POSTING (PRESERVED!)
# ============================================

def send_automated_daily_promo():
    """Automated daily promo with full intelligence"""
    try:
        promo, story, video_url, image_url, campaign_type = generate_scheduled_promo_bundle()
        
        # Channel: photo + caption so image appears (EspaLuz + marketing engine days)
        send_channel_promo_with_image(promo, image_url)
        print(f"✅ Automated promo sent to @EspaLuz channel ({campaign_type}, photo+caption).")
        
        # Send to Make.com webhook
        content_type = "ai_cofounder_v3" if campaign_type == "espaluz" else "marketing_engine_v3"
        payload = {
            "text": promo,
            "videoURL": video_url,
            "imageURL": image_url,
            "videoTitle": (
                f"EspaLuz Success Story: {story['emotion']}"
                if campaign_type == "espaluz"
                else f"AI Marketing Engine: {story['emotion']}"
            ),
            "videoDescription": story['story'][:200] + "...",
            "automated": True,
            "timestamp": datetime.now(PANAMA_TZ).isoformat(),
            "hook": story['hook'],
            "story": story['story'],
            "emotion": story['emotion'],
            "transformation": story['transformation'],
            "cta": random.choice(cta_options),
            "hashtags": " ".join(random.choice(hashtag_sets)),
            "socialProof": random.choice(social_proof),
            "audience": story.get('audience', 'general_learner'),
            "emotional_state": story.get('emotional_state', 'general'),
            "location": story.get('location', 'unknown'),
            "day_theme": story.get('day_theme', 'general'),
            "content_type": content_type,
            "campaign_type": campaign_type,
            "ai_powered": True,
            "has_memory": True,
            "strategic_calendar": True
        }
        response = requests.post(MAKE_WEBHOOK_URL, json=payload)
        print(f"📤 Sent to Make.com webhook ({campaign_type}). Response: {response.status_code}")
        
    except Exception as e:
        print(f"❌ Error in automated promo: {e}")


# ============================================
# TELEGRAM BOT COMMANDS
# ============================================

@bot.message_handler(commands=["daily_promo"])
def send_daily_promo(message):
    """Manual trigger for daily promo"""
    print("📣 /daily_promo triggered manually...")
    
    promo, story, video_url, image_url, campaign_type = generate_scheduled_promo_bundle()
    bot.reply_to(message, promo)
    send_channel_promo_with_image(promo, image_url)
    print(f"✅ Manual promo sent ({campaign_type}, photo+caption).")

    try:
        content_type = "ai_cofounder_v3" if campaign_type == "espaluz" else "marketing_engine_v3"
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
            "location": story.get('location', 'unknown'),
            "ai_powered": True,
            "has_memory": True,
            "content_type": content_type,
            "campaign_type": campaign_type,
        }
        response = requests.post(MAKE_WEBHOOK_URL, json=payload)
        print("📤 Sent to Make.com webhook. Response:", response.status_code)
    except Exception as e:
        print("❌ Failed to send to Make.com webhook:", e)


@bot.message_handler(commands=["campaign_today"])
def campaign_today(message):
    """Which campaign runs today (auto + /daily_promo use this rule)."""
    now = datetime.now(PANAMA_TZ)
    ct = get_campaign_type_for_date(now)
    label = "**EspaLuz tutoring narrative** (classic co-founder)" if ct == "espaluz" else "**AI Marketing Engine** (AIdeazz stack, roadmap, Oracle)"
    bot.reply_to(
        message,
        f"""📅 **Campaign for today** ({now.strftime('%Y-%m-%d')} Panama)

• Rule: **odd** calendar day → EspaLuz · **even** calendar day → Marketing Engine
• Today: {label}

Commands `/daily_promo` and the 6:00 PM auto post follow this schedule.""",
    )


@bot.message_handler(commands=['start', 'hello'])
def welcome(message):
    """Welcome message with full menu"""
    welcome_text = """👋 ¡Hola! I'm the EspaLuz AI Marketing Co-Founder v3.1!

🤖 **TRUE AI CO-FOUNDER CAPABILITIES:**
━━━━━━━━━━━━━━━━━━━━━━━
🧠 Memory System - No repeated content
📅 Strategic Calendar - Day themes & holidays  
🔄 Intelligent Rotation - Variety guaranteed
✅ Self-Review - Quality checks before posting
━━━━━━━━━━━━━━━━━━━━━━━

Type /help to see all commands!"""
    
    bot.reply_to(message, welcome_text)
    # Set bot commands menu
    set_bot_commands()


@bot.message_handler(commands=['help', 'menu', 'commands'])
def show_help(message):
    """Show full command menu"""
    help_text = """📋 **ESPALUZ AI CO-FOUNDER v3.1 - COMMANDS**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📣 **CONTENT GENERATION**
/daily_promo - Generate & post **today's** campaign (EspaLuz vs Marketing Engine by calendar day)
/campaign_today - Which campaign runs **today** (odd=EspaLuz, even=Engine)
/test_ai - Test AI generation (no posting)

📊 **ANALYTICS & MEMORY**
/memory - View content memory stats
/weekly - Weekly content summary
/stats - Full performance statistics

📅 **STRATEGY & PLANNING**
/strategy - Today's content strategy
/calendar - View upcoming themes & holidays
/next - Preview what's coming next

⚙️ **SYSTEM & DEBUG**
/test_time - Check server & Panama time
/status - Bot health & configuration
/version - Current version info

ℹ️ **HELP**
/start - Welcome message
/help - This command menu
/about - About AI Co-Founder v3.1

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏰ Auto-posting: Daily at 6:00 PM Panama
🔀 Campaigns: **odd** day = EspaLuz · **even** day = AI Marketing Engine
🧠 AI Model: Groq Llama 3.3 70B
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
    
    bot.reply_to(message, help_text)


@bot.message_handler(commands=['about'])
def show_about(message):
    """About the AI Co-Founder"""
    about_text = """🤖 **ESPALUZ AI MARKETING CO-FOUNDER v3.1**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Dual campaign (additive):** on **odd** calendar days we run classic EspaLuz tutoring stories; on **even** days we spotlight the **AI Marketing Engine** (AIdeazz stack, roadmap, Oracle). Same Make.com webhook; payload includes `campaign_type`.

**What makes this a TRUE AI Co-Founder:**

🧠 **Memory System**
Tracks all generated content. Never repeats stories.
Remembers audiences, emotions, locations used.

📅 **Strategic Calendar**
• Monday = Motivation
• Tuesday = Transformation  
• Wednesday = Wisdom
• Thursday = Throwback
• Friday = Celebration
• Saturday = Family
• Sunday = Reflection
+ Holiday awareness (Valentine's, Cinco de Mayo, etc.)

🔄 **Intelligent Rotation**
Cycles through 11 audiences, 8 emotions, 14 locations.
Weighted by day theme for relevance.

✅ **Self-Review**
AI checks its own content before posting:
- Similarity detection
- Length validation
- Brand alignment

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Built by: Elena Revicheva & CTO AIPA
Version: 3.1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
    
    bot.reply_to(message, about_text)


@bot.message_handler(commands=['stats'])
def show_stats(message):
    """Show full performance statistics"""
    total_posts = memory.memory['total_posts']
    recent_posts = memory.memory["posts"][-30:]
    
    # Calculate audience distribution
    audience_counts = {}
    emotion_counts = {}
    location_counts = {}
    
    for post in recent_posts:
        aud = post.get("audience", "unknown")
        audience_counts[aud] = audience_counts.get(aud, 0) + 1
        
        emo = post.get("emotion", "unknown")
        emotion_counts[emo] = emotion_counts.get(emo, 0) + 1
        
        loc = post.get("location", "unknown")
        location_counts[loc] = location_counts.get(loc, 0) + 1
    
    # Top items
    top_audience = max(audience_counts.items(), key=lambda x: x[1])[0] if audience_counts else "N/A"
    top_emotion = max(emotion_counts.items(), key=lambda x: x[1])[0] if emotion_counts else "N/A"
    top_location = max(location_counts.items(), key=lambda x: x[1])[0] if location_counts else "N/A"
    
    stats_text = f"""📊 **PERFORMANCE STATISTICS**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 **Content Volume**
• Total posts: {total_posts}
• Last 30 days: {len(recent_posts)} posts

👥 **Audience Distribution (last 30)**
• Most used: {top_audience}
• Unique audiences: {len(audience_counts)}

💭 **Emotional Arcs (last 30)**
• Most used: {top_emotion}
• Unique emotions: {len(emotion_counts)}

📍 **Locations (last 30)**
• Most used: {top_location}
• Unique locations: {len(location_counts)}

🎯 **Variety Score**
Audiences: {len(audience_counts)}/11
Emotions: {len(emotion_counts)}/8
Locations: {len(location_counts)}/14

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
    
    bot.reply_to(message, stats_text)


@bot.message_handler(commands=['calendar'])
def show_calendar(message):
    """Show upcoming themes and holidays"""
    now = datetime.now(PANAMA_TZ)
    
    # Next 7 days
    calendar_text = """📅 **CONTENT CALENDAR - NEXT 7 DAYS**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
    
    for i in range(7):
        future = now + timedelta(days=i)
        day_name = future.strftime("%A")
        date_str = future.strftime("%b %d")
        theme = StrategicCalendar.DAY_THEMES.get(day_name, {})
        
        # Check for special day
        special = StrategicCalendar.SPECIAL_DAYS.get((future.month, future.day))
        
        if i == 0:
            marker = "👉 TODAY"
        else:
            marker = f"   Day {i+1}"
        
        calendar_text += f"{marker}: {date_str} ({day_name})\n"
        calendar_text += f"      🎨 {theme.get('theme', 'general').title()}: {theme.get('focus', '')[:40]}\n"
        
        if special:
            calendar_text += f"      🎉 SPECIAL: {special['name']}\n"
        
        calendar_text += "\n"
    
    calendar_text += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    bot.reply_to(message, calendar_text)


@bot.message_handler(commands=['next'])
def show_next(message):
    """Preview what content is coming next"""
    strategy = StrategicCalendar.get_today_strategy()
    
    # What would be generated
    audience = IntelligentRotation.select_audience(
        memory.get_recent_audiences(),
        strategy["day_theme"]
    )
    emotion = IntelligentRotation.select_emotion(
        memory.get_recent_emotions(),
        strategy["day_theme"]
    )
    location = IntelligentRotation.select_location(
        memory.get_recent_locations()
    )
    
    next_text = f"""🔮 **NEXT CONTENT PREVIEW**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

If generated NOW, the AI would create:

📅 Day Theme: {strategy['day_theme']['theme'].upper()}
💡 Focus: {strategy['day_theme']['focus']}

👥 Target Audience: {audience.replace('_', ' ').title()}
💭 Emotional Arc: {emotion.replace('_', ' ').title()}
📍 Location: {location}

#️⃣ Hashtag Boost: {strategy['day_theme']['hashtag_boost']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏰ Next auto-post: {schedule.next_run()}

Use /daily_promo to generate now!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
    
    bot.reply_to(message, next_text)


@bot.message_handler(commands=['status'])
def show_status(message):
    """Show bot health and configuration"""
    panama_time = datetime.now(PANAMA_TZ)
    
    # Check API
    api_status = "✅ Configured" if GROQ_API_KEY else "❌ Missing"
    memory_status = "✅ Loaded" if memory.memory else "❌ Error"
    
    status_text = f"""⚙️ **BOT STATUS**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🤖 **Bot Info**
• Version: 3.1.0 (Dual campaign)
• Status: 🟢 Running
• Today: {"EspaLuz classic" if get_campaign_type_for_date(datetime.now(PANAMA_TZ)) == "espaluz" else "AI Marketing Engine"} (odd=EspaLuz, even=Engine)

🔑 **API Configuration**
• GROQ_API_KEY: {api_status}
• TELEGRAM_BOT_TOKEN: ✅ Active

🧠 **Memory System**
• Status: {memory_status}
• Posts recorded: {memory.memory['total_posts']}

📡 **Webhooks**
• Make.com: ✅ Configured
• Telegram Channel: @EspaLuz

⏰ **Scheduling**
• Current time (Panama): {panama_time.strftime('%H:%M:%S')}
• Daily post time: 6:00 PM Panama
• Next scheduled: {schedule.next_run()}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
    
    bot.reply_to(message, status_text)


@bot.message_handler(commands=['version'])
def show_version(message):
    """Show version info"""
    version_text = """🏷️ **VERSION INFO**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 EspaLuz AI Marketing Co-Founder
📌 Version: 3.1.0
📅 Dual campaign: April 2026

🔄 **Changelog v3.1:**
• Additive dual campaign: odd calendar day = EspaLuz, even = AI Marketing Engine
• `/campaign_today`, webhook `campaign_type` + `content_type`

🔄 **Changelog v3.0:**
• Added Memory System
• Added Strategic Calendar
• Added Intelligent Rotation
• Added Self-Review
• Added 10+ new commands

🔄 **Previous versions:**
• v2.0 - AI Story Generation
• v1.0 - Template-based content

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Built by: Elena Revicheva & CTO AIPA
GitHub: github.com/ElenaRevicheva/EspaLuz_Influencer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
    
    bot.reply_to(message, version_text)


def set_bot_commands():
    """Set the bot command menu in Telegram"""
    try:
        commands = [
            telebot.types.BotCommand("help", "📋 Show all commands"),
            telebot.types.BotCommand("daily_promo", "📣 Post today's campaign (alternates)"),
            telebot.types.BotCommand("campaign_today", "🔀 Which campaign today?"),
            telebot.types.BotCommand("strategy", "📅 Today's content strategy"),
            telebot.types.BotCommand("memory", "🧠 View content memory"),
            telebot.types.BotCommand("weekly", "📊 Weekly summary"),
            telebot.types.BotCommand("stats", "📈 Performance statistics"),
            telebot.types.BotCommand("calendar", "🗓️ Next 7 days themes"),
            telebot.types.BotCommand("next", "🔮 Preview next content"),
            telebot.types.BotCommand("test_ai", "🧪 Test AI generation"),
            telebot.types.BotCommand("status", "⚙️ Bot health check"),
            telebot.types.BotCommand("about", "ℹ️ About AI Co-Founder"),
        ]
        bot.set_my_commands(commands)
        print("✅ Bot command menu set")
    except Exception as e:
        print(f"⚠️ Could not set bot commands: {e}")


@bot.message_handler(commands=['memory'])
def show_memory(message):
    """Show memory stats"""
    stats = f"""🧠 CONTENT MEMORY STATS

📝 Total posts recorded: {memory.memory['total_posts']}
📅 Memory started: {memory.memory.get('created_at', 'Unknown')[:10]}

Recent 7 days:
👥 Audiences: {', '.join(set(memory.get_recent_audiences(7))) or 'None yet'}
💭 Emotions: {', '.join(set(memory.get_recent_emotions(7))) or 'None yet'}
📍 Locations: {', '.join(set(memory.get_recent_locations(7))) or 'None yet'}"""
    
    bot.reply_to(message, stats)


@bot.message_handler(commands=['weekly'])
def show_weekly(message):
    """Show weekly summary"""
    summary = memory.get_weekly_summary()
    bot.reply_to(message, summary)


@bot.message_handler(commands=['strategy'])
def show_strategy(message):
    """Show today's content strategy"""
    strategy = StrategicCalendar.get_today_strategy()
    
    response = f"""🎯 TODAY'S CONTENT STRATEGY

📅 Date: {strategy['date']}
📆 Day: {strategy['day_of_week']}
🎨 Theme: {strategy['day_theme']['theme'].upper()}
💡 Focus: {strategy['day_theme']['focus']}
#️⃣ Hashtags: {strategy['day_theme']['hashtag_boost']}
💭 Preferred emotions: {', '.join(strategy['day_theme']['emotions'])}"""
    
    if strategy.get("special_day"):
        response += f"\n\n🎉 SPECIAL DAY: {strategy['special_day']['name']}\n📌 {strategy['special_day']['focus']}"
    
    if strategy.get("upcoming_special"):
        response += f"\n\n⏰ UPCOMING: {strategy['upcoming_special']['name']} in {strategy['upcoming_special']['days_away']} days!"
    
    bot.reply_to(message, response)


@bot.message_handler(commands=['test_time'])
def test_time(message):
    panama_tz = pytz.timezone('America/Panama')
    now_panama = datetime.now(panama_tz)
    server_time = datetime.now()
    
    response = f"""⏰ Time Check:

🖥️ Server: {server_time.strftime('%Y-%m-%d %H:%M:%S')}
🇵🇦 Panama: {now_panama.strftime('%Y-%m-%d %H:%M:%S %Z')}

📅 Next scheduled promo: {schedule.next_run()}
⏰ Scheduled for: 6:00 PM Panama (23:00 UTC)
🔀 Today’s campaign: {"EspaLuz" if get_campaign_type_for_date(now_panama) == "espaluz" else "AI Marketing Engine"} (odd=EspaLuz, even=Engine)"""
    
    bot.reply_to(message, response)


@bot.message_handler(commands=['test_ai'])
def test_ai(message):
    """Test AI story generation"""
    bot.reply_to(message, "🧠 Testing AI Co-Founder v3.0...")
    
    strategy = StrategicCalendar.get_today_strategy()
    audience = IntelligentRotation.select_audience([], strategy["day_theme"])
    emotion = IntelligentRotation.select_emotion([], strategy["day_theme"])
    location = IntelligentRotation.select_location([])
    
    story = generate_ai_story(strategy, audience, emotion, location, memory)
    
    if story:
        response = f"""✅ AI Co-Founder v3.0 Test Successful!

📅 Strategy: {strategy['day_theme']['theme'].upper()}
👥 Audience: {audience}
💭 Emotion: {emotion}
📍 Location: {location}

**Hook:** {story['hook']}

**Story preview:** {story['story'][:200]}..."""
    else:
        response = "❌ AI generation failed. Check GROQ_API_KEY."
    
    bot.reply_to(message, response)


# ============================================
# SCHEDULING & LIFECYCLE
# ============================================

def schedule_checker():
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)
        except Exception as e:
            print(f"❌ Schedule checker error: {e}")
            time.sleep(60)


def force_single_instance():
    try:
        bot.remove_webhook()
        time.sleep(2)
        for i in range(3):
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/deleteWebhook"
            requests.get(url)
            time.sleep(1)
        print("🧹 Cleared all webhook connections")
        delay = random.uniform(1, 5)
        time.sleep(delay)
    except Exception as e:
        print(f"⚠️ Cleanup error: {e}")


def keep_alive():
    while True:
        try:
            print("🤖 Starting bot polling...")
            bot.polling(none_stop=True, timeout=30, long_polling_timeout=30)
        except Exception as e:
            if "409" in str(e):
                print("⚠️ Bot conflict detected - waiting...")
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
    print("=" * 60)
    print("🤖 ESPALUZ AI MARKETING CO-FOUNDER v3.1")
    print("=" * 60)
    print("✨ TRUE AI Co-Founder Capabilities:")
    print("   🧠 Memory System - Tracks all posts, avoids repetition")
    print("   📅 Strategic Calendar - Day themes, holidays, seasons")
    print("   🔄 Intelligent Rotation - Systematic audience cycling")
    print("   ✅ Self-Review - AI quality checks before posting")
    print("   📊 Performance Insights - Weekly summaries")
    print("   🔀 Dual campaign - Odd day: EspaLuz · Even day: AI Marketing Engine")
    print("=" * 60)
    
    force_single_instance()
    
    # Schedule daily promo
    schedule.every().day.at("23:00").do(send_automated_daily_promo)
    print("⏰ Scheduled daily promo for 6:00 PM Panama time (23:00 UTC)")

    # Display current state
    panama_tz = pytz.timezone('America/Panama')
    current_panama_time = datetime.now(panama_tz)
    print(f"🇵🇦 Panama time: {current_panama_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")

    # Show memory stats
    print(f"🧠 Memory loaded: {memory.memory['total_posts']} posts recorded")
    
    # Check AI availability
    if GROQ_API_KEY:
        print("✅ GROQ_API_KEY configured - AI generation enabled")
    else:
        print("⚠️ GROQ_API_KEY not set - will use fallback templates")
    
    # Start scheduler
    threading.Thread(target=schedule_checker, daemon=True).start()

    print("🤖 AI Marketing Co-Founder v3.1 is running!")
    print(f"📅 Next scheduled promo: {schedule.next_run()}")

    keep_alive()
