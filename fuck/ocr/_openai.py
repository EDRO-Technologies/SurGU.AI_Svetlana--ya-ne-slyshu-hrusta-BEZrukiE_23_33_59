from base64 import b64encode

from openai import OpenAI as _OpenAI

from .base import OCR


class OpenAIOCR(OCR):
    def __init__(self):
        self._session = _OpenAI()

    def process(self, images: list[bytes]):
        messages = [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": 'Ты распознаешь текст с картинок, когда пользователь присылает тебе картинку - ты должен вернуть текст с неё. Если на ней нету текста, напиши "НЕТУ ТЕКСТА"',
                    }
                ],
            },
            {
                "role": "user",
                "content": [{"type": "text", "text": "Распознай текст с этих картинок"}],
            },
        ]
        for image in images:
            print(image)
            encoded_image = b64encode(image)
            messages[1]["content"].append(
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/webp;base64,{encoded_image.decode('utf-8')}",
                        "detail": "high",
                    },
                }
            )
        completion = self._session.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        return completion.choices[0].message.content
