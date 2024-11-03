from .extractors.images.base import OCR
from .extractors.voice.base import STT
from .extractors import FileType, get_file_type


class TVV:
    def __init__(
        self, image_extractor: OCR | None = None, audio_extractor: STT | None = None
    ):
        self._image_extractor = image_extractor
        self._audio_extractor = audio_extractor

    def process(self, text: str = None, file: list[bytes] = None):
        if text is None and file is None:
            raise ValueError("text и file не могут быть одновременно 'None'")
        file_type = get_file_type(file)
        if file_type != FileType.Image:
            # Пока не поддерживается
            return None
