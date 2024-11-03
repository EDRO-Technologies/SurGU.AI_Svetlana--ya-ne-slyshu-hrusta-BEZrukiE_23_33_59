from .extractors.images.base import OCR
from .extractors.voice.base import STT
from .providers.base import Provider
from .extractors import FileType, get_file_type, prepare_images


class TVV:
    def __init__(
        self, provider: Provider, image_extractor: OCR | None = None, audio_extractor: STT | None = None
    ):
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
        self._provider.generate_report(total_text)

    def _get_chat_messages(self, user_id: str | int):
        pass