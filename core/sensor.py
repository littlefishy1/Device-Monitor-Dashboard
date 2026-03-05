import math
import random
from collections import deque

MAX_HISTORY = 30


class Sensor:
    def __init__(self, name, unit, min_val, max_val, threshold):
        self.name = name
        self.unit = unit
        self.min_val = min_val
        self.max_val = max_val
        self.threshold = threshold
        self._value = min_val
        self._tick = 0
        self.history = deque(maxlen=MAX_HISTORY)

    @property
    def value(self):
        return self._value

    @property
    def is_above_threshold(self):
        return self._value > self.threshold

    def update(self):
        self._tick += 1
        self._value = self._generate()
        self.history.append(self._value)

    def reset(self):
        self._tick = 0
        self._value = self.min_val
        self.history.clear()

    def _generate(self):
        raise NotImplementedError


class TemperatureSensor(Sensor):
    def __init__(self):
        super().__init__("Temperature", "°C", 15.0, 42.0, 35.0)

    def _generate(self):
        base = 27.0
        sine = 9.0 * math.sin(self._tick * 0.15)
        noise = random.uniform(-1.5, 1.5)
        return round(max(self.min_val, min(self.max_val, base + sine + noise)), 1)


class HumiditySensor(Sensor):
    def __init__(self):
        super().__init__("Humidity", "%", 20.0, 95.0, 75.0)

    def _generate(self):
        base = 55.0
        sine = 22.0 * math.sin(self._tick * 0.08 + 1.0)
        noise = random.uniform(-3.0, 3.0)
        return round(max(self.min_val, min(self.max_val, base + sine + noise)), 1)


class PressureSensor(Sensor):
    def __init__(self):
        super().__init__("Pressure", "hPa", 980.0, 1040.0, 1030.0)

    def _generate(self):
        base = 1013.25
        sine = 12.0 * math.sin(self._tick * 0.05 + 0.5)
        noise = random.uniform(-2.0, 2.0)
        return round(max(self.min_val, min(self.max_val, base + sine + noise)), 1)
