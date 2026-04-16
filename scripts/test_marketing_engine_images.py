#!/usr/bin/env python3
"""
One-off asset check: sends two short Telegram photos (architecture + workflow PNGs).
Does not run AI, does not touch memory, does not hit Make.com — only verifies uploads.

Daily schedule is unchanged (odd day EspaLuz, even day marketing engine, one post/day).

    ./venv/bin/python scripts/test_marketing_engine_images.py
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
    main.test_marketing_engine_image_assets()
