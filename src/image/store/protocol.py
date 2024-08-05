from typing import Protocol


class ImageStore(Protocol):
    def save(self, content: bytes) -> bool:
        """
        Saves bytes into a storage provider and returns status.
        """
