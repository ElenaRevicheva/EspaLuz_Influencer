// 🧠 REVOLUTIONARY EMOTIONALLY INTELLIGENT ORGANIC PROMO ENGINE
// World's first AI that understands the SOUL of language learning across ALL contexts

// 1. EXPANDED EMOTIONAL INTELLIGENCE - Deep Psychological Profiling
function detectEmotionalState(story, emotion, context) {
  const emotionPatterns = {
    // Core Emotions
    breakthrough_euphoria: /breakthrough|transformation|finally|clicked|everything changed|miracle|life-changing|game-changer/gi,
    crushing_embarrassment: /embarrassed|humiliated|stupid|ridiculous|awkward|mortified|ashamed|felt like an idiot/gi,
    desperate_frustration: /frustrated|stressed|overwhelmed|can't take it|breaking point|losing my mind|disaster/gi,
    soul_crushing_isolation: /alone|isolated|outsider|nobody understands|disconnected|invisible|excluded|foreign/gi,
    empowering_confidence: /confident|powerful|capable|strong|unstoppable|champion|proud|accomplished/gi,
    heart_melting_connection: /family|love|together|bond|belonging|accepted|understood|home|heart/gi,
    paralyzing_anxiety: /nervous|terrified|panic|scared|anxious|worried sick|can't breathe|frozen/gi,
    explosive_joy: /amazing|incredible|wonderful|thrilled|ecstatic|overjoyed|blessed|grateful/gi,
    
    // Professional Emotions
    career_limiting_fear: /career|job|professional|boss|interview|presentation|promotion|clients/gi,
    imposter_syndrome: /not qualified|don't belong|fake it|not good enough|they'll find out|pretending/gi,
    professional_breakthrough: /got the job|promotion|impressed|nailed it|respect|credibility|expert/gi,
    
    // Travel & Adventure Emotions
    adventure_excitement: /travel|explore|adventure|discover|journey|wanderlust|freedom|nomad/gi,
    culture_shock: /different|strange|don't understand|culture|customs|lost|confused|alien/gi,
    local_acceptance: /local|native|belong|accepted|insider|authentic|real|integrated/gi,
    
    // Service Provider Emotions
    business_growth: /clients|customers|business|income|growth|success|opportunity|expansion/gi,
    service_pride: /help|serve|provide|quality|excellence|professional|skilled|expert/gi,
    communication_barrier: /can't explain|misunderstood|lost client|language barrier|professional image/gi
  };
  
  // Advanced pattern matching with emotional intensity scoring
  let detectedEmotions = [];
  let intensityScore = 0;
  
  for (let [emotionType, pattern] of Object.entries(emotionPatterns)) {
    const matches = (story + " " + emotion + " " + context).match(pattern);
    if (matches) {
      detectedEmotions.push({
        emotion: emotionType,
        intensity: matches.length,
        triggers: matches.slice(0, 3) // Top 3 triggers
      });
      intensityScore += matches.length;
    }
  }
  
  // Return the most intense emotion or a blend
  if (detectedEmotions.length === 0) return { primary: 'general', intensity: 1, blend: [] };
  
  detectedEmotions.sort((a, b) => b.intensity - a.intensity);
  
  return {
    primary: detectedEmotions[0].emotion,
    intensity: intensityScore,
    blend: detectedEmotions.slice(1, 3), // Secondary emotions
    triggers: detectedEmotions[0].triggers
  };
}

// 2. EXPANDED LIFE CONTEXT & AUDIENCE DETECTION
function detectAudienceProfile(story, context) {
  const audienceProfiles = {
    // Expat Families (existing)
    expat_parent_toddler: /toddler|baby|bedtime|lullaby|diaper|feeding|terrible twos|potty training/gi,
    expat_parent_school: /school|teacher|homework|parent.?teacher|classroom|grades|bullying/gi,
    expat_parent_teen: /teenager|dating|independence|college|rebellion|identity|growing up/gi,
    expat_spouse: /husband|wife|partner|marriage|relationship|couples|romance|intimacy/gi,
    
    // Digital Nomads & Travelers
    digital_nomad: /remote work|laptop|coworking|wifi|nomad|location independent|freelance|online business/gi,
    backpacker_traveler: /backpack|hostel|budget travel|solo travel|adventure|explore|wanderlust/gi,
    business_traveler: /business trip|conference|meeting|networking|professional travel|corporate/gi,
    cultural_explorer: /culture|traditions|local experience|authentic|immersion|heritage|history/gi,
    retirement_expat: /retirement|retired|golden years|pension|senior|mature|wisdom/gi,
    
    // Professionals & Career
    healthcare_worker: /doctor|nurse|hospital|medical|patient|emergency|healthcare|clinic/gi,
    service_provider: /restaurant|hotel|tourism|guide|taxi|uber|airbnb|hospitality/gi,
    business_owner: /business|entrepreneur|company|clients|customers|sales|growth|startup/gi,
    corporate_professional: /office|corporate|executive|manager|leadership|boardroom|presentation/gi,
    teacher_educator: /teach|student|education|classroom|curriculum|learning|academic/gi,
    
    // Natives Learning English
    native_spanish_speaker: /inglés|english|trabajo|job|oportunidad|estudios|universidad|career/gi,
    service_industry_native: /turistas|tourists|tips|propinas|mejor trabajo|better job|english skills/gi,
    student_native: /university|college|scholarship|study abroad|international|global/gi,
    
    // Specific Situations
    emergency_medical: /emergency|hospital|accident|sick|doctor|pharmacy|urgent|crisis/gi,
    legal_situation: /lawyer|legal|documents|immigration|visa|police|court|official/gi,
    real_estate: /house|apartment|rent|buy|property|landlord|mortgage|neighborhood/gi,
    shopping_daily: /market|shopping|grocery|mercado|tienda|price|bargain|local store/gi
  };
  
  let profileScores = {};
  let totalMatches = 0;
  
  for (let [profile, pattern] of Object.entries(audienceProfiles)) {
    const matches = (story + " " + context).match(pattern);
    if (matches) {
      profileScores[profile] = matches.length;
      totalMatches += matches.length;
    }
  }
  
  // Find dominant profile
  const dominantProfile = Object.keys(profileScores).reduce((a, b) => 
    profileScores[a] > profileScores[b] ? a : b, 'general_learner'
  );
  
  // Calculate confidence
  const confidence = totalMatches > 0 ? (profileScores[dominantProfile] || 0) / totalMatches : 0;
  
  return {
    primary: dominantProfile,
    confidence: confidence,
    allProfiles: profileScores,
    context: detectSpecificContext(story, dominantProfile)
  };
}

function detectSpecificContext(story, profile) {
  const contextMap = {
    expat_parent_toddler: "Early parenting in a foreign country",
    expat_parent_school: "Navigating education systems abroad", 
    digital_nomad: "Building location-independent success",
    business_traveler: "Professional excellence across cultures",
    service_provider: "Elevating service quality through language",
    native_spanish_speaker: "Unlocking global opportunities with English",
    emergency_medical: "Critical communication when it matters most",
    cultural_explorer: "Deep cultural immersion and authentic connection"
  };
  
  return contextMap[profile] || "Personal growth through language mastery";
}

// 3. CULTURAL & GEOGRAPHICAL INTELLIGENCE
function detectCulturalContext(story, audience) {
  const culturalProfiles = {
    panama_expat: {
      pattern: /panama|panama city|casco viejo|canal|balboa|colon/gi,
      greeting: "¡Qué tal, fellow Panama adventurer!",
      context: "thriving in Panama's vibrant expat community",
      localTouch: "From Casco Viejo to modern Panama City",
      currency: "balboa/USD",
      uniqueChallenge: "tropical living with urban sophistication"
    },
    mexico_experience: {
      pattern: /mexico|mexican|cdmx|cancun|playa del carmen|tulum|guadalajara|familia/gi,
      greeting: "¡Órale! Fellow Mexico explorer!",
      context: "embracing Mexico's rich cultural tapestry",
      localTouch: "From ancient ruins to modern metropolis",
      currency: "pesos",
      uniqueChallenge: "regional dialects and cultural depth"
    },
    spain_integration: {
      pattern: /spain|spanish|madrid|barcelona|valencia|sevilla|españa/gi,
      greeting: "¡Hola desde España!",
      context: "integrating into Spain's sophisticated society",
      localTouch: "From Andalusian charm to Catalonian innovation",
      currency: "euros",
      uniqueChallenge: "formal vs informal cultural codes"
    },
    colombia_adventure: {
      pattern: /colombia|bogota|medellin|cartagena|colombian/gi,
      greeting: "¡Qué más! Colombia calling!",
      context: "discovering Colombia's transformation story",
      localTouch: "From coffee mountains to Caribbean coast",
      currency: "pesos colombianos",
      uniqueChallenge: "rapid cultural and economic evolution"
    },
    argentina_experience: {
      pattern: /argentina|buenos aires|mendoza|bariloche|argentinian/gi,
      greeting: "¡Che! Buenos Aires bound!",
      context: "navigating Argentina's European-Latin fusion",
      localTouch: "From tango nights to Patagonian adventures",
      currency: "pesos argentinos", 
      uniqueChallenge: "economic volatility with cultural richness"
    },
    costa_rica_lifestyle: {
      pattern: /costa rica|san jose|pura vida|ticos|guanacaste/gi,
      greeting: "¡Pura Vida! Costa Rica vibes!",
      context: "embracing the Pura Vida lifestyle",
      localTouch: "From cloud forests to pristine beaches",
      currency: "colones",
      uniqueChallenge: "eco-conscious living with modern needs"
    },
    general_latam: {
      pattern: /latin america|south america|central america|hispanic|latino/gi,
      greeting: "¡Hola, Latin America explorer!",
      context: "navigating the diverse Latin American experience",
      localTouch: "From Patagonia to the Caribbean",
      currency: "local currencies",
      uniqueChallenge: "cultural diversity across nations"
    }
  };
  
  for (let [region, data] of Object.entries(culturalProfiles)) {
    if (data.pattern.test(story)) {
      return {
        region: region,
        ...data,
        isNative: audience.includes('native') ? true : false
      };
    }
  }
  
  return culturalProfiles.general_latam;
}

// 4. REVOLUTIONARY PLATFORM-SPECIFIC EMOTIONAL ADAPTATIONS
const EMOTIONAL_ADAPTATIONS = {
  breakthrough_euphoria: {
    instagram: {
      hook: "🌟 THAT MOMENT when everything clicks...",
      validation: "This is what breakthrough feels like - pure magic ✨",
      cta: "Ready for YOUR breakthrough? → https://wa.me/50766623757",
      hashtags: "#BreakthroughMoment #LanguageMagic #EspaLuz #TransformationTuesday #Success",
      engagement: "Share YOUR breakthrough moment in the comments! 👇✨",
      tone: "celebratory_inspirational"
    },
    linkedin: {
      hook: "Professional Breakthrough: When Language Mastery Transforms Careers",
      validation: "This is how language skills become career accelerators",
      cta: "Unlock your professional potential → https://wa.me/50766623757",
      hashtags: "#CareerGrowth #ProfessionalDevelopment #LanguageSkills #Success #Leadership",
      engagement: "What language breakthrough transformed your career?",
      tone: "professional_inspiring"
    },
    tiktok: {
      hook: "POV: The exact moment Spanish finally clicked 🤯",
      validation: "When you realize you're actually FLUENT now",
      cta: "Your turn → https://wa.me/50766623757",
      hashtags: "#LanguageBreakthrough #SpanishTok #Fluent #Breakthrough #Success",
      engagement: "Duet this with your language learning win!",
      tone: "viral_relatable"
    },
    youtube: {
      hook: "The Exact Moment Everything Changed: A Real Language Breakthrough",
      validation: "Witness the power of emotional connection in language learning",
      cta: "Start your transformation → https://wa.me/50766623757",
      hashtags: "#LanguageLearning #Breakthrough #Success #Transformation #EspaLuz",
      tone: "documentary_inspiring"
    }
  },
  
  crushing_embarrassment: {
    instagram: {
      hook: "🫂 We've ALL been here... that moment when words fail you",
      validation: "Your embarrassment is valid, and you're not alone in this struggle",
      cta: "Never feel lost for words again → https://wa.me/50766623757",
      hashtags: "#LanguageStruggles #YouAreNotAlone #EspaLuz #RealTalk #Growth",
      engagement: "Comment 'SAME' if you've been here too 💔",
      tone: "empathetic_supportive"
    },
    linkedin: {
      hook: "Professional Vulnerability: When Language Barriers Impact Career Moments",
      validation: "These moments don't define your capability - they reveal growth opportunities",
      cta: "Build unshakeable professional confidence → https://wa.me/50766623757",
      hashtags: "#ProfessionalGrowth #Vulnerability #LanguageSkills #CareerDevelopment",
      engagement: "How do you handle professional language challenges?",
      tone: "professional_vulnerable"
    },
    tiktok: {
      hook: "That CRINGE moment when you said the wrong thing 😭",
      validation: "Bestie, we've ALL been there - it's part of the journey",
      cta: "Confidence incoming → https://wa.me/50766623757",
      hashtags: "#LanguageFail #Cringe #Relatable #SpanishStruggles #Growth",
      engagement: "Tell me your most embarrassing language moment 💀",
      tone: "relatable_humorous"
    }
  },
  
  adventure_excitement: {
    instagram: {
      hook: "🌎 ADVENTURE UNLOCKED: When language opens new worlds",
      validation: "This is what fearless exploration looks like",
      cta: "Unlock your next adventure → https://wa.me/50766623757",
      hashtags: "#AdventureUnlocked #TravelGoals #LanguageAdventure #Wanderlust #Freedom",
      engagement: "Where will your language skills take you next? 🗺️",
      tone: "adventurous_inspiring"
    },
    tiktok: {
      hook: "POV: You just unlocked a whole new country with Spanish 🔓",
      validation: "This is what freedom feels like",
      cta: "Unlock your world → https://wa.me/50766623757",
      hashtags: "#TravelHack #LanguageHack #Adventure #Nomad #Freedom",
      engagement: "Which country is calling your name?",
      tone: "adventure_viral"
    }
  },
  
  business_growth: {
    linkedin: {
      hook: "Revenue Impact: How Language Skills Transformed This Business",
      validation: "This is what happens when communication barriers disappear",
      cta: "Scale your business globally → https://wa.me/50766623757",
      hashtags: "#BusinessGrowth #Revenue #Communication #GlobalBusiness #Success",
      engagement: "How has language learning impacted your business?",
      tone: "business_results_focused"
    },
    instagram: {
      hook: "💰 BUSINESS BREAKTHROUGH: When language = revenue",
      validation: "Watch what happens when you can truly connect with clients",
      cta: "Grow your business → https://wa.me/50766623757",
      hashtags: "#BusinessGrowth #Entrepreneur #Success #ClientConnection #Revenue",
      engagement: "Tag an entrepreneur who needs to see this! 💼",
      tone: "business_inspiring"
    }
  },
  
  local_acceptance: {
    instagram: {
      hook: "💕 THAT FEELING when locals treat you like family...",
      validation: "This is what true belonging feels like",
      cta: "Find your tribe → https://wa.me/50766623757", 
      hashtags: "#Belonging #LocalAcceptance #CulturalConnection #Family #Home",
      engagement: "Where did you find your chosen family? 🏡",
      tone: "heartwarming_community"
    },
    tiktok: {
      hook: "When the abuela invites you for Sunday dinner 🥺❤️",
      validation: "This is what acceptance looks like",
      cta: "Find your familia → https://wa.me/50766623757",
      hashtags: "#Abuela #Family #Acceptance #Wholesome #Belonging",
      engagement: "This made me emotional 🥺",
      tone: "wholesome_emotional"
    }
  }
};

// 5. AUDIENCE-SPECIFIC MESSAGING FRAMEWORKS
const AUDIENCE_MESSAGING = {
  digital_nomad: {
    pain_points: ["Isolation while working remotely", "Professional networking barriers", "Client communication struggles"],
    aspirations: ["Location independence", "Global client base", "Cultural integration"],
    language: "freedom, flexibility, adventure, opportunity, independence",
    cta_style: "action-oriented, opportunity-focused"
  },
  
  service_provider: {
    pain_points: ["Lost business due to language barriers", "Lower tips from tourists", "Professional credibility"],
    aspirations: ["Higher income", "Better job opportunities", "Professional respect"],
    language: "income, growth, opportunity, professional, success",
    cta_style: "results-focused, income-oriented"
  },
  
  native_spanish_speaker: {
    pain_points: ["Limited job opportunities", "Academic barriers", "Global communication"],
    aspirations: ["Better career prospects", "International opportunities", "Personal growth"],
    language: "oportunidad, crecimiento, futuro, éxito, progreso",
    cta_style: "future-focused, opportunity-driven"
  },
  
  cultural_explorer: {
    pain_points: ["Surface-level tourist experience", "Cultural barriers", "Authentic connection"],
    aspirations: ["Deep cultural immersion", "Authentic relationships", "True understanding"],
    language: "authentic, deep, meaningful, connection, culture",
    cta_style: "experience-focused, depth-oriented"
  },
  
  business_traveler: {
    pain_points: ["Professional embarrassment", "Missed opportunities", "Cultural misunderstandings"],
    aspirations: ["Professional confidence", "Business success", "Cultural competence"],
    language: "professional, confidence, success, competence, respect",
    cta_style: "professional, results-driven"
  }
};

// 6. REVOLUTIONARY CONTENT GENERATION ENGINE
function generateEmotionallyIntelligentContent(inputData) {
  // Parse input data
  const rawStory = inputData.story || inputData.text || "";
  const rawEmotion = inputData.emotion || "";
  const rawHook = inputData.hook || "";
  const rawTransformation = inputData.transformation || "";
  const rawCTA = inputData.cta || "";
  const videoURL = inputData.videoURL || "https://youtube.com/shorts/4l9B4Rc1SxY";
  const imageURL = inputData.imageURL || "https://raw.githubusercontent.com/ElenaRevicheva/EspaLuz_Influencer/main/converted_4x5_second_image.jpg";
  
  // AI Analysis
  const emotionalProfile = detectEmotionalState(rawStory, rawEmotion, rawHook);
  const audienceProfile = detectAudienceProfile(rawStory, rawHook);
  const culturalContext = detectCulturalContext(rawStory, audienceProfile.primary);
  
  // Get messaging framework
  const audienceMsg = AUDIENCE_MESSAGING[audienceProfile.primary] || AUDIENCE_MESSAGING.cultural_explorer;
  const emotionalContent = EMOTIONAL_ADAPTATIONS[emotionalProfile.primary] || EMOTIONAL_ADAPTATIONS.breakthrough_euphoria;
  
  // Generate platform-specific content
  const platforms = generatePlatformContent(emotionalContent, audienceMsg, culturalContext, {
    story: rawStory,
    transformation: rawTransformation,
    emotion: emotionalProfile,
    audience: audienceProfile,
    videoURL,
    imageURL
  });
  
  return {
    // Analysis Results
    emotionalProfile,
    audienceProfile,
    culturalContext,
    
    // Generated Content
    ...platforms,
    
    // Optimization Data
    optimalTiming: calculateOptimalTiming(emotionalProfile, audienceProfile),
    mediaStrategy: selectOptimalMedia(emotionalProfile, audienceProfile, videoURL, imageURL),
    engagementPrediction: predictEngagement(emotionalProfile, audienceProfile)
  };
}

function generatePlatformContent(emotionalContent, audienceMsg, culturalContext, data) {
  const whatsappLink = "https://wa.me/50766623757";
  
  // Instagram - Community & Visual Storytelling
  const instagramContent = `${emotionalContent.instagram.hook}

${culturalContext.greeting}

${data.story}

${data.transformation}

${emotionalContent.instagram.validation}

${culturalContext.context} - you're not alone in this journey.

${emotionalContent.instagram.cta}

${emotionalContent.instagram.hashtags}

${emotionalContent.instagram.engagement}`.slice(0, 2200);

  // LinkedIn - Professional & Thought Leadership
  const linkedinTitle = emotionalContent.linkedin.hook;
  const linkedinBody = `${data.story}

${data.transformation}

${emotionalContent.linkedin.validation}.

For professionals navigating ${culturalContext.context}, language mastery isn't just personal growth - it's career acceleration.

${emotionalContent.linkedin.cta}

${emotionalContent.linkedin.hashtags}

${emotionalContent.linkedin.engagement}`.replace(/[🔥💕🚨😭✨🫂🌟🥺❤️🌎💰🤯]/g, '').slice(0, 2950);

  // TikTok - Viral & Authentic
  const tiktokContent = `${emotionalContent.tiktok.hook}

${emotionalContent.tiktok.validation}!

${emotionalContent.tiktok.cta}

${emotionalContent.tiktok.hashtags}`.slice(0, 145);

  // YouTube - Story-Driven & Educational
  const youtubeTitle = emotionalContent.youtube.hook.slice(0, 95);
  const youtubeDescription = `${data.story}

${data.transformation}

This is what happens when language learning meets emotional intelligence.

${culturalContext.greeting} Welcome to a community that understands your journey.

${emotionalContent.instagram.cta}

🎯 Perfect for:
• ${audienceMsg.aspirations.join('\n• ')}

#EspaLuz #EmotionalAI #LanguageLearning #${culturalContext.region}`.slice(0, 4900);

  // Twitter/X - Punchy & Shareable
  const twitterContent = `${data.emotion.triggers?.[0] || "Language breakthrough"} 

${emotionalContent.instagram.validation}

${whatsappLink}

#EspaLuz #LanguageLearning`.slice(0, 270);

  // Facebook - Community Building
  const facebookContent = `${culturalContext.greeting}

${emotionalContent.instagram.hook}

${data.story}

${data.transformation}

For everyone ${culturalContext.context} - this community celebrates every breakthrough, supports every struggle, and believes in every dream.

${emotionalContent.instagram.cta}

${emotionalContent.instagram.hashtags}`.slice(0, 2200);

  return {
    instagramContent,
    linkedinTitle,
    linkedinBody,
    tiktokContent,
    youtubeTitle,
    youtubeDescription,
    twitterContent,
    facebookContent
  };
}

function calculateOptimalTiming(emotionalProfile, audienceProfile) {
  const emotionalTiming = {
    crushing_embarrassment: 0, // Immediate support
    desperate_frustration: 0, // Urgent help
    paralyzing_anxiety: 15, // Quick but gentle
    breakthrough_euphoria: 60, // Let excitement build
    empowering_confidence: 90, // Perfect timing for celebration
    adventure_excitement: 30, // Strike while inspiration is hot
    business_growth: 120, // Professional timing
    local_acceptance: 45 // Heartwarming timing
  };
  
  const audienceTiming = {
    digital_nomad: 30, // Always online
    business_traveler: 60, // Professional windows
    service_provider: 15, // Quick consumption
    cultural_explorer: 45, // Contemplative timing
    native_spanish_speaker: 30 // Eager for opportunities
  };
  
  const baseDelay = emotionalTiming[emotionalProfile.primary] || 30;
  const audienceModifier = audienceTiming[audienceProfile.primary] || 30;
  
  return Math.max(0, (baseDelay + audienceModifier) / 2);
}

function selectOptimalMedia(emotionalProfile, audienceProfile, videoURL, imageURL) {
  const videoEmotions = ['breakthrough_euphoria', 'adventure_excitement', 'empowering_confidence'];
  const videoAudiences = ['digital_nomad', 'cultural_explorer', 'business_traveler'];
  
  const useVideo = videoEmotions.includes(emotionalProfile.primary) || 
                   videoAudiences.includes(audienceProfile.primary);
  
  return {
    instagram: useVideo ? videoURL : imageURL,
    linkedin: imageURL, // Professional preference
    tiktok: videoURL, // Always video
    youtube: videoURL, // Always video
    facebook: useVideo ? videoURL : imageURL,
    twitter: imageURL // Quick engagement
  };
}

function predictEngagement(emotionalProfile, audienceProfile) {
  const emotionalEngagement = {
    breakthrough_euphoria: 9.5,
    crushing_embarrassment: 8.7,
    adventure_excitement: 8.9,
    empowering_confidence: 8.5,
    local_acceptance: 9.2,
    business_growth: 7.8
  };
  
  const audienceEngagement = {
    digital_nomad: 8.8,
    service_provider: 8.2,
    cultural_explorer: 9.1,
    business_traveler: 7.9,
    native_spanish_speaker: 8.5
  };
  
  const baseScore = emotionalEngagement[emotionalProfile.primary] || 8.0;
  const audienceScore = audienceEngagement[audienceProfile.primary] || 8.0;
  
  return {
    predicted_score: ((baseScore + audienceScore) / 2).toFixed(1),
    confidence: emotionalProfile.intensity > 3 ? 'high' : 'medium',
    viral_potential: baseScore > 9.0 ? 'high' : 'medium'
  };
}

// MAIN EXECUTION FUNCTION
const inputData = arguments[0] || {};
const result = generateEmotionallyIntelligentContent(inputData);

// Output the complete emotional intelligence analysis and content
output = result;