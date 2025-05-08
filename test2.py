import pigpio
import time

class DHT11:
    def __init__(self, pi, gpio):
        self.pi = pi
        self.gpio = gpio
        self.cb = None
        self.high_tick = 0
        self.bits = []
    
    def _cb(self, gpio, level, tick):
        if level == 1:
            self.high_tick = tick
        elif level == 0:
            diff = pigpio.tickDiff(self.high_tick, tick)
            self.bits.append(1 if diff > 50 else 0)
    
    def read(self):
        self.bits = []

        # Send start signal
        self.pi.set_mode(self.gpio, pigpio.OUTPUT)
        self.pi.write(self.gpio, 0)
        time.sleep(0.018)
        self.pi.write(self.gpio, 1)
        self.pi.set_mode(self.gpio, pigpio.INPUT)

        # Setup callback
        self.cb = self.pi.callback(self.gpio, pigpio.EITHER_EDGE, self._cb)
        time.sleep(0.2)
        self.cb.cancel()

        if len(self.bits) < 40:
            raise RuntimeError("Failed to read enough bits")

        # Convert bits to bytes
        data = []
        for i in range(0, 40, 8):
            byte = 0
            for j in range(8):
                byte = (byte << 1) | self.bits[i + j]
            data.append(byte)

        checksum = sum(data[:4]) & 0xFF
        if data[4] != checksum:
            raise ValueError("Checksum failed")

        return data[2], data[0]  # temperature, humidity

pi = pigpio.pi()
sensor = DHT11(pi, 4)

try:
    while True:
        try:
            temp, hum = sensor.read()
            print(f"Temperature: {temp}°C, Humidity: {hum}%")
        except Exception as e:
            print("Error:", e)
        time.sleep(2)
except KeyboardInterrupt:
    print("Stopping...")
finally:
    pi.stop()
