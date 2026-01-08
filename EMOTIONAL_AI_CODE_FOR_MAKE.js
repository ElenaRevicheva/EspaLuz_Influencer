// 🧠 EMOTIONAL INTELLIGENCE ENGINE FOR MAKE.COM v2.0
// Updated for AI-generated content from EspaLuz AI Influencer Co-Founder
// Copy this entire code into your Make.com scenario's JavaScript/Code module

// ============================================
// 1. AUDIENCE NAME FORMATTING
// ============================================
function formatAudienceName(audience) {
  const audienceNames = {
    'expat_parent': 'fellow expat parent',
    'digital_nomad': 'fellow digital nomad',
    'service_provider': 'hardworking professional',
    'business_traveler': 'ambitious professional',
    'cultural_explorer': 'fellow traveler',
    'healthcare_worker': 'dedicated healthcare hero',
    'entrepreneur': 'fellow entrepreneur',
    'retiree': 'fellow adventurer',
    'teacher': 'fellow educator',
    'immigrant': 'fellow newcomer',
    'general_learner': 'language learner'
  };
  return audienceNames[audience] || 'amazing human';
}

// ============================================
// 2. EMOTION DETECTION & CLASSIFICATION
// ============================================
function detectEmotionalState(story, emotion) {
  const emotionPatterns = {
    frustration: /panic|meltdown|frustrated|stressed|overwhelmed|disaster|chaos/gi,
    embarrassment: /embarrassed|ashamed|ridiculous|awkward|humiliated|felt stupid|cringe|mortified|burning|face red/gi,
    anxiety: /nervous|worried|terrified|scared|panic|afraid|anxious/gi,
    isolation: /alone|isolated|outsider|silent|disconnected|lonely|excluded/gi,
    breakthrough: /breakthrough|transformation|confidence|proud|champion|success|victory|nailed|landed/gi,
    joy: /joy|happy|excited|amazing|wonderful|love|thrilled|delighted/gi,
    empowerment: /powerful|strong|capable|advocate|prepared|confident|empowered/gi,
    connection: /family|together|bond|close|relationship|love|connection|friends|accepted/gi
  };
  
  for (let [emotionType, pattern] of Object.entries(emotionPatterns)) {
    if (pattern.test(story)) {
      return emotionType;
    }
  }
  
  // Fallback to emotion field analysis
  if (emotion && emotion.includes('embarrass')) return 'embarrassment';
  if (emotion && emotion.includes('robotic')) return 'frustration';
  if (emotion && emotion.includes('isolation')) return 'isolation';
  if (emotion && emotion.includes('CONNECTION')) return 'connection';
  if (emotion && emotion.includes('PRIDE')) return 'empowerment';
  
  return 'general';
}

// ============================================
// 3. LIFE CONTEXT DETECTION
// ============================================
function detectLifeContext(story) {
  const contexts = {
    early_parenting: /toddler|bedtime|lullaby|baby|diaper|feeding/gi,
    school_age: /school|teacher|homework|parent.?teacher|classroom/gi,
    teen_parenting: /teenager|independence|dating|college/gi,
    professional: /work|office|meeting|business|career|job|client|presentation|contract/gi,
    healthcare: /doctor|hospital|pharmacy|medical|emergency|sick|nurse|patient/gi,
    social: /market|shopping|neighbors|community|friends|restaurant|bar|cafe/gi,
    romance: /husband|wife|date|dance|relationship|partner/gi,
    family_gathering: /reunion|family|relatives|celebration|holiday/gi,
    travel: /travel|tourist|backpack|hostel|airport|restaurant|local|culture/gi
  };
  
  for (let [context, pattern] of Object.entries(contexts)) {
    if (pattern.test(story)) return context;
  }
  return 'general';
}

// ============================================
// 4. CULTURAL CONTEXT AWARENESS (EXPANDED)
// ============================================
function detectCulturalContext(story) {
  if (/panama|panama city/gi.test(story)) return 'panama';
  if (/mexico|mexican|familia|ciudad de mexico/gi.test(story)) return 'mexico';
  if (/spain|spanish|españa|madrid|barcelona/gi.test(story)) return 'spain';
  if (/colombia|colombian|medell[íi]n|bogot[áa]|cartagena|el poblado/gi.test(story)) return 'colombia';
  if (/argentina|buenos aires|argentine/gi.test(story)) return 'argentina';
  if (/peru|lima|peruvian/gi.test(story)) return 'peru';
  if (/costa rica|san jose|tico/gi.test(story)) return 'costa_rica';
  return 'latam_general';
}

// ============================================
// 5. EMOTIONAL ADAPTATIONS BY PLATFORM
// ============================================
const EMOTIONAL_ADAPTATIONS = {
  embarrassment: {
    instagram: {
      hook: "😅 We've ALL been there...",
      validation: "Those cringe moments? They're actually growth moments",
      cta: "Start your FREE 7-day trial → https://wa.me/50766623757",
      hashtags: "#LanguageFail #LearnFromMistakes #EspaLuz #BilingualJourney #GrowthMindset",
      engagement: "Drop a 😬 if you've had a language fail moment!"
    },
    linkedin: {
      hook: "The language mistake that changed everything",
      validation: "Professional growth often starts with an embarrassing moment",
      cta: "Try FREE for 7 days → https://wa.me/50766623757",
      hashtags: "#ProfessionalGrowth #LanguageLearning #EspaLuz #GrowthMindset #CareerDevelopment",
      engagement: "What's your most memorable language learning moment?"
    },
    tiktok: {
      hook: "POV: Your Spanish just betrayed you 😭💀",
      validation: "The way I SCREAMED reading this",
      cta: "FREE trial awaits → https://wa.me/50766623757",
      hashtags: "#SpanishFail #LanguageFail #EspaLuz #Relatable #LearnSpanish",
      engagement: "Stitch this with your own fail!"
    },
    youtube: {
      hook: "From Embarrassing Fail to Fluent: A Real Story",
      validation: "Every fluent speaker has a cringe story",
      cta: "Start your transformation → https://wa.me/50766623757",
      hashtags: "#LanguageLearning #EspaLuz #LearnSpanish #Transformation"
    }
  },
  
  frustration: {
    instagram: {
      hook: "🫂 You're not alone in this struggle...",
      validation: "Every learner has felt this exact overwhelm",
      cta: "Start your FREE trial → https://wa.me/50766623757",
      hashtags: "#LanguageStruggles #YouAreNotAlone #EspaLuz #LearningSupport #BilingualJourney",
      engagement: "Comment 'SAME' if you've been here 👇"
    },
    linkedin: {
      hook: "Professional challenge: Language barriers in critical moments",
      validation: "Workplace communication shouldn't add to your stress",
      cta: "Try FREE for 7 days → https://wa.me/50766623757",
      hashtags: "#ProfessionalDevelopment #WorkplaceConfidence #EspaLuz #CareerGrowth",
      engagement: "What's your experience with language barriers at work?"
    },
    tiktok: {
      hook: "POV: When Spanish fails you at the worst moment 😭",
      validation: "We've ALL been there, bestie",
      cta: "FREE trial awaits → https://wa.me/50766623757",
      hashtags: "#SpanishStruggles #EspaLuz #LanguageLearning #RelatableContent",
      engagement: "Duet this with your own fail story!"
    },
    youtube: {
      hook: "The Moment Every Learner Dreads: Lost in Translation",
      validation: "If you've ever felt helpless because of language barriers",
      cta: "Start FREE today → https://wa.me/50766623757",
      hashtags: "#LanguageBarriers #EspaLuz #BilingualJourney"
    }
  },
  
  breakthrough: {
    instagram: {
      hook: "🌟 TRANSFORMATION ALERT:",
      validation: "This is what breakthrough looks like",
      cta: "Try FREE for 7 days → https://wa.me/50766623757",
      hashtags: "#TransformationTuesday #SuccessStory #EspaLuz #Empowerment #BilingualWin",
      engagement: "Save this for motivation! ✨"
    },
    linkedin: {
      hook: "Success story: From language barrier to career advancement",
      validation: "Professional growth through confident communication",
      cta: "Start your FREE trial → https://wa.me/50766623757",
      hashtags: "#CareerGrowth #SuccessStory #ProfessionalWin #EspaLuz #Leadership",
      engagement: "Share your own professional breakthrough in the comments"
    },
    tiktok: {
      hook: "That moment when everything clicks 🔥✨",
      validation: "THIS is the energy we're manifesting",
      cta: "Try FREE now → https://wa.me/50766623757",
      hashtags: "#GlowUp #Transformation #SuccessStory #EspaLuz #MainCharacterEnergy",
      engagement: "Use this sound for your own win!"
    },
    youtube: {
      hook: "From Struggle to Success: A Real EspaLuz Transformation",
      validation: "Proof that breakthrough moments are real",
      cta: "Start FREE today → https://wa.me/50766623757",
      hashtags: "#TransformationStory #LanguageLearning #EspaLuz #SuccessStory"
    }
  },
  
  connection: {
    instagram: {
      hook: "💕 The moment everything changed...",
      validation: "Connection is what we're all seeking",
      cta: "Try FREE for 7 days → https://wa.me/50766623757",
      hashtags: "#Connection #BilingualBonding #EspaLuz #CulturalConnection #Love",
      engagement: "Tag someone who gets this feeling 💕"
    },
    linkedin: {
      hook: "The power of authentic connection in multicultural environments",
      validation: "True connection transcends language barriers",
      cta: "Start FREE today → https://wa.me/50766623757",
      hashtags: "#Relationships #CulturalIntelligence #EspaLuz #GlobalMindset",
      engagement: "How do you build connections across cultures?"
    },
    tiktok: {
      hook: "When you finally feel like family 🥺❤️",
      validation: "This feeling hits different",
      cta: "Try FREE now → https://wa.me/50766623757",
      hashtags: "#FamilyFeels #Belonging #EspaLuz #WholesomeContent #Connection",
      engagement: "This made me cry happy tears 🥺"
    },
    youtube: {
      hook: "Building Real Connections Through Language",
      validation: "The best moments come from genuine connection",
      cta: "Start FREE today → https://wa.me/50766623757",
      hashtags: "#Connection #LanguageLearning #EspaLuz #CulturalExchange"
    }
  },
  
  general: {
    instagram: {
      hook: "✨ Your language journey matters...",
      validation: "Every step forward counts",
      cta: "Start FREE today → https://wa.me/50766623757",
      hashtags: "#LanguageLearning #EspaLuz #BilingualJourney #LearnSpanish #GrowthMindset",
      engagement: "What's your language learning goal? 👇"
    },
    linkedin: {
      hook: "The power of language learning in today's global world",
      validation: "Communication skills open doors",
      cta: "Try FREE for 7 days → https://wa.me/50766623757",
      hashtags: "#LanguageLearning #ProfessionalGrowth #EspaLuz #GlobalCommunication",
      engagement: "How has language learning impacted your career?"
    },
    tiktok: {
      hook: "Language learning glow-up incoming ✨",
      validation: "This is your sign to start",
      cta: "Try FREE → https://wa.me/50766623757",
      hashtags: "#LanguageLearning #EspaLuz #LearnSpanish #GlowUp",
      engagement: "Save for later!"
    },
    youtube: {
      hook: "Transform Your Communication Skills",
      validation: "Every fluent speaker started somewhere",
      cta: "Start FREE today → https://wa.me/50766623757",
      hashtags: "#LanguageLearning #EspaLuz #LearnSpanish"
    }
  }
};

// ============================================
// 6. LIFE CONTEXT MESSAGING
// ============================================
const CONTEXT_MESSAGING = {
  early_parenting: {
    empathy: "Those early parenting days when every moment feels crucial...",
    hope: "You're building something beautiful with your little one",
    community: "For all the parents in the thick of it"
  },
  professional: {
    empathy: "Your career shouldn't suffer because of language barriers...",
    hope: "Professional confidence is within your reach",
    community: "For ambitious professionals breaking barriers"
  },
  healthcare: {
    empathy: "Healthcare moments require clear, confident communication...",
    hope: "You can advocate powerfully for your family's health",
    community: "For those who refuse to be lost in translation when it matters"
  },
  travel: {
    empathy: "Traveling is amazing, but language barriers can dim the experience...",
    hope: "Imagine connecting authentically with every local you meet",
    community: "For travelers who want more than just tourist experiences"
  },
  social: {
    empathy: "Social situations can feel isolating when you can't fully express yourself...",
    hope: "Real connections are just a conversation away",
    community: "For everyone building community in a new language"
  },
  general: {
    empathy: "Every journey has its challenges...",
    hope: "Your breakthrough is closer than you think",
    community: "For everyone on this beautiful journey"
  }
};

// ============================================
// 7. CULTURAL ADAPTATIONS (EXPANDED)
// ============================================
const CULTURAL_ADAPTATIONS = {
  panama: {
    greeting: "¡Qué xopa, fellow Panama expat!",
    context: "navigating life in Panama",
    community: "the amazing expat community here"
  },
  mexico: {
    greeting: "¡Hola, México family!",
    context: "embracing Mexican culture",
    community: "your Mexican familia"
  },
  spain: {
    greeting: "¡Hola desde España!",
    context: "integrating into Spanish society",
    community: "your Spanish community"
  },
  colombia: {
    greeting: "¡Hola, parcero!",
    context: "exploring beautiful Colombia",
    community: "the warm Colombian community"
  },
  argentina: {
    greeting: "¡Che, hola!",
    context: "discovering Argentina",
    community: "the passionate Argentine community"
  },
  peru: {
    greeting: "¡Hola, amigo!",
    context: "experiencing Peru",
    community: "the welcoming Peruvian community"
  },
  costa_rica: {
    greeting: "¡Pura vida!",
    context: "living the Costa Rican dream",
    community: "the pura vida community"
  },
  latam_general: {
    greeting: "¡Hola, fellow adventurer!",
    context: "exploring Latin America",
    community: "the incredible Latino community"
  }
};

// ============================================
// MAIN PROCESSING FUNCTION
// ============================================
const inputData = arguments[0] || {};

// Extract input data
const rawStory = inputData.story || inputData.text || "";
const rawEmotion = inputData.emotion || "";
const rawHook = inputData.hook || "";
const rawTransformation = inputData.transformation || "";
const rawCTA = inputData.cta || "";
const rawHashtags = inputData.hashtags || "";
const videoURL = inputData.videoURL || "https://youtube.com/shorts/4l9B4Rc1SxY";
const imageURL = inputData.imageURL || "https://raw.githubusercontent.com/ElenaRevicheva/EspaLuz_Influencer/main/espaluz_qr_4x5.jpg";
const audience = inputData.audience || "general_learner";

// Format audience for display
const friendlyAudience = formatAudienceName(audience);

// EMOTIONAL INTELLIGENCE ANALYSIS
const detectedEmotion = detectEmotionalState(rawStory, rawEmotion);
const lifeContext = detectLifeContext(rawStory);
const culturalContext = detectCulturalContext(rawStory);

// GET EMOTIONAL ADAPTATIONS (with fallback)
const emotionalContent = EMOTIONAL_ADAPTATIONS[detectedEmotion] || EMOTIONAL_ADAPTATIONS.general;

// GET CONTEXT MESSAGING (with fallback)
const contextMsg = CONTEXT_MESSAGING[lifeContext] || CONTEXT_MESSAGING.general;

// GET CULTURAL ADAPTATIONS (with fallback)
const culturalMsg = CULTURAL_ADAPTATIONS[culturalContext] || CULTURAL_ADAPTATIONS.latam_general;

// ============================================
// BUILD PLATFORM-SPECIFIC CONTENT
// ============================================

// INSTAGRAM - Emotionally Rich & Community-Focused
const INSTAGRAM_CONTENT = `${emotionalContent.instagram.hook}

${contextMsg.empathy}

${rawStory}

${rawTransformation}

${emotionalContent.instagram.validation}. ${contextMsg.hope}.

${emotionalContent.instagram.cta}

${emotionalContent.instagram.hashtags}

${emotionalContent.instagram.engagement}`.slice(0, 2200);

// LINKEDIN - Professional & Clean (NO raw variable names, NO emojis in body)
const LINKEDIN_TITLE = emotionalContent.linkedin.hook;
const LINKEDIN_BODY = `${contextMsg.empathy}

${rawStory}

${rawTransformation}

${emotionalContent.linkedin.validation}.

${contextMsg.community} - this one's for you.

${emotionalContent.linkedin.cta}

${emotionalContent.linkedin.hashtags}

${emotionalContent.linkedin.engagement}`.replace(/[🔥💕🚨😭✨🫂🌟🥺❤️😅😬💀🎯💰💬🖥️🌍🇵🇦📅⏰]/g, '').slice(0, 2950);

// TIKTOK - Short & Punchy
const TIKTOK_CONTENT = `${emotionalContent.tiktok.hook}

${emotionalContent.tiktok.validation}!

${emotionalContent.tiktok.cta}

${emotionalContent.tiktok.hashtags}`.slice(0, 145);

// YOUTUBE - Story-Driven
const YOUTUBE_TITLE = emotionalContent.youtube.hook.slice(0, 95);
const YOUTUBE_DESCRIPTION = `${emotionalContent.youtube.validation}...

${rawStory}

${rawTransformation}

${contextMsg.hope}.

${emotionalContent.youtube.cta}

${culturalMsg.greeting} Welcome to ${culturalMsg.community}.

${emotionalContent.youtube.hashtags || rawHashtags}`.slice(0, 4900);

// TWITTER/X - Punchy & Engaging
const TWITTER_CONTENT = `${rawHook.slice(0, 50)}...

${emotionalContent.instagram.validation}.

${rawCTA || emotionalContent.instagram.cta}

#EspaLuz #LearnSpanish`.slice(0, 270);

// FACEBOOK - Community & Story-Focused
const FACEBOOK_CONTENT = `${culturalMsg.greeting}

${emotionalContent.instagram.hook}

${rawStory}

${rawTransformation}

${contextMsg.community} - you inspire us every day.

${emotionalContent.instagram.cta}

${emotionalContent.instagram.hashtags}`.slice(0, 2200);

// EMOTIONAL TIMING OPTIMIZATION
const EMOTIONAL_TIMING = {
  frustration: 0,
  embarrassment: 0,
  anxiety: 30,
  breakthrough: 60,
  isolation: 15,
  connection: 45,
  joy: 30,
  empowerment: 90,
  general: 30
};

const optimalDelay = EMOTIONAL_TIMING[detectedEmotion] || 30;

// MEDIA STRATEGY BY PLATFORM & EMOTION
const MEDIA_STRATEGY = {
  youtube: videoURL,
  instagram: detectedEmotion === 'breakthrough' ? videoURL : imageURL,
  linkedin: imageURL,
  tiktok: videoURL,
  facebook: detectedEmotion === 'connection' ? videoURL : imageURL,
  twitter: imageURL
};

// ============================================
// OUTPUT (CLEAN - no debug metadata!)
// ============================================
output = {
  // Original data
  originalStory: rawStory,
  originalEmotion: rawEmotion,
  videoURL: videoURL,
  imageURL: imageURL,
  
  // Analysis results
  detectedEmotion: detectedEmotion,
  lifeContext: lifeContext,
  culturalContext: culturalContext,
  optimalDelay: optimalDelay,
  friendlyAudience: friendlyAudience,
  
  // Platform-Optimized Content (CLEAN!)
  instagramContent: INSTAGRAM_CONTENT,
  linkedinTitle: LINKEDIN_TITLE,
  linkedinBody: LINKEDIN_BODY,
  tiktokContent: TIKTOK_CONTENT,
  youtubeTitle: YOUTUBE_TITLE,
  youtubeDescription: YOUTUBE_DESCRIPTION,
  twitterContent: TWITTER_CONTENT,
  facebookContent: FACEBOOK_CONTENT,
  
  // Media Strategy
  instagramMedia: MEDIA_STRATEGY.instagram,
  linkedinMedia: MEDIA_STRATEGY.linkedin,
  tiktokMedia: MEDIA_STRATEGY.tiktok,
  youtubeMedia: MEDIA_STRATEGY.youtube,
  facebookMedia: MEDIA_STRATEGY.facebook,
  twitterMedia: MEDIA_STRATEGY.twitter,
  
  // Engagement helpers
  emotionalValidation: emotionalContent.instagram.validation,
  communityMessage: contextMsg.community,
  culturalGreeting: culturalMsg.greeting
};
