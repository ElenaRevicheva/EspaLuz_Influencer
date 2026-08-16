#!/usr/bin/env python3
"""
Provider chain eval for the EspaLuz Influencer bot.

Same intent as VibeJobHunter's evals/test_provider_chain.py, adapted to this
repo (no pytest here, so it runs standalone):

    python3 eval_llm_chain.py

Three questions, in increasing order of usefulness:

  1. Can each provider answer at all, at the budget this bot really sends?
  2. Is the answer USABLE BY THIS BOT? "Non-empty" is not the bar. This bot
     posts to Instagram, and its own prompt says:
         "No markdown bold or asterisks — Instagram shows them literally."
     A provider that returns "**Hola**" or "# English" would publish those
     characters verbatim. That provider does not fit, however good the prose is.
  3. Does the CHAIN survive losing providers? That is the whole point of having
     one, and it is the test that actually reproduces a bad day.

Why it exists (2026-08-16): this bot ran on ONE provider. Groq retired
llama-3.3-70b that day. A single-provider content bot fails silently — no post,
no alert, because "no post today" looks exactly like "quiet day".

Exit 1 if the chain cannot produce usable text. Providers without a key are
skipped. A provider that answers but fails the FITNESS checks is reported
loudly and does not fail the run on its own — the chain may still be fine — but
it tells you which provider you would not want first in the order.
"""
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from llm_chain import PROFILE_BULK, PROVIDER_KEYS, call_provider, complete  # noqa: E402

PROMPT = (
    "Write ONE short bilingual social post (English then Spanish) inviting expat "
    "families in Panama to try an AI Spanish tutor. Warm, max 2 sentences. "
    "Plain text only — no markdown, no asterisks, no headings."
)
BUDGET = 500

# Instagram renders these literally, so they are disqualifying, not cosmetic.
MARKDOWN = re.compile(r"\*\*|^#{1,6}\s|\n#{1,6}\s|__")


def fitness(text: str) -> list:
    """Return the reasons this output would NOT be publishable. Empty == fits."""
    problems = []
    t = text.strip()
    if len(t) < 40:
        problems.append(f"too short ({len(t)} chars)")
    if MARKDOWN.search(t):
        problems.append("contains markdown (Instagram shows ** and # literally)")
    # The post is meant to be bilingual; a Spanish-free reply missed the brief.
    if not re.search(r"[áéíóúñ¿¡]", t, re.I) and " la " not in t.lower() and " para " not in t.lower():
        problems.append("no Spanish detected")
    return problems


def main() -> int:
    print(f"=== 1. can each provider answer? (this bot's real job, {BUDGET} tokens) ===")
    answered, unfit = {}, {}
    for provider in PROFILE_BULK:
        if not os.environ.get(PROVIDER_KEYS[provider], "").strip():
            print(f"  {provider:<8} SKIP   no {PROVIDER_KEYS[provider]}")
            continue
        try:
            t0 = time.time()
            text = (call_provider(provider, None, PROMPT, BUDGET) or "").strip()
            ms = int((time.time() - t0) * 1000)
            if not text:
                print(f"  {provider:<8} FAIL   EMPTY at {BUDGET} tokens")
                continue
            answered[provider] = text
            print(f"  {provider:<8} ok  {ms:>5}ms  {text[:44]!r}")
        except Exception as e:  # noqa: BLE001
            print(f"  {provider:<8} FAIL   {str(e)[:80]}")

    print("\n=== 2. is the answer PUBLISHABLE? (Instagram renders markdown literally) ===")
    for provider, text in answered.items():
        problems = fitness(text)
        if problems:
            unfit[provider] = problems
            print(f"  {provider:<8} UNFIT  {'; '.join(problems)}")
        else:
            print(f"  {provider:<8} fits")

    print("\n=== 3. does the chain survive losing providers? ===")
    saved = {}
    for p in list(PROFILE_BULK)[:2]:
        k = PROVIDER_KEYS[p]
        saved[k] = os.environ.get(k)
        os.environ[k] = "broken-on-purpose"
    try:
        text, errors = complete(PROMPT, max_tokens=BUDGET, order=PROFILE_BULK)
        ok = bool(text.strip())
        print(f"  broke {', '.join(list(PROFILE_BULK)[:2])} → "
              f"{'still produced a post ✅' if ok else 'chain DIED ❌'}")
        if errors:
            print(f"  skipped: {'; '.join(errors)[:120]}")
    finally:
        for k, v in saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v

    print("\n=== verdict ===")
    if not text.strip():
        print("❌ chain produced nothing with two providers down — do not deploy")
        return 1
    if unfit:
        print(f"⚠️  {len(unfit)} provider(s) answer but are UNFIT for Instagram: {', '.join(unfit)}")
        print("   Keep them LATE in PROFILE_BULK, or strip markdown before posting.")
    print("✅ chain produces publishable text and survives losing providers")
    return 0


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    raise SystemExit(main())
