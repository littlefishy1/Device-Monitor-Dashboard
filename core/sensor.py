import math
import random


class Sensor:
    warn_low = None
    warn_high = None

    def __init__(self, name, unit, min_val, max_val):
        self.name = name
        self.unit = unit
        self.min_val = min_val
        self.max_val = max_val
        self._value = min_val
        self._tick = 0

    def value(self):
        return self._value

    def update(self):
        self._tick += 1
        self._value = self._generate()

    def is_warning(self):
        if self.warn_low is not None and self._value < self.warn_low:
            return True
        if self.warn_high is not None and self._value > self.warn_high:
            return True
        return False

    def _generate(self):
        raise NotImplementedError


class TemperatureSensor(Sensor):
    warn_low = 20.0
    warn_high = 40.0

    def __init__(self):
        super().__init__("Temperature", "°C", 15.0, 45.0)

    def _generate(self):
        base = 30.0
        sine = 15.0 * math.sin(self._tick * 0.15)
        noise = random.uniform(-0.5, 0.5)
        value = round(max(self.min_val, min(self.max_val, base + sine + noise)), 1)
        return value


class HumiditySensor(Sensor):
    warn_low = 25.0
    warn_high = 55.0

    def __init__(self):
        super().__init__("Humidity", "%", 20.0, 60.0)

    def _generate(self):
        base = 40.0
        sine = 20.0 * math.sin(self._tick * 0.08 + 1.0)
        noise = random.uniform(-1.0, 1.0)
        value = round(max(self.min_val, min(self.max_val, base + sine + noise)), 1)
        return value


class PressureSensor(Sensor):
    warn_low = 995.0
    warn_high = 1025.0

    def __init__(self):
        super().__init__("Pressure", "hPa", 980.0, 1040.0)

    def _generate(self):
        base = 1010.0
        sine = 25.0 * math.sin(self._tick * 0.05 + 0.5)
        noise = random.uniform(-1.0, 1.0)
        value = round(max(self.min_val, min(self.max_val, base + sine + noise)), 1)
        return value
