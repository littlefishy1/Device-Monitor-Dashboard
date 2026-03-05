import math
import random


class Sensor:
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

    def _generate(self):
        raise NotImplementedError


class TemperatureSensor(Sensor):
    def __init__(self):
        super().__init__("Temperature", "°C", 15.0, 42.0)

    def _generate(self):
        base = 27.0
        sine = 8.0 * math.sin(self._tick * 0.15)
        noise = random.uniform(-1.5, 1.5)
        value = round(max(self.min_val, min(self.max_val, base + sine + noise)), 1)
        return value


class HumiditySensor(Sensor):
    def __init__(self):
        super().__init__("Humidity", "%", 20.0, 95.0)

    def _generate(self):
        base = 45.0
        sine = 15.0 * math.sin(self._tick * 0.08 + 1.0)
        noise = random.uniform(-3.0, 3.0)
        value = round(max(self.min_val, min(self.max_val, base + sine + noise)), 1)
        return value


class PressureSensor(Sensor):
    def __init__(self):
        super().__init__("Pressure", "hPa", 980.0, 1040.0)

    def _generate(self):
        base = 1010.0
        sine = 10.0 * math.sin(self._tick * 0.05 + 0.5)
        noise = random.uniform(-2.0, 2.0)
        value = round(max(self.min_val, min(self.max_val, base + sine + noise)), 1)
        return value
