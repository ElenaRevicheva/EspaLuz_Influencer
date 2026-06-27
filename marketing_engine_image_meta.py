"""
Per-asset focus hints for AI Marketing Engine even-day posts.
Paired with the image shown in Telegram / Make.com → Instagram.

Legacy PNGs (architecture/workflow) keep their original framing.
me_01..me_32 promo cards each spotlight one live agent or engine layer.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

# First four URLs in main.marketing_engine_image_urls (order must match)
LEGACY_PNG_FOCUS: Dict[str, Dict[str, str]] = {
    "marketing_engine_architecture.png": {
        "label": "Engine architecture",
        "focus": "Multi-agent orchestration — how CTO AIPA, CMO, and domain bots share one roadmap on Oracle.",
    },
    "marketing_engine_workflow.png": {
        "label": "Engine workflow",
        "focus": "Daily loop: capture signal → generate proof → publish → measure — not one-off hype posts.",
    },
    "marketing_engine_architecture_1.png": {
        "label": "Engine architecture (alt)",
        "focus": "Resilience layer: health checks, failover chains, and docs that keep nine agents alive on $0 infra.",
    },
    "marketing_engine_workflow_1.png": {
        "label": "Engine workflow (alt)",
        "focus": "GEO + SEO as parallel discovery rails — crawlers and LLM answer engines both fed with truth.",
    },
}

# me_01..me_32 — one card per row; copy should name the agent/layer in the hook or first sentence.
ME_CARD_FOCUS: list[Dict[str, str]] = [
    {"label": "CTO AIPA", "focus": "AI Technical Co-Founder — code review, GitHub webhooks, and fleet-wide deploy discipline."},
    {"label": "CMO AIPA + VibeJob Hunter", "focus": "LangGraph job pipeline, eval harness, and marketing automation on the same Oracle VM."},
    {"label": "EspaLuz WhatsApp", "focus": "Revenue-grade language tutor — voice, photos, emotional AI; dogfood proof for the engine."},
    {"label": "EspaLuz Telegram", "focus": "Family bot with pgvector memory — bilingual tutoring that remembers context."},
    {"label": "EspaLuz Influencer", "focus": "Dual campaign bot: EspaLuz learner days + AI Marketing Engine even days → Make.com → social."},
    {"label": "Algom Alpha", "focus": "X stream prospecting — keyword hiring signals routed toward HubSpot CRM."},
    {"label": "Atuona Creative Co-Founder", "focus": "Flux + multi-provider video — creative pipeline with honest provider labeling."},
    {"label": "OpenClaw VibeJobs", "focus": "Shortlist bot — curated jobs surface without noise."},
    {"label": "Sprint Briefing (Sprinter)", "focus": "AWS Lambda morning voice memo — what shipped overnight across repos."},
    {"label": "AILA (design)", "focus": "Orchestration layer roadmap — unified agent bus for the ten-agent ecosystem."},
    {"label": "GEO + SEO Engine", "focus": "geo-manifest, JSON-LD, sitemap — machine-verifiable discoverability on aideazz.xyz."},
    {"label": "HubSpot CRM wiring", "focus": "Every agent posts structured signals — trials, prospects, milestones — one pipeline."},
    {"label": "Outbound / outreach", "focus": "Resend + Hunter caps — hire-us and hire-me lanes with honest outreach_log."},
    {"label": "Lead triage", "focus": "AI classification → respond to high-signal founders first."},
    {"label": "Oracle resilience", "focus": "systemd + PM2 health cron — nine agents on Always Free, restart on hang."},
    {"label": "Atlas Shifted", "focus": "Marketing-angle radar — Bright Data ads, angle classifier, daily memory board."},
    {"label": "Bright Data enrichment", "focus": "Live web unlock for prospect research — rate-limited, logged."},
    {"label": "Blog / dev.to publisher", "focus": "Compound SEO — long-form posts mirrored and cached on Oracle."},
    {"label": "X webhook handler", "focus": "Follow/DM/mention events → Telegram + auto-follow — social loop closed."},
    {"label": "Podcast / voice pipeline", "focus": "Russian voice notes → polished English content — Speechmatics + Groq."},
    {"label": "AI Film Studio", "focus": "Seedance / Runway / Luma reels — portfolio proof for creative buyers."},
    {"label": "Portfolio + pitch", "focus": "Investor-grade static proof — every agent card links to live demos."},
    {"label": "Make.com distribution", "focus": "One webhook fans out to Instagram, LinkedIn, and syndication scenarios."},
    {"label": "Multi-model failover", "focus": "Claude → Groq → OpenAI → Grok chains — no silent dead provider."},
    {"label": "pgvector RAG memory", "focus": "Two-layer memory on EspaLuz bots — retrieval that feels like a real tutor."},
    {"label": "LangGraph eval harness", "focus": "131 tests + Claude self-grade — production discipline, not demo code."},
    {"label": "Hiring pipeline CRM", "focus": "Job applications push hiring deals — VJH and CTO share one HubSpot spine."},
    {"label": "Inquiry forms + UTM", "focus": "Site leads attributed — know which channel sent the founder."},
    {"label": "Buffer / social queue", "focus": "Graceful skip when queue full — no duplicate spam across agents."},
    {"label": "Resilience runbooks", "focus": "ORACLE_ALL_PRODUCTS_RESILIENCE — ops truth docs, not slide filler."},
    {"label": "AI Marketing Engine (meta)", "focus": "The system that markets itself — agents, GEO, outreach, and proof in one loop."},
    {"label": "Build in public", "focus": "Elena Revicheva — Deputy CEO → solo builder; Panama, bilingual, shipping daily."},
]


def _basename(url: str) -> str:
    return url.rsplit("/", 1)[-1]


def focus_for_image_url(url: str) -> Optional[Dict[str, Any]]:
    """Return {label, focus, asset} for Groq prompt injection, or None."""
    if not url:
        return None
    base = _basename(url)
    if base in LEGACY_PNG_FOCUS:
        row = LEGACY_PNG_FOCUS[base]
        return {"asset": base, **row}
    if base.startswith("me_") and base.endswith(".jpg"):
        try:
            idx = int(base[3:5]) - 1
            if 0 <= idx < len(ME_CARD_FOCUS):
                return {"asset": base, **ME_CARD_FOCUS[idx]}
        except ValueError:
            pass
    return None
