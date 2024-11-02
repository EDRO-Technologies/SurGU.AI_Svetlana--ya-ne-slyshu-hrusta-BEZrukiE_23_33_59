from io import BytesIO
from pathlib import Path

from PIL import Image

from ..extractors import prepare_images


def test_prepare_image_from_bytes():
    with open(Path(__file__).parent / "image.jpg", "rb") as f:
        content = f.read()
    images_bytes = prepare_images([content])
    image = Image.open(BytesIO(images_bytes[0]))
    assert max(image.size) == 512

def test_prepare_image_from_path():
    images_bytes = prepare_images([str(Path(__file__).parent / "image.jpg")])
    image = Image.open(BytesIO(images_bytes[0]))
    assert max(image.size) == 512
