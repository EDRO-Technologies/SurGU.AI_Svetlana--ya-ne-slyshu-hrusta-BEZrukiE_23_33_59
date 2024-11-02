from io import BytesIO

from PIL import Image, ImageOps


def prepare_images(images: list[bytes | str]) -> list[bytes]:
    """
    Подготавливает картинки для распознавания, переводя в необходимый формат (webp) и уменьшая разрешение картинки.

    Argumemnts
    ----------
    images : list[bytes | str]
        Лист картинок в виде байтов или пути до файла.

    Returns
    -------
    Лист с байтами картинок переведенными в webp и уменьшиным разрешением
    """
    ready_images = []
    for image in images:
        if isinstance(image, str):
            with open(image, "rb") as f:
                image = f.read()
        image = Image.open(BytesIO(image))
        cropped_image = ImageOps.contain(image, (512, 512))
        image_file = BytesIO()
        cropped_image.save(image_file, "webp")
        image_file.seek(0)
        ready_images.append(image_file.getvalue())
    return ready_images
