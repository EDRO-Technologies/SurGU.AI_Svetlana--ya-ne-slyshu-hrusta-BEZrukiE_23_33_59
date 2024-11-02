from .base import Provider
from transformers import PreTrainedModel

class TransformersProvider(Provider):
    def __init__(self, model: str, token: str | None):
        self.model = PreTrainedModel.from_pretrained()
