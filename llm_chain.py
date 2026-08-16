"""
Provider fallback chain for the EspaLuz Influencer bot.

Why (2026-08-16): this bot ran on ONE provider — Groq — with no fallback at all.
Groq retired llama-3.3-70b that day. A single-provider content bot fails
silently: it posts nothing, and nobody is paged, because "no post today" looks
identical to "quiet day".

Order is the BULK profile, chosen for what this bot does. It writes scheduled
social content; nobody is waiting on a response, so cost matters more than
latency and the free providers go first:

    gemini -> groq -> openai -> grok -> claude

Claude last on purpose: it writes the best copy, but this bot generates many
posts a week and reaching Claude means four providers are already down.

Rules carried over from the VJH and cto-aipa chains:
  - An EMPTY reply is a FAILURE, not an answer. Reasoning models spend a small
    max_tokens budget thinking privately and return "". Passing that back would
    post an empty string.
  - Every provider gets at least MIN_TOKENS. Measured floor for
    openai/gpt-oss-120b is ~200 tokens before it emits anything.
  - Model ids are env-overridable, so the next retirement is a config change,
    not a code change.

Verified by eval_llm_chain.py — nothing is listed here that has not written a
real post at the real budget.
"""
import json
import os
import urllib.request
from typing import Iterable, List, Tuple

MIN_TOKENS = 300

PROFILE_BULK: Tuple[str, ...] = ("gemini", "groq", "openai", "grok", "claude")

PROVIDER_KEYS = {
    "gemini": "GEMINI_API_KEY",
    "groq": "GROQ_API_KEY",
    "openai": "OPENAI_API_KEY",
    "grok": "XAI_API_KEY",
    "claude": "ANTHROPIC_API_KEY",
}

_URLS = {
    "groq": "https://api.groq.com/openai/v1/chat/completions",
    "openai": "https://api.openai.com/v1/chat/completions",
    "grok": "https://api.x.ai/v1/chat/completions",
    "claude": "https://api.anthropic.com/v1/messages",
}


def _model(provider: str) -> str:
    if provider == "groq":
        # THE one Groq switch, same env var as the rest of the fleet.
        return os.environ.get("GROQ_MODEL", "").strip() or "openai/gpt-oss-120b"
    return {
        # 2.5-flash writes better prose than flash-lite; this bot only writes prose.
        "gemini": os.environ.get("GEMINI_MODEL", "").strip() or "gemini-2.5-flash",
        "openai": os.environ.get("OPENAI_CHAIN_MODEL", "").strip() or "gpt-4o-mini",
        "grok": os.environ.get("XAI_MODEL", "").strip() or "grok-4.20-0309-non-reasoning",
        "claude": os.environ.get("CLAUDE_CHAIN_MODEL", "").strip() or "claude-haiku-4-5-20251001",
    }[provider]


def _post(url: str, headers: dict, body: dict, timeout: int = 45) -> dict:
    req = urllib.request.Request(
        url, data=json.dumps(body).encode(), method="POST",
        headers={"Content-Type": "application/json", **headers},
    )
    return json.loads(urllib.request.urlopen(req, timeout=timeout).read().decode())


def call_provider(provider: str, system: str | None, prompt: str, max_tokens: int) -> str:
    """One provider, one attempt. Raises on transport/HTTP failure."""
    key = os.environ.get(PROVIDER_KEYS[provider], "").strip()
    if not key:
        raise RuntimeError(f"no {PROVIDER_KEYS[provider]}")
    model = _model(provider)

    if provider == "gemini":
        body: dict = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"maxOutputTokens": max_tokens, "temperature": 0.7},
        }
        if system:
            body["systemInstruction"] = {"parts": [{"text": system}]}
        url = (f"https://generativelanguage.googleapis.com/v1beta/models/{model}"
               f":generateContent?key={key}")
        data = _post(url, {}, body)
        cands = data.get("candidates") or [{}]
        parts = (cands[0].get("content") or {}).get("parts") or [{}]
        return parts[0].get("text") or ""

    if provider == "claude":
        body = {"model": model, "max_tokens": max_tokens,
                "messages": [{"role": "user", "content": prompt}]}
        if system:
            body["system"] = system
        data = _post(_URLS["claude"], {"x-api-key": key, "anthropic-version": "2023-06-01"}, body)
        return "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")

    # groq / openai / grok are OpenAI-compatible
    messages = ([{"role": "system", "content": system}] if system else []) + \
               [{"role": "user", "content": prompt}]
    headers = {"Authorization": "Bearer " + key}
    if provider == "groq":
        # Cloudflare 403s the default urllib User-Agent.
        headers["User-Agent"] = "Mozilla/5.0 (EspaLuz Influencer)"
    data = _post(_URLS[provider], headers,
                 {"model": model, "messages": messages,
                  "max_tokens": max_tokens, "temperature": 0.7})
    return data["choices"][0]["message"]["content"] or ""


def complete(prompt: str, max_tokens: int = 800, system: str | None = None,
             order: Iterable[str] = PROFILE_BULK) -> Tuple[str, List[str]]:
    """Walk the chain until a provider returns real text.

    Returns (text, errors). Empty text means every provider failed, and `errors`
    says why each one did — so a silent content outage becomes a readable log
    line instead of a bot that simply stopped posting.
    """
    budget = max(int(max_tokens), MIN_TOKENS)
    errors: List[str] = []
    for provider in order:
        try:
            text = call_provider(provider, system, prompt, budget)
            if text and text.strip():
                return text, errors
            errors.append(f"{provider}: empty response")
        except Exception as e:  # noqa: BLE001 — any failure must advance the chain
            errors.append(f"{provider}: {str(e)[:120]}")
    return "", errors
