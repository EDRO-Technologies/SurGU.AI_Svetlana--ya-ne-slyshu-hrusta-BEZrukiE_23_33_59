from PIL import Image
from io import BytesIO


from TakVamVidno import TVV
from TakVamVidno.providers import OpenAIProvider
from TakVamVidno.extractors import OpenAIOCR, OpenAIWhisper

tvv = TVV(OpenAIProvider(), OpenAIOCR(), OpenAIWhisper())

with open("C:/PATH/image.jpg", "rb") as f:
    content = f.read()

text, image = tvv.process(None, files=[content])
print(text)

Image.open(BytesIO(image)).show()