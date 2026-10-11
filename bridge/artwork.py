# pip install pillow requests
import io
import base64
import requests
from PIL import Image, ImageOps


def toBitmap(imageBytes, size=32):
    """Turn image bytes into a size x size 1-bit bitmap in the layout
    framebuf.MONO_VLSB expects, returned as base64 text."""
    image = Image.open(io.BytesIO(imageBytes)).convert("L")
    image = ImageOps.fit(image, (size, size))
    image = ImageOps.autocontrast(image)
    image = image.convert("1")

    bitmap = bytearray(size * size // 8)
    for y in range(size):
        for x in range(size):
            if image.getpixel((x, y)):
                bitmap[(y // 8) * size + x] |= 1 << (y % 8)
    return base64.b64encode(bitmap).decode("ascii")

_cache = {"url": None, "bitmap": None}

def getArtwork(url, size=32, timeout=3):
    """Download and convert the cover, but only when the URL changes."""
    if url != _cache["url"]:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        _cache["bitmap"] = toBitmap(response.content, size) #type: ignore
        _cache["url"] = url
    return _cache["bitmap"]
