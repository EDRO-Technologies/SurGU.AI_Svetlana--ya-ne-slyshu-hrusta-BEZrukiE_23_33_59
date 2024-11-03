## 👀 Так вам видно

![Так вам видно](https://github.com/user-attachments/assets/f05c1e85-727d-4005-9a8d-676914dabcd1)


[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Библиотека для анализа документов и записей разговоров при помощи ИИ.

### ⚡ Ключевые фишки

- 👀 Визуализация данных. Не только текст, но ещё и графики, например, [интеллект-карта](https://ru.wikipedia.org/wiki/%D0%94%D0%B8%D0%B0%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B0_%D1%81%D0%B2%D1%8F%D0%B7%D0%B5%D0%B9).
- 🧐 Возможность задать вопрос по документу. Не надо больше искать иголку в стоге сена, можно просто спросить у ИИ.
- 🤩 Универсальная библиотека, с большой кастомизацией. С самого начала предоставляется выбор сервиса для превращения картинок в текст, обработки этого текста, итд.
- 😉 Простота использования. Для начала работы достаточно всего нескольких строчек кода.

### 👨‍💻 Установка и использование

#### Установка 
```bash
pip install TakVamVidno[openai] @ "git+https://github.com/holy-jesus/TakVamVidno"
```

Эта команда установить библиотеку TakVamVidno для использования `openai` в качестве распознавания текста с картинки и генерации ответа. 

Возможные варианты: 
- TakVamVidno[openai]
- TakVamVidno[tesseract]
- TakVamVidno[transformers]

#### Использование

Пример использования
```python
from TakVamVidno import TVV
from TakVamVidno.extractors import OpenAIOCR, prepare_images
from TakVamVidno.providers import OpenAIProvider

tvv = TVV(OpenAIProvider(), OpenAIOCR())
images = prepare_images(["./image.jpg"])
tvv.process(None, files=images)
```

### 📆 Планы

- Дописать `README.md` :)
- Дописать план :))
