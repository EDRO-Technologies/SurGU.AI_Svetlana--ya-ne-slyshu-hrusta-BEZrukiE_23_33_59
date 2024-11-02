"""
Распознаватели текста с картинки
"""

from ._openai import OpenAIOCR
from ._tesseract import TesseractOCR
from ._transformers import TransformersOCR
from .prepare_images import prepare_images
