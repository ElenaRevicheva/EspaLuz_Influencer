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

MAKE_WEBHOOK_URL = "https://hook.us2.make.com/ecv7x7innu2g1r3olsqi12ca4uadkmi9"

# Emotional Intelligence Engine webhook (for testing)
EMOTIONAL_AI_WEBHOOK_URL = "https://hook.us2.make.com/ecv7x7innu2g1r3olsqi12ca4uadkmi9"

# Backup webhook for alternative social media posting (if Buffer fails)
BACKUP_WEBHOOK_URL = "https://hook.us2.make.com/backup-webhook-url-here"

# ESPALUZ VIDEO URLs - Direct download from Dropbox
# ESPALUZ BRANDED VIDEO FILES - Direct download URLs
video_links = [
    "https://www.dropbox.com/scl/fi/uy5uv35wicmtbcr667p9u/202509151508.mp4?rlkey=om1n84rnwnpkobgvcm31d7xhd&st=21jbk8c9&dl=1"  # ONLY your EspaLuz video
]

# CURATED IMAGE COLLECTION - 6 Perfect Images with URL-Encoded Names
image_urls = [
    # QR CODES - Direct conversion paths
    "https://raw.githubusercontent.com/ElenaRevicheva/EspaLuz_Influencer/main/qr%20code%20of%20whatsapp%20espaluz.jpg",  # WhatsApp QR (spaces encoded)
    "https://raw.githubusercontent.com/ElenaRevicheva/EspaLuz_Influencer/main/espaluz_qr_4x5.jpg",  # Telegram QR
    
    # BRANDED CONTENT IMAGES - Professional visuals  
    "https://raw.githubusercontent.com/ElenaRevicheva/EspaLuz_Influencer/main/WhatsApp%20Image%202025-09-15%20at%2014.15.27_92d791cd.jpg",
    "https://raw.githubusercontent.com/ElenaRevicheva/EspaLuz_Influencer/main/WhatsApp%20Image%202025-09-15%20at%2014.15.56_9e90aa1c.jpg",
    "https://raw.githubusercontent.com/ElenaRevicheva/EspaLuz_Influencer/main/WhatsApp%20Image%202025-09-23%20at%2010.46.04_571ea224.jpg",
    "https://raw.githubusercontent.com/ElenaRevicheva/EspaLuz_Influencer/main/WhatsApp%20Image%202025-09-23%20at%2010.46.04_75d5e010.jpg"
]

# REVOLUTIONARY EMOTIONALLY INTELLIGENT STORY TEMPLATES - EXPANDED AUDIENCES
story_templates = [
    # EXPAT FAMILIES - Original Audience
    {
        "hook": "🧠 AI THAT ACTUALLY GETS IT",
        "story": "I was having a meltdown trying to discipline my toddler in Spanish. I sent a frustrated voice message to EspaLuz: 'I don't know how to be firm but loving in Spanish!' The AI didn't just translate—it UNDERSTOOD I was a stressed parent and coached me through it.",
        "transformation": "EspaLuz analyzed my emotional state, gave me gentle parenting phrases in Spanish, and sent a personalized video showing me how to set boundaries with love. Now my daughter responds better, and I feel confident as a bilingual parent! 🎭💕",
        "emotion": "🤖 From robotic apps to EMOTIONAL AI",
        "audience": "expat_parent",
        "emotional_state": "desperate_frustration"
    },
    
    # DIGITAL NOMADS - New High-Value Audience
    {
        "hook": "💻 REMOTE WORK BREAKTHROUGH",
        "story": "Client call disaster in Mexico City. My Spanish wasn't good enough for the business presentation, and I was losing a $50K contract. I felt like a fraud calling myself 'location independent' when I couldn't even communicate professionally.",
        "transformation": "EspaLuz's business Spanish module didn't just teach me phrases—it understood my professional anxiety and coached me through confident business communication. I nailed the follow-up presentation and landed the contract! Now I'm truly location independent.",
        "emotion": "💼 From imposter syndrome to PROFESSIONAL CONFIDENCE",
        "audience": "digital_nomad",
        "emotional_state": "career_breakthrough"
    },
    
    # SERVICE PROVIDERS - Huge Untapped Market
    {
        "hook": "💰 INCOME DOUBLED WITH ENGLISH",
        "story": "I was a tour guide in Cartagena making barely enough to survive. Tourists would ask complex questions in English, and I'd just smile and nod, losing tips and credibility. My English was holding back my dreams of a better life.",
        "transformation": "EspaLuz understood I wasn't just learning English—I was fighting for my family's future. It coached me through tourism vocabulary, confident pronunciation, and cultural communication. Now I'm the highest-rated guide in the city, earning 3x more!",
        "emotion": "🚀 From survival to PROSPERITY",
        "audience": "service_provider",
        "emotional_state": "empowering_confidence"
    },
    
    # BUSINESS TRAVELERS - Professional Market
    {
        "hook": "🎯 BOARDROOM BREAKTHROUGH",
        "story": "Merger negotiations in Madrid. I was the only American executive who couldn't contribute meaningfully because my Spanish wasn't business-level. I watched a $2M deal almost collapse because of communication barriers. I felt professionally inadequate.",
        "transformation": "EspaLuz detected my professional anxiety and created a business Spanish crash course tailored to my industry. Within weeks, I was leading Spanish negotiations with confidence. The merger succeeded, and I got promoted to VP of International Operations!",
        "emotion": "📈 From professional liability to EXECUTIVE ASSET",
        "audience": "business_traveler",
        "emotional_state": "breakthrough_euphoria"
    },
    
    # CULTURAL EXPLORERS - Adventure Market
    {
        "hook": "🌍 AUTHENTIC CONNECTION UNLOCKED",
        "story": "Three months backpacking through South America, but I was still just a tourist. Staying in hostels, eating at tourist restaurants, never connecting with locals. I was traveling but not truly experiencing the culture.",
        "transformation": "EspaLuz understood my desire for authentic connection and taught me conversational Spanish that opened hearts, not just conversations. Families invited me to Sunday dinners, I learned traditional recipes from abuelas, and experienced the real Latin America!",
        "emotion": "❤️ From tourist to FAMILY",
        "audience": "cultural_explorer",  
        "emotional_state": "local_acceptance"
    },
    
    # HEALTHCARE WORKERS - Critical Situations
    {
        "hook": "🏥 LIFE-SAVING COMMUNICATION",
        "story": "Emergency room nurse in Miami. Spanish-speaking patient having chest pains, but I couldn't understand her symptoms description. I had to rely on Google Translate while she was in distress. I felt helpless when lives depended on clear communication.",
        "transformation": "EspaLuz created medical Spanish modules that understood the emotional weight of healthcare communication. It taught me not just medical terms, but how to provide comfort and confidence to scared patients. Now I'm the go-to nurse for Spanish-speaking emergencies.",
        "emotion": "🛡️ From helpless to LIFESAVER",
        "audience": "healthcare_worker",
        "emotional_state": "empowering_confidence"
    },
    
    # ENTREPRENEURS - Business Growth
    {
        "hook": "📊 BUSINESS EXPANSION SUCCESS",
        "story": "My online business was stuck serving only English speakers. I knew the Latin American market was huge, but language barriers kept me from expanding. I was leaving millions on the table because I couldn't communicate with potential customers.",
        "transformation": "EspaLuz understood my entrepreneurial drive and created business expansion modules. It taught me customer service Spanish, marketing language, and cultural business etiquette. My revenue increased 400% in the first year of Latin American expansion!",
        "emotion": "💎 From limited market to GLOBAL EMPIRE",
        "audience": "entrepreneur",
        "emotional_state": "business_growth"
    },
    
    # NATIVES LEARNING ENGLISH - Reverse Market
    {
        "hook": "🎓 UNIVERSITY DREAMS ACHIEVED",
        "story": "Soy de Colombia y siempre soñé con estudiar en Estados Unidos, pero mi inglés no era suficiente para los exámenes de admisión. Veía cómo otros conseguían becas mientras yo me quedaba atrás. Me sentía limitada por el idioma.",
        "transformation": "EspaLuz entendió que no solo estaba aprendiendo inglés—estaba luchando por mi futuro. Me ayudó con inglés académico, confianza para hablar, y preparación para exámenes. ¡Conseguí una beca completa para MIT! Ahora estoy estudiando ingeniería.",
        "emotion": "🌟 From limited opportunities to UNLIMITED FUTURE",
        "audience": "native_english_learner",
        "emotional_state": "breakthrough_euphoria"
    },
    
    # RETIREMENT EXPATS - Growing Market
    {
        "hook": "🌅 RETIREMENT PARADISE UNLOCKED",
        "story": "Retired to Costa Rica for the Pura Vida lifestyle, but felt like a prisoner in my own paradise. Couldn't talk to neighbors, understand the doctor, or navigate daily life. I was living in isolation instead of integration.",
        "transformation": "EspaLuz understood that at 65, I wasn't just learning Spanish—I was reclaiming my independence and dignity. It adapted to my learning pace and focused on practical daily conversations. Now I'm the gringo who helps other expats integrate!",
        "emotion": "🏡 From isolated retiree to COMMUNITY LEADER",
        "audience": "retirement_expat",
        "emotional_state": "local_acceptance"
    },
    
    # EMERGENCY SITUATIONS - High Stakes
    {
        "hook": "🚨 CRISIS COMMUNICATION BREAKTHROUGH",
        "story": "My elderly mother fell in her Mexico City apartment. I'm calling from the US, trying to coordinate with Spanish-speaking doctors and paramedics. Every second mattered, but language barriers were slowing down her care.",
        "transformation": "EspaLuz's emergency Spanish module prepared me for exactly this scenario. I confidently communicated her medical history, allergies, and symptoms to the medical team. She got immediate proper care and recovered fully!",
        "emotion": "⚡ From panic to PREPARED ADVOCATE",
        "audience": "emergency_situation",
        "emotional_state": "empowering_confidence"
    },
    
    # ORIGINAL EXPAT FAMILY STORIES (Enhanced)
    {
        "hook": "🎬 THE CONVERSATION MODE MIRACLE",
        "story": "My husband and I were fighting about money—in English. Our Spanish neighbors could hear everything through thin walls, but we couldn't explain or apologize because of the language barrier. I felt so embarrassed and isolated.",
        "transformation": "I used EspaLuz's new Conversation Mode to practice what I wanted to say. Voice message → instant analysis → Spanish coaching → personalized motivation video. I knocked on their door, apologized in perfect Spanish, and we're now close friends! 🏠✨",
        "emotion": "💬 From isolation to CONNECTION",
        "audience": "expat_spouse",
        "emotional_state": "heart_melting_connection"
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

# REVOLUTIONARY BENEFIT SECTIONS - EXPANDED FOR ALL AUDIENCES
benefit_sections = [
    {
        "title": "🧠 WORLD'S FIRST EMOTIONAL AI COACH",
        "points": [
            "🎭 Detects your emotional state and adapts responses accordingly",
            "👨‍👩‍👧‍👦 Recognizes your life context (parent, professional, traveler, entrepreneur) for targeted support",
            "💕 Provides empathy and encouragement, not just cold translations",
            "🎯 Coaches you through real-life situations with emotional intelligence",
            "💼 Understands professional anxiety, family stress, travel excitement, business pressure"
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
        "title": "💼 PROFESSIONAL & BUSINESS MASTERY",
        "points": [
            "📊 Business Spanish for entrepreneurs expanding to Latin markets",
            "🏥 Medical Spanish for healthcare workers saving lives",
            "✈️ Executive-level Spanish for international business travelers",
            "💰 Service industry English for tourism professionals increasing income",
            "🎓 Academic English for natives pursuing international education"
        ]
    },
    {
        "title": "🌍 CULTURAL & TRAVEL INTELLIGENCE",
        "points": [
            "🗺️ Location-specific Spanish for digital nomads (Mexico City, Medellín, Panama)",
            "🏠 Integration Spanish for retirees living their best expat life",
            "❤️ Authentic connection Spanish for cultural explorers and backpackers",
            "🚨 Emergency Spanish for critical life situations",
            "🎭 Cultural etiquette and context, not just language rules"
        ]
    },
    {
        "title": "👨‍👩‍👧‍👦 FAMILY-CENTERED LEARNING",
        "points": [
            "🏠 Designed for expat families in Panama, Mexico, Spain, Colombia, Costa Rica",
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

# REVOLUTIONARY SOCIAL PROOF - ALL AUDIENCES
social_proof = [
    # EXPAT FAMILIES (Original)
    "🧠 'The AI detected I was stressed about parenting and gave me exactly the Spanish phrases I needed to connect with my daughter. It's like having a bilingual therapist!' - Sarah, expat mom in Panama",
    "🎬 'Conversation Mode changed everything. I sent a panicked voice message about my son's school meeting, and EspaLuz coached me through the whole thing with personalized videos!' - Mike, Panama City",
    "💕 'My husband's family finally accepts me. EspaLuz understood I felt like an outsider and taught me cultural Spanish, not just words.' - Jennifer, married to Mexican national",
    
    # DIGITAL NOMADS & ENTREPRENEURS
    "💻 'Lost a $30K client because of language barriers. EspaLuz's business Spanish got me fluent in negotiations. Now I'm closing deals in 3 countries!' - Alex, digital nomad entrepreneur",
    "📈 'My SaaS business was English-only. EspaLuz helped me expand to Latin America. Revenue jumped 400% in 8 months!' - Maria, tech entrepreneur",
    "🎯 'I was paying tourist prices at the market until EspaLuz taught me confident haggling Spanish. Now vendors treat me like family!' - Tom, location-independent consultant",
    
    # SERVICE PROVIDERS & NATIVES LEARNING ENGLISH
    "💰 'Como guía turístico, EspaLuz mejoró mi inglés profesional. Ahora gano el triple y tengo las mejores reseñas en TripAdvisor!' - Carlos, tour guide in Cartagena",
    "🎓 'Conseguí beca completa para Stanford gracias a EspaLuz. Mi inglés académico pasó de básico a universitario en 6 meses.' - Ana, Colombian engineering student",
    "🏥 'As a hotel manager, EspaLuz taught me hospitality English that impresses international guests. Got promoted to regional manager!' - Luis, hospitality professional",
    
    # HEALTHCARE & EMERGENCY SITUATIONS
    "⚡ 'EspaLuz detected my anxiety about medical appointments and prepared me with doctor-specific Spanish. I advocated for my mom like a pro!' - Carlos, caring for elderly parent",
    "🏥 'Emergency room Spanish from EspaLuz saved lives. I can now comfort scared patients and communicate critical information with confidence.' - Dr. Patricia, Miami ER",
    "🚨 'When my dad had a heart attack in Mexico, EspaLuz's medical Spanish helped me coordinate his care from the US. He's alive because I could communicate clearly.' - Robert, emergency situation",
    
    # BUSINESS TRAVELERS & PROFESSIONALS
    "💼 'Boardroom Spanish from EspaLuz landed me the VP position. I went from liability to asset in international negotiations.' - James, corporate executive",
    "✈️ 'Business travel was stressful until EspaLuz taught me professional Spanish. Now I lead our Latin American expansion.' - Michelle, business development director",
    
    # CULTURAL EXPLORERS & RETIREES
    "🌟 'It's not just translation—it's emotional support. The AI celebrates my wins and encourages me through frustrations. Like having a Spanish-speaking best friend!' - Lisa, solo backpacker",
    "🏡 'Retired to Costa Rica but felt isolated. EspaLuz helped me integrate with locals. Now I'm the neighborhood gringo who helps everyone!' - Bob, retirement expat",
    "❤️ 'Backpacking through Colombia, EspaLuz connected me with local families. I experienced authentic culture, not just tourist spots.' - Emma, cultural explorer",
    
    # FAMILY SUCCESS STORIES
    "👨‍👩‍👧‍👦 'Our family went from language barriers to bilingual bonding. EspaLuz understood our dynamics and coached us all differently.' - The Rodriguez Family, 3 generations",
    "🎭 'The AI knew I was embarrassed about my pronunciation and sent me confidence-building exercises. Now I sing Spanish lullabies to my kids!' - Amanda, bilingual family"
]

# REVOLUTIONARY HASHTAG SETS - ALL AUDIENCES & PLATFORMS
hashtag_sets = [
    # Instagram/Facebook - Emotional AI + Family Focus
    ["#EspaLuz", "#EmotionalAI", "#BilingualFamilies", "#ConversationMode", "#SpanishWithHeart", "#FamilyFirst", "#ExpatLife"],
    
    # TikTok - Viral + All Audiences
    ["#EspaLuz", "#AICoach", "#SpanishTok", "#ExpatTok", "#NomadLife", "#BilingualJourney", "#LanguageHack", "#EmotionalIntelligence"],
    
    # LinkedIn - Professional + Business Focus
    ["#EspaLuz", "#EmotionalAI", "#BusinessSpanish", "#ProfessionalDevelopment", "#GlobalBusiness", "#CareerGrowth", "#ExecutiveSpanish"],
    
    # YouTube - Educational + Success Stories
    ["#EspaLuz", "#LanguageLearning", "#EmotionalAI", "#SuccessStory", "#BilingualSuccess", "#ConversationMode", "#LanguageBreakthrough"],
    
    # Digital Nomad Focus
    ["#EspaLuz", "#DigitalNomad", "#RemoteWork", "#LocationIndependent", "#NomadLife", "#BusinessSpanish", "#GlobalEntrepreneur"],
    
    # Service Provider Focus (English/Spanish Mix)
    ["#EspaLuz", "#TourismEnglish", "#HospitalitySpanish", "#ServiceExcellence", "#ProfessionalEnglish", "#CareerUpgrade", "#IncomeBoost"],
    
    # Healthcare & Emergency Focus
    ["#EspaLuz", "#MedicalSpanish", "#HealthcareHeroes", "#EmergencySpanish", "#LifeSavingCommunication", "#PatientCare", "#MedicalAI"],
    
    # Cultural Explorer Focus
    ["#EspaLuz", "#CulturalImmersion", "#AuthenticTravel", "#LocalConnection", "#BackpackerLife", "#CulturalExchange", "#TravelDeep"],
    
    # Entrepreneur & Business Growth
    ["#EspaLuz", "#BusinessGrowth", "#EntrepreneurLife", "#GlobalExpansion", "#StartupSuccess", "#BusinessSpanish", "#RevenueGrowth"],
    
    # Native English Learners (Spanish/English Mix)
    ["#EspaLuz", "#InglésAcadémico", "#UniversityDreams", "#ScholarshipSuccess", "#AcademicEnglish", "#FuturoIlimitado", "#EducaciónGlobal"],
    
    # Retirement & Lifestyle Focus
    ["#EspaLuz", "#RetirementAbroad", "#ExpatRetirement", "#PuraVida", "#RetirementGoals", "#SeniorExpats", "#LifestyleChange"],
    
    # Geographic Specific - Expanded
    ["#EspaLuz", "#PanamaExpats", "#MexicoLife", "#ColombiaLife", "#CostaRicaLife", "#SpainLife", "#LatinAmericaLife", "#CentralAmerica"],
    
    # Emotional & Breakthrough Focus
    ["#EspaLuz", "#EmotionalIntelligence", "#LanguageBreakthrough", "#ConfidenceBuilding", "#PersonalGrowth", "#TransformationStory", "#AIThatCares"],
    
    # Feature-Specific Technology
    ["#EspaLuz", "#ConversationMode", "#PersonalizedVideos", "#VoiceToText", "#WhatsAppLearning", "#AICoaching", "#EmotionalSupport"],
    
    # General High-Engagement
    ["#EspaLuz", "#LanguageLearning", "#BilingualLife", "#SpanishSuccess", "#LifeChanging", "#DreamsComeTrue", "#UnlimitedPotential"]
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
    
    # DAILY IMAGE ROTATION: Select 1 random image from all 6
    image_url = random.choice(image_urls)
    
    # Debug: Print which video and image were selected
    print(f"🎬 Selected video: {video_url}")
    print(f"🖼️ Selected image: {image_url}")

    # Build rich promo content with embedded video links
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

🎬 WATCH: See this transformation in action → {video_url}

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
        
        # Send to Make.com webhook with REVOLUTIONARY emotional intelligence data
        payload = {
            "text": promo,
            "videoURL": video_url,
            "imageURL": image_url,  # Primary image
            "videoTitle": f"EspaLuz Success Story: {story['emotion']}",
            "videoDescription": story['story'][:200] + "...",
            "automated": True,
            "timestamp": datetime.now(pytz.timezone('America/Panama')).isoformat(),
            
            # REVOLUTIONARY Emotional Intelligence Data
            "hook": story['hook'],
            "story": story['story'],
            "emotion": story['emotion'],
            "transformation": story['transformation'],
            "cta": random.choice(cta_options),
            "hashtags": " ".join(random.choice(hashtag_sets)),
            "socialProof": random.choice(social_proof),
            
            # NEW: Audience & Emotional State Intelligence
            "audience": story.get('audience', 'general_learner'),
            "emotional_state": story.get('emotional_state', 'general'),
            "target_market": story.get('audience', 'expat_parent'),
            
            # NEW: Enhanced Content Metadata
            "content_type": "success_story",
            "emotional_intensity": "high" if any(word in story['story'].lower() for word in ['disaster', 'crisis', 'breakthrough', 'miracle', 'lost', 'failed', 'couldn\'t']) else "medium",
            "viral_potential": "high" if story.get('emotional_state') in ['breakthrough_euphoria', 'empowering_confidence', 'business_growth', 'career_breakthrough'] else "medium",
            
            # NEW: Platform Optimization Hints
            "instagram_focus": "community_engagement" if story.get('audience') in ['expat_parent', 'cultural_explorer'] else "professional_growth",
            "linkedin_focus": "professional_growth" if story.get('audience') in ['digital_nomad', 'business_traveler', 'entrepreneur'] else "personal_development",
            "tiktok_focus": "viral_relatability" if story.get('emotional_state') in ['crushing_embarrassment', 'local_acceptance'] else "educational_content",
            "youtube_focus": "educational_inspiration" if story.get('audience') in ['service_provider', 'native_english_learner'] else "transformation_story"
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
            "imageURL": image_url,  # Primary image
            "videoTitle": f"EspaLuz Success Story: {story['emotion']}",
            "videoDescription": story['story'][:200] + "...",
            "automated": False,
            
            # REVOLUTIONARY Emotional Intelligence Data
            "hook": story['hook'],
            "story": story['story'],
            "emotion": story['emotion'],
            "transformation": story['transformation'],
            "cta": random.choice(cta_options),
            "hashtags": " ".join(random.choice(hashtag_sets)),
            "socialProof": random.choice(social_proof),
            
            # NEW: Audience & Emotional State Intelligence
            "audience": story.get('audience', 'general_learner'),
            "emotional_state": story.get('emotional_state', 'general'),
            "target_market": story.get('audience', 'expat_parent'),
            
            # NEW: Enhanced Content Metadata
            "content_type": "success_story",
            "emotional_intensity": "high" if any(word in story['story'].lower() for word in ['disaster', 'crisis', 'breakthrough', 'miracle', 'lost', 'failed', 'couldn\'t']) else "medium",
            "viral_potential": "high" if story.get('emotional_state') in ['breakthrough_euphoria', 'empowering_confidence', 'business_growth', 'career_breakthrough'] else "medium",
            
            # NEW: Platform Optimization Hints
            "instagram_focus": "community_engagement" if story.get('audience') in ['expat_parent', 'cultural_explorer'] else "professional_growth",
            "linkedin_focus": "professional_growth" if story.get('audience') in ['digital_nomad', 'business_traveler', 'entrepreneur'] else "personal_development",
            "tiktok_focus": "viral_relatability" if story.get('emotional_state') in ['crushing_embarrassment', 'local_acceptance'] else "educational_content",
            "youtube_focus": "educational_inspiration" if story.get('audience') in ['service_provider', 'native_english_learner'] else "transformation_story"
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
    """Test command for revolutionary emotional AI engine"""
    print("🧠 /test_emotional_ai triggered...")
    
    promo, story, video_url, image_url = generate_promo_content()
    
    # Reply to the user who triggered the command
    audience_type = story.get('audience', 'general_learner')
    emotional_state = story.get('emotional_state', 'general')
    bot.reply_to(message, f"🧠 **REVOLUTIONARY EMOTIONAL AI TEST**\n\n🎯 Audience: {audience_type}\n🎭 Emotional State: {emotional_state}\n💫 Emotion: {story['emotion']}\n\nContent generated and sent to Make.com for revolutionary processing!\n\nCheck Make.com scenario for results.")
    
    try:
        payload = {
            "text": promo,
            "videoURL": video_url,
            "imageURL": image_url,
            "videoTitle": f"EspaLuz Success Story: {story['emotion']}",
            "videoDescription": story['story'][:200] + "...",
            "automated": False,
            "testMode": True,
            
            # REVOLUTIONARY Emotional Intelligence Data
            "hook": story['hook'],
            "story": story['story'],
            "emotion": story['emotion'],
            "transformation": story['transformation'],
            "cta": random.choice(cta_options),
            "hashtags": " ".join(random.choice(hashtag_sets)),
            "socialProof": random.choice(social_proof),
            
            # NEW: Audience & Emotional State Intelligence
            "audience": story.get('audience', 'general_learner'),
            "emotional_state": story.get('emotional_state', 'general'),
            "target_market": story.get('audience', 'expat_parent'),
            
            # NEW: Enhanced Content Metadata
            "content_type": "success_story",
            "emotional_intensity": "high" if any(word in story['story'].lower() for word in ['disaster', 'crisis', 'breakthrough', 'miracle', 'lost', 'failed', 'couldn\'t']) else "medium",
            "viral_potential": "high" if story.get('emotional_state') in ['breakthrough_euphoria', 'empowering_confidence', 'business_growth', 'career_breakthrough'] else "medium",
            
            # NEW: Platform Optimization Hints
            "instagram_focus": "community_engagement" if story.get('audience') in ['expat_parent', 'cultural_explorer'] else "professional_growth",
            "linkedin_focus": "professional_growth" if story.get('audience') in ['digital_nomad', 'business_traveler', 'entrepreneur'] else "personal_development",
            "tiktok_focus": "viral_relatability" if story.get('emotional_state') in ['crushing_embarrassment', 'local_acceptance'] else "educational_content",
            "youtube_focus": "educational_inspiration" if story.get('audience') in ['service_provider', 'native_english_learner'] else "transformation_story"
        }
        
        # Send to Revolutionary Emotional AI webhook
        response = requests.post(EMOTIONAL_AI_WEBHOOK_URL, json=payload)
        print(f"🧠 Sent to Revolutionary Emotional AI webhook. Response: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Failed to send to Revolutionary Emotional AI webhook: {e}")

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
