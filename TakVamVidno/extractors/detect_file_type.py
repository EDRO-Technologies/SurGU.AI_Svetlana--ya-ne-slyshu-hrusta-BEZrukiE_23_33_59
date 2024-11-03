from enum import Enum

import magic


class FileType(Enum):
    Image = 0
    Audio = 1
    Else = 2


def get_file_type(file: bytes) -> FileType:
    mime = magic.Magic(mime=True)

    file_type = mime.from_buffer(file)
    if file_type.startswith("image"):
        return FileType.Image
    elif file_type.startswith("audio"):
        return FileType.Audio
    else:
        return FileType.Else
