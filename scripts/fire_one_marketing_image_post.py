#!/usr/bin/env python3
"""
One-shot AI Marketing Engine post with a new me_* promo card.
Uses image_url_override so the daily rotation index is NOT advanced.
Does not change odd/even schedule — tonight's 6 PM cron still runs as usual.
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, ROOT)

from dotenv import load_dotenv

load_dotenv()

import random
import requests
from datetime import datetime

import main  # noqa: E402

# First new agent card — override only; scheduled even-day rotation stays at current index.
ME_IMAGE = (
    "https://raw.githubusercontent.com/ElenaRevicheva/EspaLuz_Influencer/main/"
    "marketing_engine_images/me_01.jpg"
)


def fire_one_marketing_image_post() -> None:
    print("🔥 One-shot marketing-engine post (me_* image, rotation index unchanged)...")
    promo, story, video_url, image_url = main.generate_marketing_engine_content(
        image_url_override=ME_IMAGE
    )
    asset = image_url.rsplit("/", 1)[-1]
    main.send_channel_promo_with_image(promo, image_url)
    print(f"✅ Telegram photo+caption sent ({asset}).")

    payload = {
        "text": promo,
        "videoURL": video_url,
        "imageURL": image_url,
        "videoTitle": f"AI Marketing Engine: {story['emotion']}",
        "videoDescription": story["story"][:200] + "...",
        "automated": False,
        "manual_marketing_image_post": True,
        "timestamp": datetime.now(main.PANAMA_TZ).isoformat(),
        "hook": story["hook"],
        "story": story["story"],
        "emotion": story["emotion"],
        "transformation": story["transformation"],
        "cta": random.choice(main.cta_options),
        "hashtags": " ".join(random.choice(main.hashtag_sets)),
        "socialProof": random.choice(main.social_proof),
        "audience": story.get("audience", "startup_founder"),
        "emotional_state": story.get("emotional_state", "general"),
        "location": story.get("location", "unknown"),
        "day_theme": story.get("day_theme", "general"),
        "content_type": "marketing_engine_v3",
        "campaign_type": "marketing_engine",
        "ai_powered": True,
        "has_memory": True,
        "strategic_calendar": True,
    }
    resp = requests.post(main.MAKE_WEBHOOK_URL, json=payload, timeout=30)
    print(f"📤 Make.com webhook (marketing_engine, {asset}). Response: {resp.status_code}")
    idx = main.memory.memory.get("marketing_image_rotation_index")
    print(f"🖼️ Rotation index unchanged: {idx} (next even-day post picks from there)")


if __name__ == "__main__":
    fire_one_marketing_image_post()
    print("✅ Done — normal 6 PM schedule untouched.")
