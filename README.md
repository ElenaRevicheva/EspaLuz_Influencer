# EspaLuz AI Influencer Co-Founder v2.0

AI-powered social media content generation for EspaLuz language tutoring service.

## What's New in v2.0

**Upgraded from template-based to AI-generated content!**

- **AI Story Generation**: Uses Groq (Llama 3.3 70B) to create fresh, unique stories daily
- **Brand Knowledge Integration**: AI understands EspaLuz's voice, audiences, and emotional arcs
- **Fallback System**: Graceful degradation to templates if AI is unavailable
- **Make.com Compatibility**: Webhook interface preserved - no changes needed to Make.com scenario

## Architecture

```
[Schedule] → [AI Story Generation] → [Telegram Post] → [Make.com Webhook] → [Social Platforms]
                    ↓
             [Groq API / Fallback Templates]
```

## Environment Variables

```bash
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
GROQ_API_KEY=your_groq_api_key  # Required for AI generation
```

## Commands

- `/daily_promo` - Generate and post AI-powered promotional content
- `/test_ai` - Test AI story generation
- `/test_time` - Check server and Panama time
- `/test_emotional_ai` - Test full pipeline with webhook

## Scheduling

Daily promo posts at **4:55 PM Panama time (21:55 UTC)**.

## Backup

- **Branch**: `backup/pre-ai-cofounder-upgrade-20260108_180511`
- **Tag**: `v1.0-template-based`

To restore: `git checkout v1.0-template-based`

## Author

Elena Revicheva & CTO AIPA
