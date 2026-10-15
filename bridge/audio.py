import wave
from pathlib import Path
try:
    import numpy as np
except ImportError:
    np = None

def despike(samples):
    out = bytearray(samples)
    for i in range(1, len(samples) - 1):
        a, b, c = samples[i - 1], samples[i], samples[i + 1]
        out[i] = sorted((a, b, c))[1]
    return bytes(out)

def analyze(samples, rate):
    n = len(samples)
    ordered = sorted(samples)
    mean = sum(samples) / n
    p1, p99 = ordered[int(n * 0.01)], ordered[int(n * 0.99)]
    stats = {
        "level": p99 - p1,
        "mean": round(mean),
        "spikesPct": round(100 * sum(1 for s in samples if s in (0, 255)) / n, 2),
    }
    if np is not None:
        x = np.frombuffer(samples, dtype=np.uint8).astype(float)
        x -= x.mean()
        spectrum = np.abs(np.fft.rfft(x * np.hanning(len(x)))) ** 2
        freqs = np.fft.rfftfreq(len(x), 1 / rate)
        spectrum[freqs < 20] = 0                              # ignore DC and slow drift
        peak = int(spectrum.argmax())
        window = (freqs > freqs[peak] - 15) & (freqs < freqs[peak] + 15)
        stats["dominantHz"] = round(float(freqs[peak]))
        stats["dominantSharePct"] = round(100 * float(spectrum[window].sum() / spectrum.sum()))
    return stats

def saveWav(samples, rate, path=None):
    path = Path(path) if path else Path(__file__).parent / "capture.wav"
    stats = analyze(samples, rate)
    clean = despike(samples)
    mean = sum(clean) / len(clean)
    centered = bytes(max(0, min(255, int(s - mean + 128))) for s in clean)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(1)
        w.setframerate(rate)
        w.writeframes(centered)
    return {"saved": path.name, "seconds": round(len(samples) / rate, 1), "rate": rate, **stats}

def toRecognitionWav(samples, rate, path=None):
    if np is None:
        raise RuntimeError("numpy is required for recognition: pip install numpy")
    path = Path(path) if path else Path(__file__).parent / "capture_16k.wav"

    x = np.frombuffer(samples, dtype=np.uint8).astype(np.float64)
    x -= x.mean()
    if len(x) > 2:
        x[1:-1] = np.median(np.stack([x[:-2], x[1:-1], x[2:]]), axis=0)

    peak = np.percentile(np.abs(x), 99.5) or 1.0
    x = np.clip(x / peak * 0.7, -1.0, 1.0)
    target = 16000
    old_t = np.arange(len(x)) / rate
    new_t = np.arange(int(len(x) / rate * target)) / target
    y = np.interp(new_t, old_t, x)

    pcm = (y * 32767).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(target)
        w.writeframes(pcm.tobytes())
    return str(path)
