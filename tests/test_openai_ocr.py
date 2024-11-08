from pathlib import Path

from dotenv import load_dotenv

from TakVamVidno.extractors import OpenAIOCR
from TakVamVidno.extractors import prepare_images


load_dotenv(".env")


def test_openai_ocr():
    ocr = OpenAIOCR()
    with open(Path(__file__).parent / "image.jpg", "rb") as f:
        content = f.read()
    images = prepare_images([content])
    text = ocr.process(images)
    assert text


if __name__ == "__main__":
    test_openai_ocr()
