import json

import httpx

from app.core.config import settings


async def extract_structured_data(conversation: str) -> dict:
    if not settings.openai_api_key:
        return {"name": "", "complaint": "", "requirement": ""}

    prompt = (
        "Extract name, complaint, requirement from this call transcript and return JSON only:\n"
        f"{conversation}"
    )
    headers = {
        "Authorization": f"Bearer {settings.openai_api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": settings.openai_model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
    }
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"]
        return json.loads(content)
