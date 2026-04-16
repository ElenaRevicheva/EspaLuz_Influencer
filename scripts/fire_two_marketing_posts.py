#!/usr/bin/env python3
"""
Run **two full AI Marketing Engine posts** (one per marketing_engine_*.png): Groq copy, memory,
Telegram photo+caption, **Make.com webhook** each — so your scenario can push to Instagram, LinkedIn, etc.

Does **not** change the systemd schedule: odd day = EspaLuz, even day = marketing engine (one post/day).

Stop the bot first if you run this on the same host (avoid two Telegram polling processes), or run from a
one-off shell with the same .env:

    cd /home/ubuntu/EspaLuz_Influencer
    ./venv/bin/python scripts/fire_two_marketing_posts.py

If main.py is already running as a service, prefer:

    sudo systemctl stop espaluz-influencer
    ./venv/bin/python scripts/fire_two_marketing_posts.py
    sudo systemctl start espaluz-influencer
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
