from openai import OpenAI as _OpenAI

from .base import Provider
from .load_prompt import load_prompt

MAX_RECURSION = 4


class OpenAIProvider(Provider):
    """
    Класс, который подводит анализирует полученный текст.

    Рекомендуемые модели:
        - `gpt-4o-mini` (дешевле, быстрее, но чуть хуже качество)
        - `gpt-4o` (дороже, медленее, но лучше качество)

    Полный список моделей: https://platform.openai.com/docs/models/model-endpoint-compatibility

    Argumemnts
    ----------
    model : str : "gpt-4o-mini"
        ID модели для распознавания. `gpt-4o-mini` по умолчанию.
    base_url : str | None
        Адрес альтернативного сервера OpenAI API
    prompt : str | None
        Системное сообщение. При None загружает внутреннее системное сообщение.
    """

    def __init__(
        self,
        model: str = "gpt-4o-mini",
        base_url: str | None = None,
        prompt: str | None = None,
    ):
        self._session = _OpenAI(base_url=base_url)
        self._model = model
        self._prompt = prompt or load_prompt()

    def generate_report(self, text: str, messages: list[dict] = None):
        if messages is None:
            messages = [{"role": "system", "content": self._prompt}]
        return self._generate(text, messages)

    def _generate(
        self, text: str, messages: list[dict], recursion: int = None
    ) -> tuple[list[dict], str]:
        if recursion is None:
            recursion = 0
            messages.append({"role": "user", "content": text})
        response = self._session.chat.completions.create(
            model=self._model,
            messages=messages,
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "mind_map",
                        "description": "Рисует интеллект-карту",
                        "strict": False,
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "main_topic": {
                                    "type": "string",
                                    "description": "Основная тема текста",
                                },
                                "subtopics": {
                                    "type": "string",
                                    "description": """Подтемы текста и детали подтемы в JSON формате: {"подтема1": ["деталь1.1", "деталь1.2"], "подтема2": ["деталь2.1"]}""",
                                },
                            },
                            "additionalProperties": False,
                            "required": [],
                        },
                    },
                }
            ],
            tool_choice="auto",
        )
        choice = response.choices[0]
        if choice.finish_reason == "stop":
            messages.append({"role": "assistant", "content": choice.message.content})
            print(messages, choice.message.content)
            return messages, choice.message.content
        elif choice.finish_reason == "tool_calls":
            print(choice)
        else:
            raise ValueError(
                f"Неизвестная причина завершения генерации: {choice.finish_reason}"
            )
