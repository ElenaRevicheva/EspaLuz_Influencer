#!/usr/bin/env python3
"""Fire exactly one send_automated_daily_promo() — same path as 6 PM cron."""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, ROOT)

from dotenv import load_dotenv

load_dotenv()

import main  # noqa: E402

if __name__ == "__main__":
    print("🔥 One-shot automated promo (same as daily schedule)...")
    main.send_automated_daily_promo()
    print("✅ Done.")
