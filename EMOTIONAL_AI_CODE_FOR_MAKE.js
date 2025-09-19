// 🧠 EMOTIONAL INTELLIGENCE ENGINE FOR MAKE.COM
// Copy this entire code into your cloned scenario's parser module

// 1. EMOTION DETECTION & CLASSIFICATION
function detectEmotionalState(story, emotion) {
  const emotionPatterns = {
    frustration: /panic|meltdown|frustrated|stressed|overwhelmed|disaster|chaos/gi,
    embarrassment: /embarrassed|ashamed|ridiculous|awkward|humiliated|felt stupid/gi,
    anxiety: /nervous|worried|terrified|scared|panic|afraid|anxious/gi,
    isolation: /alone|isolated|outsider|silent|disconnected|lonely|excluded/gi,
    breakthrough: /breakthrough|transformation|confidence|proud|champion|success|victory/gi,
    joy: /joy|happy|excited|amazing|wonderful|love|thrilled|delighted/gi,
    empowerment: /powerful|strong|capable|advocate|prepared|confident|empowered/gi,
    connection: /family|together|bond|close|relationship|love|connection/gi
  };
  
  // Check story content for emotional indicators
  for (let [emotionType, pattern] of Object.entries(emotionPatterns)) {
    if (pattern.test(story)) {
      return emotionType;
    }
  }
  
  // Fallback to emotion field analysis
  if (emotion.includes('robotic')) return 'frustration';
  if (emotion.includes('isolation')) return 'isolation';
  if (emotion.includes('CONNECTION')) return 'connection';
  if (emotion.includes('PRIDE')) return 'empowerment';
  if (emotion.includes('ROMANCE')) return 'joy';
  
  return 'general';
}

// 2. PARENTING STAGE & LIFE CONTEXT DETECTION
function detectLifeContext(story) {
  const contexts = {
    early_parenting: /toddler|bedtime|lullaby|baby|diaper|feeding/gi,
    school_age: /school|teacher|homework|parent.?teacher|classroom/gi,
    teen_parenting: /teenager|independence|dating|college/gi,
    professional: /work|office|meeting|business|career|job/gi,
    healthcare: /doctor|hospital|pharmacy|medical|emergency|sick/gi,
    social: /market|shopping|neighbors|community|friends/gi,
    romance: /husband|wife|date|dance|relationship|partner/gi,
    family_gathering: /reunion|family|relatives|celebration|holiday/gi
  };
  
  for (let [context, pattern] of Object.entries(contexts)) {
    if (pattern.test(story)) return context;
  }
  return 'general';
}

// 3. CULTURAL CONTEXT AWARENESS
function detectCulturalContext(story) {
  if (/panama|panama city/gi.test(story)) return 'panama';
  if (/mexico|mexican|familia/gi.test(story)) return 'mexico';
  if (/spain|spanish|españa/gi.test(story)) return 'spain';
  return 'expat_general';
}

// 4. EMOTIONAL ADAPTATIONS BY PLATFORM
const EMOTIONAL_ADAPTATIONS = {
  frustration: {
    instagram: {
      hook: "🫂 You're not alone in this struggle...",
      validation: "Every parent has felt this exact overwhelm",
      cta: "Find your calm → https://wa.me/50766623757",
      hashtags: "#MomStruggles #YouAreNotAlone #EspaLuz #ParentingSupport #BilingualMom",
      engagement: "Comment 'SAME' if you've been here 👇"
    },
    linkedin: {
      hook: "Professional challenge: Language barriers in critical moments",
      validation: "Workplace communication shouldn't add to your stress",
      cta: "Build workplace confidence → https://wa.me/50766623757",
      hashtags: "#ProfessionalDevelopment #WorkplaceConfidence #EspaLuz #CareerGrowth",
      engagement: "What's your experience with language barriers at work?"
    },
    tiktok: {
      hook: "POV: When Spanish fails you at the worst moment 😭",
      validation: "We've ALL been there, bestie",
      cta: "Never again → https://wa.me/50766623757",
      hashtags: "#ParentingFail #SpanishStruggles #EspaLuz #MomTok #RelatableContent",
      engagement: "Duet this with your own fail story!"
    },
    youtube: {
      hook: "The Moment Every Parent Dreads: Lost in Translation",
      validation: "If you've ever felt helpless because of language barriers",
      cta: "Transform your confidence → https://wa.me/50766623757",
      hashtags: "#ParentingStruggles #LanguageBarriers #EspaLuz #BilingualParenting"
    }
  },
  
  breakthrough: {
    instagram: {
      hook: "🌟 TRANSFORMATION ALERT:",
      validation: "This is what breakthrough looks like",
      cta: "Your transformation awaits → https://wa.me/50766623757",
      hashtags: "#TransformationTuesday #SuccessStory #EspaLuz #Empowerment #BilingualWin",
      engagement: "Save this for motivation! ✨"
    },
    linkedin: {
      hook: "Success story: From language barrier to career advancement",
      validation: "Professional growth through confident communication",
      cta: "Unlock your potential → https://wa.me/50766623757",
      hashtags: "#CareerGrowth #SuccessStory #ProfessionalWin #EspaLuz #Leadership",
      engagement: "Share your own professional breakthrough in the comments"
    },
    tiktok: {
      hook: "That moment when everything clicks 🔥✨",
      validation: "THIS is the energy we're manifesting",
      cta: "Get your glow-up → https://wa.me/50766623757",
      hashtags: "#GlowUp #Transformation #SuccessStory #EspaLuz #MainCharacterEnergy",
      engagement: "Use this sound for your own win!"
    },
    youtube: {
      hook: "From Struggle to Success: A Real EspaLuz Transformation",
      validation: "Proof that breakthrough moments are real",
      cta: "Start your journey → https://wa.me/50766623757",
      hashtags: "#TransformationStory #LanguageLearning #EspaLuz #SuccessStory"
    }
  },
  
  connection: {
    instagram: {
      hook: "💕 The moment everything changed...",
      validation: "Connection is what we're all seeking",
      cta: "Build deeper bonds → https://wa.me/50766623757",
      hashtags: "#FamilyConnection #BilingualBonding #EspaLuz #FamilyFirst #Love",
      engagement: "Tag someone who gets this feeling 💕"
    },
    linkedin: {
      hook: "The power of authentic connection in multicultural environments",
      validation: "True connection transcends language barriers",
      cta: "Strengthen your relationships → https://wa.me/50766623757",
      hashtags: "#Relationships #CulturalIntelligence #EspaLuz #GlobalMindset",
      engagement: "How do you build connections across cultures?"
    },
    tiktok: {
      hook: "When you finally feel like family 🥺❤️",
      validation: "This feeling hits different",
      cta: "Find your tribe → https://wa.me/50766623757",
      hashtags: "#FamilyFeels #Belonging #EspaLuz #WholesomeContent #Connection",
      engagement: "This made me cry happy tears 🥺"
    }
  }
};

// 5. LIFE CONTEXT SPECIFIC MESSAGING
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
    community: "For parents who refuse to be lost in translation when it matters most"
  }
};

// 6. CULTURAL NUANCES
const CULTURAL_ADAPTATIONS = {
  panama: {
    greeting: "¡Qué tal, fellow Panama expat!",
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
  }
};

// MAIN PROCESSING FUNCTION
const inputData = arguments[0] || {};
const rawStory = inputData.story || inputData.text || "";
const rawEmotion = inputData.emotion || "";
const rawHook = inputData.hook || "";
const rawTransformation = inputData.transformation || "";
const rawCTA = inputData.cta || "";
const rawHashtags = inputData.hashtags || "";
const videoURL = inputData.videoURL || "https://youtube.com/shorts/4l9B4Rc1SxY";
const imageURL = inputData.imageURL || "https://raw.githubusercontent.com/ElenaRevicheva/EspaLuz_Influencer/main/converted_4x5_second_image.jpg";

// EMOTIONAL INTELLIGENCE ANALYSIS
const detectedEmotion = detectEmotionalState(rawStory, rawEmotion);
const lifeContext = detectLifeContext(rawStory);
const culturalContext = detectCulturalContext(rawStory);

// GET EMOTIONAL ADAPTATIONS
const emotionalContent = EMOTIONAL_ADAPTATIONS[detectedEmotion] || EMOTIONAL_ADAPTATIONS.general || {
  instagram: { hook: rawHook, validation: "Your journey matters", cta: rawCTA, hashtags: rawHashtags },
  linkedin: { hook: rawHook, validation: "Professional growth through language", cta: rawCTA, hashtags: rawHashtags },
  tiktok: { hook: rawHook, validation: "You've got this!", cta: rawCTA, hashtags: rawHashtags },
  youtube: { hook: rawHook, validation: "Every story matters", cta: rawCTA, hashtags: rawHashtags }
};

// GET CONTEXT MESSAGING
const contextMsg = CONTEXT_MESSAGING[lifeContext] || {
  empathy: "Every journey has its challenges...",
  hope: "Your breakthrough is closer than you think",
  community: "For everyone on this beautiful journey"
};

// GET CULTURAL ADAPTATIONS
const culturalMsg = CULTURAL_ADAPTATIONS[culturalContext] || {
  greeting: "¡Hola, amazing human!",
  context: "navigating your unique journey",
  community: "your incredible community"
};

// BUILD EMOTIONALLY INTELLIGENT CONTENT FOR EACH PLATFORM

// INSTAGRAM - Emotionally Rich & Community-Focused
const INSTAGRAM_CONTENT = `${emotionalContent.instagram.hook}

${contextMsg.empathy}

${rawStory}

${rawTransformation}

${emotionalContent.instagram.validation}. ${contextMsg.hope}.

${emotionalContent.instagram.cta}

${emotionalContent.instagram.hashtags}

${emotionalContent.instagram.engagement}`.slice(0, 2200);

// LINKEDIN - Professional & Empowering
const LINKEDIN_TITLE = emotionalContent.linkedin.hook;
const LINKEDIN_BODY = `${contextMsg.empathy}

${rawStory}

${rawTransformation}

${emotionalContent.linkedin.validation}.

${contextMsg.community} - this one's for you.

${emotionalContent.linkedin.cta}

${emotionalContent.linkedin.hashtags}

${emotionalContent.linkedin.engagement}`.replace(/[🔥💕🚨😭✨🫂🌟🥺❤️]/g, '').slice(0, 2950);

// TIKTOK - Authentic & Relatable
const TIKTOK_CONTENT = `${emotionalContent.tiktok.hook}

${emotionalContent.tiktok.validation}!

${emotionalContent.tiktok.cta}

${emotionalContent.tiktok.hashtags}`.slice(0, 145);

// YOUTUBE - Story-Driven & Inspiring
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

${rawCTA}

#EspaLuz #EmotionalAI`.slice(0, 270);

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
  frustration: 0, // Post immediately - urgent emotional support
  anxiety: 30, // Short delay - gentle approach
  breakthrough: 60, // Celebrate with perfect timing
  isolation: 15, // Quick but thoughtful response
  connection: 45, // Let the emotion build
  joy: 30, // Share happiness promptly
  empowerment: 90 // Let success marinate
};

const optimalDelay = EMOTIONAL_TIMING[detectedEmotion] || 0;

// MEDIA STRATEGY BY PLATFORM & EMOTION
const MEDIA_STRATEGY = {
  youtube: videoURL, // Always video for Shorts
  instagram: detectedEmotion === 'breakthrough' ? videoURL : imageURL, // Video for wins, image for stories
  linkedin: imageURL, // Professional image preferred
  tiktok: videoURL, // Always video
  facebook: detectedEmotion === 'connection' ? videoURL : imageURL, // Video for emotional moments
  twitter: imageURL // Image for quick engagement
};

// OUTPUT EMOTIONAL INTELLIGENCE DATA
output = {
  // Original data
  originalStory: rawStory,
  originalEmotion: rawEmotion,
  videoURL: videoURL,
  imageURL: imageURL,
  
  // Emotional Intelligence Analysis
  detectedEmotion: detectedEmotion,
  lifeContext: lifeContext,
  culturalContext: culturalContext,
  optimalDelay: optimalDelay,
  
  // Platform-Optimized Content
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
  
  // Engagement Data
  emotionalValidation: emotionalContent[Object.keys(emotionalContent)[0]]?.validation || "Your journey matters",
  communityMessage: contextMsg.community,
  culturalGreeting: culturalMsg.greeting
};