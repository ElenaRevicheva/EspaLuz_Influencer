#!/usr/bin/env python3
"""One-off: seed last_milestone_influencer_post so even days use marketing-engine images."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.join(ROOT, "content_memory.json")
with open(path, encoding="utf-8") as f:
    data = json.load(f)
data.setdefault("last_milestone_influencer_post", "2026-06-26T23:00:46-05:00")
with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
print(
    "rotation_idx", data.get("marketing_image_rotation_index"),
    "last_milestone", data.get("last_milestone_influencer_post"),
)
