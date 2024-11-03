from io import BytesIO

from .base import STT


class OpenAIWhisper(STT):
    def __init__(self) -> None:
        from openai import OpenAI
        self._session = OpenAI()

    def recognize(self, audio_files: list[bytes]) -> list[str]:
        results = []
        for audio_file in audio_files:
            response = self._session.audio.transcriptions.create(model="whisper-1", file=BytesIO(audio_file))
            results.append(response.text)
        return results