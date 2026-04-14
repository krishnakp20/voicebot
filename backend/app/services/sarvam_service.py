import httpx

from app.core.config import settings


async def text_to_speech(text: str, speaker: str, language: str = "en") -> bytes:
    if not settings.sarvam_api_key:
        return b""
    headers = {"Authorization": f"Bearer {settings.sarvam_api_key}"}
    payload = {"text": text, "speaker": speaker, "language_code": language}
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(f"{settings.sarvam_base_url}/text-to-speech", json=payload, headers=headers)
        resp.raise_for_status()
        return resp.content


async def speech_to_text(audio_bytes: bytes, language: str = "en") -> str:
    if not settings.sarvam_api_key:
        return ""
    headers = {"Authorization": f"Bearer {settings.sarvam_api_key}"}
    files = {"audio": ("input.wav", audio_bytes, "audio/wav")}
    data = {"language_code": language}
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(f"{settings.sarvam_base_url}/speech-to-text", headers=headers, files=files, data=data)
        resp.raise_for_status()
        return resp.json().get("text", "")
