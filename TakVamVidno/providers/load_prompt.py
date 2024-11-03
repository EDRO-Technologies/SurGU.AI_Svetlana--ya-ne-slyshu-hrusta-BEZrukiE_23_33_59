from pathlib import Path


def load_prompt() -> str:
    return (Path(__file__).parent / "prompt").read_text()
