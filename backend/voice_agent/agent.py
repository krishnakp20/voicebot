import asyncio
from dataclasses import dataclass

import httpx

from app.core.config import settings
from app.services.sarvam_service import speech_to_text, text_to_speech


@dataclass
class AgentContext:
    call_id: str
    client_id: int
    agent_id: int
    prompt: str
    voice: str
    customer_name: str


class DynamicVoiceAgent:
    def __init__(self, context: AgentContext) -> None:
        self.context = context
        self.transcript_parts: list[str] = []

    async def on_user_speech(self, text: str) -> str:
        self.transcript_parts.append(f"USER: {text}")
        reply = await self.generate_response(text)
        self.transcript_parts.append(f"AI: {reply}")
        return reply

    async def on_audio_frame(self, audio_bytes: bytes, language: str = "en") -> bytes:
        """
        STT -> LLM -> TTS hook for LiveKit media handlers.
        """
        user_text = await speech_to_text(audio_bytes, language=language)
        reply = await self.on_user_speech(user_text)
        return await text_to_speech(reply, speaker=self.context.voice, language=language)

    async def generate_response(self, user_text: str) -> str:
        if not settings.openai_api_key:
            return "Thank you, we have logged your request."
        payload = {
            "model": settings.openai_model,
            "messages": [
                {"role": "system", "content": self.context.prompt},
                {"role": "user", "content": user_text},
            ],
        }
        headers = {"Authorization": f"Bearer {settings.openai_api_key}"}
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]

    async def finalize(self, duration: int, status: str, recording_url: str) -> None:
        transcript = "\n".join(self.transcript_parts)
        async with httpx.AsyncClient(timeout=30) as client:
            await client.post(
                f"{settings.backend_api_url}/calls/events/finalize/{self.context.call_id}",
                json={
                    "duration": duration,
                    "status": status,
                    "transcript": transcript,
                    "recording_url": recording_url,
                },
            )


async def run_livekit_session(metadata: dict) -> None:
    """
    Entry point used by your LiveKit worker.
    Metadata is expected to include prompt, voice, client_id, and call details.
    """
    context = AgentContext(
        call_id=metadata["call_id"],
        client_id=metadata["client_id"],
        agent_id=metadata["agent_id"],
        prompt=metadata["prompt"],
        voice=metadata["voice"],
        customer_name=metadata["customer_name"],
    )
    agent = DynamicVoiceAgent(context)
    await agent.on_user_speech(f"Hello, I am {context.customer_name}")
    await asyncio.sleep(1)
    await agent.finalize(duration=60, status="completed", recording_url="")
