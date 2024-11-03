import os

from pymongo import MongoClient

from .extractors.images.base import OCR
from .extractors.voice.base import STT
from .providers.base import Provider
from .extractors import FileType, get_file_type, prepare_images


class TVV:
    def __init__(
        self, provider: Provider, image_extractor: OCR | None = None, audio_extractor: STT | None = None
    ):
        self._db = MongoClient(host=os.getenv("MONGODB_HOST"), port=os.getenv("MONGODB_PORT"), username=os.getenv("MONGODB_USERNAME"), password=os.getenv("MONGODB_PASSWORD"))["TakVamVidno"]
        self._provider = provider
        self._image_extractor = image_extractor
        self._audio_extractor = audio_extractor

    def process(self, user_id: str | int, text: str = None, files: list[bytes] = None):
        if text is None and files is None:
            raise ValueError("text и file не могут быть одновременно 'None'")
        for file in files:
            file_type = get_file_type(file)
            if file_type != FileType.Image:
                # Пока не поддерживается
                raise ValueError("Файл данного типа не поддерживается.")
        images = prepare_images(files)
        text_from_files = self._image_extractor.extract(images)
        if not any(text_from_files):
            return None
        total_text = "\n".join(text for text in text_from_files if text)
        messages = self._get_chat_messages(user_id)
        messages, text, image = self._provider.generate_report(total_text, messages)
        # self._set_chat_messages(user_id, messages)
        return text, image


    def _get_chat_messages(self, user_id: str | int):
        return self._db.messages.find_one({"_id": user_id})

    def _set_chat_messages(self, user_id: str | int, messages: list[dict]):
        return self._db.messages.update_one({"_id":user_id}, {"$set": messages})