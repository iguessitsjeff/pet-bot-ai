from typing import Protocol

from src.image.store.protocol import ImageStore


class ImageGenerator(Protocol):
    def generate_image(self, prompt: str, image_store: ImageStore = None) -> bytes:
        pass
