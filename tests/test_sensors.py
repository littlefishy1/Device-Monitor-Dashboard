import os
import sys
import unittest


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

from core.sensor import HumiditySensor, PressureSensor, TemperatureSensor

class TestTemperatureSensor(unittest.TestCase):
    def setUp(self):
        self.sensor = TemperatureSensor()

    def test_name_and_unit(self):
        self.assertEqual(self.sensor.name, "Temperature")
        self.assertEqual(self.sensor.unit, "°C")

    def test_value_stays_in_range(self):
        for i in range(50):
            self.sensor.update()
            val =  self.sensor.value()
            self.assertGreaterEqual(val, self.sensor.min_val)
            self.assertLessEqual(val, self.sensor.max_val)

    def test_warning_behavior(self):
        self.sensor._value = 10.0
        self.assertTrue(self.sensor.is_warning())

        self.sensor._value = 30.0
        self.assertFalse(self.sensor.is_warning())

        self.sensor._value = 45.0
        self.assertTrue(self.sensor.is_warning())


class TestHumiditySensor(unittest.TestCase):
    def setUp(self):
        self.sensor = HumiditySensor()

    def test_name_and_unit(self):
        self.assertEqual(self.sensor.name, "Humidity")
        self.assertEqual(self.sensor.unit, "%")

    def test_value_stays_in_range(self):
        for i in range(50):
            self.sensor.update()
            val =  self.sensor.value()
            self.assertGreaterEqual(val, self.sensor.min_val)
            self.assertLessEqual(val, self.sensor.max_val)

    def test_warning_behavior(self):
        self.sensor._value = 10.0
        self.assertTrue(self.sensor.is_warning())

        self.sensor._value = 40.0
        self.assertFalse(self.sensor.is_warning())

        self.sensor._value = 60.0
        self.assertTrue(self.sensor.is_warning())


class TestPressureSensor(unittest.TestCase):
    def setUp(self):
        self.sensor = PressureSensor()

    def test_name_and_unit(self):
        self.assertEqual(self.sensor.name, "Pressure")
        self.assertEqual(self.sensor.unit, "hPa")

    def test_value_stays_in_range(self):
        for i in range(100):
            self.sensor.update()
            val =  self.sensor.value()
            self.assertGreaterEqual(val, self.sensor.min_val)
            self.assertLessEqual(val, self.sensor.max_val)

    def test_warning_behavior(self):
        self.sensor._value = 980.0
        self.assertTrue(self.sensor.is_warning())

        self.sensor._value = 1010.0
        self.assertFalse(self.sensor.is_warning())

        self.sensor._value = 1040.0
        self.assertTrue(self.sensor.is_warning())


if __name__ == "__main__":
    unittest.main()