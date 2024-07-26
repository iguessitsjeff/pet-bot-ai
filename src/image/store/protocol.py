from typing import Protocol


class ImageStore(Protocol):
    def save(content: bytes) -> bool:
        """
        Saves bytes into a storage provider and returns status.
        """
