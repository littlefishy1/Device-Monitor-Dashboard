from PyQt6.QtCore import QObject, QTimer, pyqtSignal

from .sensor import HumiditySensor, PressureSensor, TemperatureSensor


class DataSimulator(QObject):
    data_updated = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.sensors = [TemperatureSensor(),HumiditySensor(), PressureSensor()]
        self._running = False
        self._timer = QTimer(self)
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._tick)


    @property
    def running(self):
        return self._running

    def start(self):
        if not self._running:
            self._running = True
            self._timer.start()

    def stop(self):
        if self._running:
            self._running = False
            self._timer.stop()

    def toggle(self):
        self.stop() if self._running else self.start()

    def _tick(self):
        for sensor in self.sensors:
            sensor.update()
        self.data_updated.emit()
