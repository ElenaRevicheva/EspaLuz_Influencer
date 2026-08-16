#!/usr/bin/env python3
"""
Provider chain eval for the EspaLuz Influencer bot.

Same idea as VibeJobHunter's evals/test_provider_chain.py and cto-aipa's
scripts/eval-llm-chain.cjs, adapted to this repo (no pytest here, so it runs
standalone):

    python3 eval_llm_chain.py

What it checks:
  1. Every configured provider can write this bot's real output — a short
     bilingual social post — at the budget this bot really sends (500-1800).
  2. The bulk chain returns real text end to end.

Why it exists (2026-08-16): this bot had ONE provider. Groq retired
llama-3.3-70b and its free-tier replacements are reasoning models that can
return "" on small budgets. One provider with no fallback means a Groq outage
is a silent content outage — the bot posts nothing and nobody is paged.

Exit 1 if the chain cannot produce text. Providers without a key are skipped.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from llm_chain import PROFILE_BULK, PROVIDER_KEYS, call_provider, complete  # noqa: E402

PROMPT = (
    "Write ONE short bilingual social post (English then Spanish) inviting expat "
    "families in Panama to try an AI Spanish tutor. Warm, no hashtags, max 2 sentences."
)
BUDGET = 500


def main() -> int:
    print("=== each provider, this bot's real job (500 tokens) ===")
    for provider in PROFILE_BULK:
        key = os.environ.get(PROVIDER_KEYS[provider], "").strip()
        if not key:
            print(f"  {provider:<8} SKIP   no {PROVIDER_KEYS[provider]}")
            continue
        try:
            import time

            t0 = time.time()
            text = (call_provider(provider, None, PROMPT, BUDGET) or "").strip()
            ms = int((time.time() - t0) * 1000)
            if not text:
                print(f"  {provider:<8} FAIL   EMPTY at {BUDGET} tokens")
            else:
                print(f"  {provider:<8} ok  {ms:>5}ms  {text[:46]!r}")
        except Exception as e:  # noqa: BLE001
            print(f"  {provider:<8} FAIL   {str(e)[:80]}")

    print("\n=== the bulk chain (what the bot actually calls) ===")
    text, errors = complete(PROMPT, max_tokens=BUDGET, order=PROFILE_BULK)
    if text.strip():
        print(f"  bulk chain ok -> {text.strip()[:70]!r}")
        if errors:
            print(f"  (skipped {len(errors)} provider(s): {'; '.join(errors)[:110]})")
        print("\n✅ chain produced real text")
        return 0
    print(f"  bulk chain FAILED: {'; '.join(errors)[:200]}")
    print("\n❌ chain produced nothing — do not deploy")
    return 1


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    raise SystemExit(main())
