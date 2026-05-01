"""
cto_milestone_module.py — CTO AIPA collaboration for EspaLuz Influencer.

ADDITIVE / SAFE:
- Called from send_automated_daily_promo() ONLY on even days, before the
  regular marketing_engine slot. If this returns None for any reason,
  the original marketing_engine content runs as always.
- Never raises. Never modifies existing logic.

WHAT IT DOES:
1. Polls http://127.0.0.1:8080/api/influencer-updates (CMO AIPA, same Oracle VM)
2. If a pending CTO milestone exists, generates an Instagram/Telegram-ready
   story via Groq — same dict shape as existing story generators.
3. After successful post, marks the milestone as posted_influencer.

TONE RULES (non-negotiable):
- Zero tech jargon. HR managers and business owners are the target.
- Frame every milestone as a HUMAN outcome: what changed for a real person?
- Elena's identity: former Deputy CEO/CLO (7 yrs) who rebuilt herself as an
  AI-augmented builder. Not a junior. Not intimidating. Trustworthy and real.
- Never say "neural network", "model weights", "LangGraph node" — say
  "the system now remembers", "the bot now decides for itself", etc.
- Always end with: why this matters for someone hiring or partnering with Elena.
"""

import json
import logging
import os
import urllib.request
import urllib.error
from datetime import datetime
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

# Same Oracle VM — CMO AIPA web service
CMO_API_URL = os.environ.get("CMO_API_URL", "http://127.0.0.1:8080")
X_UPDATES_SECRET = os.environ.get("X_UPDATES_SECRET", "")

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.3-70b-versatile"

PORTFOLIO_URL = "https://aideazz.xyz/portfolio"


# ── HTTP helpers ──────────────────────────────────────────────────────────────

def _get(path: str) -> Optional[Dict]:
    url = f"{CMO_API_URL.rstrip('/')}{path}"
    headers = {"User-Agent": "EspaLuz-Influencer/3.1"}
    if X_UPDATES_SECRET:
        headers["Authorization"] = f"Bearer {X_UPDATES_SECRET}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as resp:
            return json.loads(resp.read())
    except Exception as e:
        logger.warning(f"[CTO-Milestone] GET {path} failed: {e}")
        return None


def _post(path: str, data: Dict) -> bool:
    url = f"{CMO_API_URL.rstrip('/')}{path}"
    body = json.dumps(data).encode()
    headers = {
        "Content-Type": "application/json",
        "Content-Length": str(len(body)),
        "User-Agent": "EspaLuz-Influencer/3.1",
    }
    if X_UPDATES_SECRET:
        headers["Authorization"] = f"Bearer {X_UPDATES_SECRET}"
    try:
        req = urllib.request.Request(url, data=body, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=8) as resp:
            result = json.loads(resp.read())
            return bool(result.get("ok"))
    except Exception as e:
        logger.warning(f"[CTO-Milestone] POST {path} failed: {e}")
        return False


# ── Story generation ─────────────────────────────────────────────────────────

# Human-readable milestone translations (non-technical framing)
MILESTONE_HUMAN_FRAMES = {
    "pgvector RAG": {
        "what": "Our Spanish tutor now genuinely remembers every student — not just the last message, but the full learning history. It knows your weak spots before you do.",
        "why_business": "This is what separates AI tools that feel robotic from ones that feel like a thoughtful tutor. Memory makes retention real.",
        "emotion": "warmth",
        "audience": "education_founder",
    },
    "LangGraph": {
        "what": "The job-hunting agent now makes its own decisions — it filters, scores, and only surfaces roles that are genuinely aligned. No more noise.",
        "why_business": "This is what 'AI decision-making' looks like in practice: not science fiction, but a bot that saves 3 hours per day of manual filtering.",
        "emotion": "confidence",
        "audience": "hr_professional",
    },
    "AWS Lambda": {
        "what": "Every morning at 8 AM, a voice memo arrives on my phone: what happened in my codebases overnight, what needs attention, what shipped. Built and running on AWS — $2/month.",
        "why_business": "This is the real AI co-founder pitch: not a chatbot, but infrastructure that watches your business while you sleep.",
        "emotion": "amazement",
        "audience": "tech_founder",
    },
    "eval harness": {
        "what": "131 automated tests now run every time any change is made — including one where Claude grades its own output. If the AI disagrees with itself too often, the change is flagged.",
        "why_business": "Quality control on AI systems used to mean 'pray it works in prod'. Now it means measurable, repeatable standards — same discipline as enterprise software.",
        "emotion": "trust",
        "audience": "cto_hiring",
    },
    "dedup": {
        "what": "The daily briefing now fires exactly once — not three times, not zero times. Sounds simple. In distributed systems, exactly-once delivery is actually hard.",
        "why_business": "This is the difference between a demo and a production system. Production means reliability, not just capability.",
        "emotion": "reliability",
        "audience": "tech_founder",
    },
}


def _pick_human_frame(milestone: Dict) -> Dict:
    """Match milestone to a human framing by keyword scan."""
    title = (milestone.get("title", "") + " " + milestone.get("description", "")).lower()
    for keyword, frame in MILESTONE_HUMAN_FRAMES.items():
        if keyword.lower() in title:
            return frame
    # Generic fallback
    return {
        "what": milestone.get("description", "")[:200],
        "why_business": "This is what AI-augmented building looks like in practice: real systems, real results, real accountability.",
        "emotion": "confidence",
        "audience": "general_professional",
    }


def _groq_generate(milestone: Dict, frame: Dict) -> Optional[str]:
    """Generate a 180-220 word Instagram caption via Groq."""
    if not GROQ_API_KEY:
        return None

    prompt = f"""You write Instagram captions for Elena Revicheva — a former Deputy CEO/Chief Legal Officer (7 years running digital government programs) who rebuilt herself as an AI builder. She ships 10 live AI agents on a $0/month Oracle server. She is based in Panama.

CTO AIPA (her AI co-founder) just shipped this milestone:
Title: {milestone.get('title', '')}
In human terms: {frame['what']}
Why it matters for business: {frame['why_business']}

WRITE AN INSTAGRAM CAPTION:
- Length: 180–220 words
- Tone: honest, warm, first-person. "Building in public" energy. NOT corporate.
- Target reader: HR manager or business founder who is curious about AI but slightly afraid of it.
- Open with a hook — a relatable human moment, not a tech announcement.
- Middle: what actually changed (in plain language — no jargon like LangGraph, pgvector, Lambda).
- End: one line about what this means if you're hiring or partnering with someone who builds like this.
- Final line: aideazz.xyz/portfolio
- Emotion to convey: {frame['emotion']}
- 4-6 hashtags at the end: mix of #AI #BuildingInPublic #AppliedAI #AIdeazz #PanamaFounder and one role-specific tag.
- No markdown bold or asterisks — Instagram shows them literally.
- Do NOT use the words: neural network, LangGraph, pgvector, Lambda, vector, embedding, node, pipeline.

Generate the caption now:"""

    payload = json.dumps({
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.75,
        "max_tokens": 500,
    }).encode()

    req = urllib.request.Request(
        GROQ_API_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read())
            return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        logger.warning(f"[CTO-Milestone] Groq generation failed: {e}")
        return None


def _fallback_caption(milestone: Dict, frame: Dict) -> str:
    """Static fallback if Groq is unavailable."""
    return (
        f"Something small shipped this week that I want to share.\n\n"
        f"{frame['what']}\n\n"
        f"{frame['why_business']}\n\n"
        f"I spent 7 years as a Deputy CEO running government digital programs. "
        f"Then I rebuilt myself into an AI builder — one working system at a time. "
        f"This is what that looks like in practice: not pitch decks, real deployed code.\n\n"
        f"If you're looking for someone who understands both boardrooms and codebases:\n"
        f"{PORTFOLIO_URL}\n\n"
        f"#AI #BuildingInPublic #AppliedAI #AIdeazz #PanamaFounder #AIEngineer"
    )


# ── Public API ────────────────────────────────────────────────────────────────

def fetch_and_generate_milestone_story(marketing_engine_image_urls: list) -> Optional[Dict[str, Any]]:
    """
    Main entry point. Called from send_automated_daily_promo() on even days.

    Returns a dict with keys: promo, story, video_url, image_url, campaign_type
    OR None if no pending milestone / any error.

    SAFE: never raises.
    """
    try:
        # 1. Fetch pending milestone
        result = _get("/api/influencer-updates?limit=1")
        if not result or not result.get("ok") or not result.get("pending"):
            logger.info("[CTO-Milestone] No pending milestones for Influencer — using regular content")
            return None

        milestone = result["pending"][0]
        logger.info(f"[CTO-Milestone] Found milestone: {milestone.get('title', '')[:60]}")

        # 2. Pick human frame
        frame = _pick_human_frame(milestone)

        # 3. Generate caption
        caption = _groq_generate(milestone, frame) or _fallback_caption(milestone, frame)

        # 4. Pick image — CTO milestone posts use sprinter.jpg; fall back to marketing engine pool
        MILESTONE_IMAGE = "https://raw.githubusercontent.com/ElenaRevicheva/EspaLuz_Influencer/main/sprinter.jpg"
        import random
        image_url = MILESTONE_IMAGE if MILESTONE_IMAGE else (
            random.choice(marketing_engine_image_urls) if marketing_engine_image_urls else ""
        )

        # 5. Build story dict (same shape as existing generators)
        story = {
            "hook": caption[:100],
            "story": caption,
            "emotion": frame["emotion"],
            "transformation": f"From executive to AI builder — shipping real systems",
            "audience": frame["audience"],
            "emotional_state": frame["emotion"],
            "location": "Panama City, Panama",
            "day_theme": "cto_milestone",
            "milestone_title": milestone.get("title", ""),
            "milestone_repo": milestone.get("repo", ""),
            "received_at": milestone.get("received_at", ""),
        }

        logger.info(f"[CTO-Milestone] Story generated ({len(caption)} chars)")
        return {
            "promo": caption,
            "story": story,
            "video_url": "",         # no video for milestone posts
            "image_url": image_url,
            "campaign_type": "cto_milestone",
            "milestone": milestone,  # keep for mark-posted call
        }

    except Exception as e:
        logger.error(f"[CTO-Milestone] Unexpected error: {e}")
        return None  # SAFE FALLBACK — existing content runs


def mark_milestone_posted(milestone: Dict) -> None:
    """Call after successful post. Non-critical — logs only on failure."""
    try:
        _post("/api/influencer-updates/mark", {
            "repo": milestone.get("repo", ""),
            "received_at": milestone.get("received_at", ""),
        })
        logger.info(f"[CTO-Milestone] Marked as Influencer-posted: {milestone.get('title', '')[:50]}")
    except Exception as e:
        logger.warning(f"[CTO-Milestone] mark failed (non-critical): {e}")
