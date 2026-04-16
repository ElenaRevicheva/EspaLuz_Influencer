#!/usr/bin/env python3
"""
Fire two AI Marketing Engine posts: one photo+caption per marketing_engine_*.png
(uses ``marketing_engine_image_urls`` order in main.py).

Run from repo root with ``TELEGRAM_BOT_TOKEN`` (and ``GROQ_API_KEY``) in ``.env``:

    ./venv/bin/python scripts/fire_two_marketing_posts.py
"""

from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, ROOT)

from dotenv import load_dotenv  # noqa: E402

load_dotenv()

import main  # noqa: E402


if __name__ == "__main__":
    main.fire_two_marketing_image_posts()
    print("Done: two posts (Telegram + Make webhook each).")
