"""EspaLuz nightly post = TRUE content only (21 Nov 2026).

Elena: "EspaLuz posts should be the freshest, valuable, contain only truth - no AI theater, no AI-generated simulated
facts". The old EspaLuz night asked a model for a story ("You're at the feria in Santiago... your child points...") -
an invented scene every third night. This module builds the EspaLuz story WITHOUT a model, from two verified sources:

  1. FEATURE_CARDS - what the product really does today (each line checked against the bots' menus / live tests).
  2. The bots' own country data (espaluz_country_contexts_full.py: 21 countries, local expressions, cultural notes) -
     a real local word with its meaning and one real "good to know".

Nights alternate: local-word card, feature card. Only the EspaLuz lane uses this; the AI Marketing Engine lane is untouched.
Links are tracked with the Influencer's own code (utm_campaign = INFLUENCER_CODE) so visits and web sign-ups show up in
the daily film report and in HubSpot ([ESPALUZ] WEB deals via first_touch).
"""
import importlib.util
import os
import random
from datetime import datetime

INFLUENCER_CODE = "f20261121e5a1"   # EspaLuz nightly channel posts (the code format the bots and report already read)
TRUE_URL = f"https://app.espaluz.lat/?utm_source=influencer&utm_medium=channel&utm_campaign={INFLUENCER_CODE}"
TRUE_VIDEO = "https://youtube.com/shorts/vsshZlJL6YQ"   # film 02 (EN), live since 21 Nov 2026
TRUE_HASHTAGS = ["#EspaLuz", "#ExpatFamily", "#LifeInLatinAmerica", "#BilingualFamily", "#NewCountry"]
SLOGAN = "Paperwork gets solved once. Adaptation is what lasts. / Los trámites pasan. La adaptación queda."

# Each card: hook + what is TRUE today. No numbers that are not in the product, no users, no results.
FEATURE_CARDS = [
    {"hook": "📸 A letter from school you can't read?",
     "story": "Send EspaLuz a photo of it on WhatsApp or Telegram. She explains it in English and Spanish and helps you write the answer. "
              "Mándale una foto a EspaLuz: te la explica en inglés y español y te ayuda a responder."},
    {"hook": "🗣️ At the doctor, the bank or a public office",
     "story": "Voice translation mode: you speak, EspaLuz says it in Spanish, and brings the answer back to you "
              "(Telegram: /convo on · WhatsApp: translate mode). Tú hablas, ella lo dice en español y te trae la respuesta."},
    {"hook": "🦥🐒 Ten minutes a day for your child (ages 5-8)",
     "story": "Pere and Titi talk with your child in their own voices: tracing letters and numbers, songs, small games. "
              "After the lesson you get a short report of what was practised. Después de la clase recibes un resumen."},
    {"hook": "🧠 One family memory, three doors",
     "story": "Start on the web, WhatsApp or Telegram - EspaLuz remembers your family the same way on all three. "
              "La misma memoria de tu familia en la web, WhatsApp y Telegram."},
    {"hook": "💼 English for your work, not for a test",
     "story": "Pro English: a quick level check, then real work scenes - a call with a client, a price, a job interview, an email - "
              "and a pronunciation score on your voice notes. Inglés para tu trabajo, con escenas reales."},
    {"hook": "🧭 Already speak Spanish?",
     "story": "Settle mode: the local ways nobody explains, plus English when you need it. "
              "Modo settle: las costumbres locales que nadie explica, y el inglés cuando lo necesitas."},
    {"hook": "🌎 21 Spanish-speaking countries, each its own way",
     "story": "Tell EspaLuz your country and she uses its own words, customs and everyday situations - Panama is not Mexico, "
              "and Mexico is not Spain. Cada país, a su manera."},
    {"hook": "📱 On Android? Free beta until 31 December",
     "story": "Write ANDROID to EspaLuz on WhatsApp: she sends you the 3 steps, and your family uses the app free until 31 December. "
              "Escribe ANDROID por WhatsApp: gratis hasta el 31 de diciembre."},
]


def _country_data():
    """The bots' own curated data (same file the bots answer from). None if not found - feature cards still work."""
    here = os.path.dirname(os.path.abspath(__file__))
    for path in (os.getenv("ESPALUZ_COUNTRY_CONTEXTS", ""),
                 os.path.join(here, "..", "EspaLuzWhatsApp", "espaluz_country_contexts_full.py"),
                 os.path.join(here, "..", "EspaLuzFamilybot", "espaluz_country_contexts_full.py")):
        if path and os.path.isfile(path):
            try:
                spec = importlib.util.spec_from_file_location("espaluz_cc", path)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                return mod.COUNTRY_CONTEXTS
            except Exception as e:  # noqa: BLE001
                print(f"⚠️ country data unreadable: {e}")
    return None


# Only practical, everyday notes go public. Excluded on purpose: opinions ("progressive", "class_conscious"), legal or
# money claims that go stale (bitcoin, tax_benefits, dollarized), safety advice, and "most affordable"-type rankings.
PRACTICAL_NOTES = {"formality", "time", "tips", "food_times", "coffee", "mate", "dinner", "kiss", "siesta", "punctuality",
                   "altitude", "weather", "spanglish", "tereré", "hurricanes", "regions", "chilean_spanish", "resolver",
                   "music", "food", "pupusas", "arepas"}


def _local_word_card(rng):
    data = _country_data()
    if not data:
        return None
    options = []
    for c in data.values():
        words = (c.get("local_vocabulary") or {}).get("expressions") or {}
        notes = {k: v for k, v in (c.get("cultural_notes") or {}).items() if isinstance(v, str) and k in PRACTICAL_NOTES}
        for w, meaning in words.items():
            options.append((c, w, meaning, notes))
    if not options:
        return None
    c, word, meaning, notes = rng.choice(options)
    note = ""
    if notes:
        k = rng.choice(sorted(notes))
        note = f"\nGood to know in {c.get('name')}: {notes[k]}"
    return {"hook": f"{c.get('flag', '🌎')} In {c.get('name')}, \"{word}\" means: {meaning}",
            "story": "One of the local words EspaLuz knows - the words people really say, in 21 Spanish-speaking countries." + note,
            "location": c.get("name")}


def build_story(now=None, seed=None):
    """A story dict in the shape the Influencer already uses (hook/story/transformation/emotion/theme/audience/location)."""
    now = now or datetime.now()
    rng = random.Random(seed if seed is not None else now.strftime("%Y-%m-%d"))
    card = _local_word_card(rng) if now.toordinal() % 2 == 0 else None
    kind = "local_word" if card else "feature"
    if not card:
        card = dict(rng.choice(FEATURE_CARDS))
    return {
        "hook": card["hook"],
        "story": card["story"],
        "transformation": SLOGAN,
        "emotion": "🌎 True today, on the web, WhatsApp and Telegram",
        "theme": f"true_{kind}",
        "audience": "settling_family",
        "emotional_state": "clarity",
        "location": card.get("location", "Latin America"),
    }
