from .base import Provider


class TransformersProvider(Provider):
    def __init__(self, model: str, token: str | None):
        from transformers import PreTrainedModel
    
    def generate_report(self, text: str, messages: list[str]) -> str:
        pass