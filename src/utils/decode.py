import base64
import gzip


def decode_and_uncompress(data: str) -> str:
    compressed = base64.decodebytes(data.encode())
    return gzip.decompress(data=compressed).decode()
