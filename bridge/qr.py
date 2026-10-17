# pip install qrcode
import base64
def packMatrix(matrix):
    """Pack a square QR matrix (list of rows of True/False) into {"n": size, "d": base64 bits}.
    Bit number y * n + x is stored in byte (bit // 8), least significant bit first."""
    n = len(matrix)
    bits = bytearray((n * n + 7) // 8)
    for y, row in enumerate(matrix):
        for x, dark in enumerate(row):
            if dark:
                i = y * n + x
                bits[i >> 3] |= 1 << (i & 7)
    return {"n": n, "d": base64.b64encode(bits).decode("ascii")}


def makeQR(url):
    """QR code for `url`, in the smallest version that fits. The error correction is the
    lowest level: a screen can't get scratched, and fewer modules means bigger ones on the display."""
    import qrcode
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L, #type: ignore
        box_size=1,
        border=0,                     # the box adds its own white margin
    )
    qr.add_data(url)
    qr.make(fit=True)
    return packMatrix(qr.get_matrix())
