import ubinascii  # type: ignore


def drawQR(display, qr, x=None, inverted=True, show=True):
    """Draw a QR code as big as the screen allows, using a whole number of pixels per module
    (scanners need every module to be the same size, so the code is never stretched).
    `qr` is {"n": size, "d": base64 bits}.

    inverted=True  lit modules on a black screen: no big bright block, so phone cameras don't
                   wash out the code (current iPhone and Android camera apps read these).
    inverted=False the usual dark modules on a white square.

    How big it gets depends on the code: 33x33 modules (today's long login URL) only fits at
    1 pixel per module, while 29x29 or smaller (a shorter URL) fits at 2 pixels per module.

    x     left edge in pixels (None = centred). show=False lets the caller add text before the
          screen is refreshed. Returns the x position just right of the code."""
    n = qr["n"]
    bits = ubinascii.a2b_base64(qr["d"])

    scale = max(1, display.height // n)
    size = n * scale
    left = x if x is not None else (display.width - size) // 2
    top = (display.height - size) // 2
    module = 1 if inverted else 0

    display.fill(0)
    if not inverted:
        display.fillRect(left, top, size, size, 1)
    for y in range(n):
        for x in range(n):
            i = y * n + x
            if (bits[i >> 3] >> (i & 7)) & 1:
                display.fillRect(left + x * scale, top + y * scale, scale, scale, module)
    if show:
        display.show()
    return left + size
