from .base import OCR


class TesseractOCR(OCR): 
    def __init__(self, tesseract_cmd: str):
        """
        Класс для распознавания текста при помощи Tesseract

        Arguments
        ---------
        tesseract_cmd : str 
            Полный путь до запускного файла Tesseract
        """
        import pytesseract
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        self._pytesseract = pytesseract

    def extract(self, images: list[bytes]) -> list[str]:
        results = []
        for image in images:
            results.append(self._pytesseract.image_to_string(image))
        return results
