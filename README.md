# EspaLuz AI Influencer Co-Founder v3.1

AI-powered social media content for **EspaLuz** (language tutoring) **and** additive promotion of the **AI Marketing Engine** (AIdeazz stack, roadmap, Oracle deployment).

## What’s new in v3.1 (dual campaign)

- **Alternation by calendar day (Panama):** **odd** day (1, 3, 5…) → classic **EspaLuz** tutoring narrative (v3.0 co-founder). **Even** day (2, 4, 6…) → **AI Marketing Engine** narrative (AIdeazz, agents, SEO/resilience, case-study framing).
- **Same pipeline:** Telegram → channel → **Make.com** webhook (extra JSON keys: `campaign_type`, `content_type`).
- **New assets:** `marketing_engine_architecture.png`, `marketing_engine_workflow.png` (referenced in promos on engine days).
- **Commands:** `/campaign_today` shows which campaign runs today; `/daily_promo` follows the same rule as the scheduled post.

Prior behavior (v3.0 memory, calendar, rotation, Groq, Make compatibility) is unchanged for EspaLuz days.

## Architecture

```
[Schedule 6PM Panama] → [Campaign router: odd=EspaLuz / even=Engine]
        → [Groq story + memory] → [Telegram @EspaLuz] → [Make.com webhook] → [Social platforms]
```

## Environment variables

```bash
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
GROQ_API_KEY=your_groq_api_key   # Required for AI generation (both campaigns)
```

## Commands (high level)

- `/daily_promo` — Generate and post **today’s** campaign (respects odd/even rule).
- `/campaign_today` — Show whether today is EspaLuz or Marketing Engine.
- `/test_ai` — Test EspaLuz story generation (no campaign router).
- `/test_time` — Server vs Panama time + next schedule + today’s campaign.
- `/help` — Full menu.

## Scheduling

Daily auto-post at **6:00 PM Panama** (23:00 UTC), same as v3.0.

## Backup

- **Branch:** `backup/pre-ai-cofounder-upgrade-20260108_180511`
- **Tag:** `v1.0-template-based`

To restore: `git checkout v1.0-template-based`

## Author

Elena Revicheva & CTO AIPA
