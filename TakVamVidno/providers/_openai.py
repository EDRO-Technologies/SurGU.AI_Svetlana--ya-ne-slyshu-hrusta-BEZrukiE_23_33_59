from openai import OpenAI as _OpenAI

from .base import Provider


class OpenAIProvider(Provider):
    def __init__(self, model: str = "gpt-4o-mini", base_url: str | None = None):
        self._session = _OpenAI()
        self._model = model

    def generate(self):
        self._session.chat.completions.create(
            model=self._model,
            messages=[],
        )
