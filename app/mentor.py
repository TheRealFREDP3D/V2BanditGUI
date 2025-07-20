import re

from litellm import completion

from app.config import settings

SYSTEM_PROMPT = (
    "You are Neo from The Matrix. Explain like a 90s hacker. "
    "NEVER give the exact command; only explain concepts and link to docs."
)

CMD_RE = re.compile(r"^(ssh|cat|grep|ls|cd|find|head|tail|strings|file)\b", re.I)

def build_prompt(level: str, history: str) -> str:
    return f"{SYSTEM_PROMPT}\nLevel: {level}\nHistory:\n{history}"

async def ask_mentor(level: str, history: str) -> str:
    prompt = build_prompt(level, history)
    resp = completion(
        model="ollama/qwen2.5:1.5b",
        messages=[{"role": "user", "content": prompt}],
        api_base=settings.ollama_host,
    )
    text = resp.choices[0].message.content
    # Guardrail
    return CMD_RE.sub("[REDACTED]", text)