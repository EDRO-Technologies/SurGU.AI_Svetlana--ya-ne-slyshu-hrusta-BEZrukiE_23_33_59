from .base import OCR


class TesseractOCR(OCR): 
    def __init__(self):
        ...

    def extract(self, images: list[bytes]) -> list[str]:
        ...
