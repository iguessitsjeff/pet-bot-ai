import requests


def download_image(url: str) -> bytes:
    image_response = requests.get(url=url)

    image_response.raise_for_status()

    return image_response.content
