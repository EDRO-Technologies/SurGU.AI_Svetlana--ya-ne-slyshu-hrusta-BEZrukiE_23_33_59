from io import BytesIO

from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image

from .base import OCR


class TransformersOCR(OCR):
    """
    Класс для локального распознавания текста.

    Рекомендуемые модели:
        - `raxtemur/trocr-base-ru` для рукописного русского текста
        - `microsoft/trocr-base-handwritten` для рукописного английского текста

    Argumemnts
    ----------
    model : str
        ID модели для распознавания

    Example
    -------
    >>> from TakVamVidno.extractors.images import TransformersOCR, prepare_images
    >>> ocr = TransformersOCR()
    >>> result = ocr.extract(prepare_images(["./image.jpg"]))
    >>> print(result[0])
    """
    def __init__(self, model: str = "raxtemur/trocr-base-ru"):
        self._processor = TrOCRProcessor.from_pretrained(model)
        self._model = VisionEncoderDecoderModel.from_pretrained(model)

    def extract(self, images: list[bytes]) -> list[str | None]:
        results = []
        for image in images:
            pixel_values = self._processor(
                Image.open(BytesIO(image)).convert("RGB"), return_tensors="pt"
            ).pixel_values
            generated_ids = self._model.generate(pixel_values)
            results.append(
                self._processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            )
        return results
