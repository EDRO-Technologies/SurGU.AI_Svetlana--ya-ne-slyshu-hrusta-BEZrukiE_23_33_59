from base64 import b64encode

from .base import OCR


SYSTEM = {
    "role": "system",
    "content": [
        {
            "type": "text",
            "text": 'Ты распознаешь текст с картинок, когда пользователь присылает тебе картинку - ты должен вернуть текст с неё. Пиши текст в точности как на картинке, без сокращений и пропуска слов. Если на ней нету текста, напиши "НЕТУ ТЕКСТА"',
        }
    ],
}


class OpenAIOCR(OCR):
    """
    Класс, который может распознавать любой текст (рукописный и машинный) на всех языках.

    Рекомендуемые модели:
        - `gpt-4o-mini` (дешевле, но чуть хуже качество)
        - `gpt-4o` (дороже, но лучше качество)

    Полный список моделей: https://platform.openai.com/docs/models/model-endpoint-compatibility

    Argumemnts
    ----------
    model : str : "gpt-4o-mini"
        ID модели для распознавания. `gpt-4o-mini` по умолчанию.
    base_url : str | None
        Адрес альтернативного сервера OpenAI API

    Example
    -------
    >>> from TakVamVidno.extractors.images import OpenAIOCR, prepare_images
    >>> ocr = OpenAIOCR()
    >>> result = ocr.extract(prepare_images(["./image.jpg"]))
    >>> print(result[0])
    """

    def __init__(
        self,
        model: str = "gpt-4o-mini",
        base_url: str | None = None,
        *args,
        **kwargs,
    ):
        from openai import OpenAI as _OpenAI
        self._model = model
        self._session = _OpenAI(base_url=base_url, *args, **kwargs)

    def extract(self, images: list[bytes]) -> list[str]:
        results = []
        for image in images:
            messages = [
                SYSTEM,
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Распознай текст с этой картинки"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/webp;base64,{b64encode(image).decode('utf-8')}",
                                "detail": "high",
                            },
                        },
                    ],
                },
            ]
            completion = self._session.chat.completions.create(
                model=self._model,
                messages=messages,
            )
            content = completion.choices[0].message.content
            results.append(None if content == "НЕТУ ТЕКСТА" else content)
        return results
