import random, itertools
from typing import List
from flask import current_app

def _iter_keys(provider: str) -> List[str]:
    # randomise starting point so we spread usage across keys
    keys = current_app.config["PROVIDER_KEYS"].get(provider, [])
    n    = len(keys)
    start = random.randrange(n) if n else 0
    return itertools.chain(keys[start:], keys[:start])

###########
# OpenAI  #
###########
def openai_chat(model: str, prompt: str) -> str:
    import openai
    ex = None
    for key in _iter_keys("openai"):
        try:
            client = openai.OpenAI(api_key=key)
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
            )
            return resp.choices[0].message.content
        except Exception as e:
            ex = e
            continue
    raise RuntimeError(f"All OpenAI keys failed: {ex}")

###########
# Anthropic
###########
def anthropic_chat(model: str, prompt: str) -> str:
    import anthropic
    ex = None
    for key in _iter_keys("anthropic"):
        try:
            client = anthropic.Anthropic(api_key=key)
            resp = client.messages.create(
                model=model,
                max_tokens=512,
                messages=[{"role": "user", "content": prompt}],
            )
            return resp.content[0].text
        except Exception as e:
            ex = e
    raise RuntimeError(f"All Anthropic keys failed: {ex}")

###########
# Google (Gemini)
###########
def google_chat(model: str, prompt: str) -> str:
    import google.generativeai as genai
    ex = None
    for key in _iter_keys("google"):
        try:
            genai.configure(api_key=key)
            mdl = genai.GenerativeModel(model)
            resp = mdl.generate_content(prompt)
            return resp.text
        except Exception as e:
            ex = e
    raise RuntimeError(f"All Google keys failed: {ex}")

PROVIDER_FUNCS = {
    "openai":    openai_chat,
    "anthropic": anthropic_chat,
    "google":    google_chat,
}
