import gc
import time
from machine import ADC, Pin  # type: ignore

class Microphone:
    def __init__(self, pin=34, rate=8000, seconds=8):
        self.adc = ADC(Pin(pin))
        self.adc.atten(ADC.ATTN_11DB)
        self.rate = rate
        for s in range(seconds, 2, -1):
            gc.collect()
            try:
                buf = bytearray(rate * s)
            except MemoryError:
                continue
            gc.collect()
            if gc.mem_free() < 25000: #type: ignore
                buf = None
                continue
            self.buf = buf
            self.seconds = s
            break
        else:
            raise MemoryError("not enough RAM for the audio buffer")
        print("mic buffer:", self.seconds, "s")

    def record(self):
        buf = self.buf
        adc = self.adc
        n = len(buf)
        period = 1000000 // self.rate
        start = time.ticks_us() #type: ignore
        t = start
        for i in range(n):
            buf[i] = adc.read_u16() >> 8
            t = time.ticks_add(t, period) #type: ignore
            while time.ticks_diff(t, time.ticks_us()) > 0: #type: ignore
                pass
        elapsed = time.ticks_diff(time.ticks_us(), start) #type: ignore
        return buf, n * 1000000 // elapsed
