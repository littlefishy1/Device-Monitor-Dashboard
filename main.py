import sys

from PyQt6.QtCore import Qt, QDateTime
from PyQt6.QtWidgets import QApplication, QMainWindow, QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget


from core.simulator import DataSimulator

from collections import deque
import pyqtgraph as pg

_CHART_COLORS = ["#ef5350", "#42a5f5", "#66bb6a"]


class SensorCard(QFrame):
    def __init__(self, sensor, parent=None):
        super().__init__(parent)
        self._sensor = sensor
        self._warnings_visible = True
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setMinimumWidth(220)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(10)

        self._name_label = QLabel(sensor.name)
        self._name_label.setAlignment( Qt.AlignmentFlag.AlignCenter)
        self._name_label.setStyleSheet("font-size: 15px; font-weight: bold; color: #aaaaaa;")

        self._value_label = QLabel("--")
        self._value_label.setAlignment( Qt.AlignmentFlag.AlignCenter)
        self._value_label.setStyleSheet("font-size: 50px; font-weight: bold; color: #ffffff;")

        self._unit_label = QLabel(sensor.unit)
        self._unit_label.setAlignment( Qt.AlignmentFlag.AlignCenter)
        self._unit_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #888888;")

        self._warn_label = QLabel("")
        self._warn_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._warn_label.setStyleSheet("font-size: 15px; color: #e53935;")

        layout.addWidget(self._name_label)
        layout.addWidget(self._value_label)
        layout.addWidget(self._unit_label)
        layout.addWidget(self._warn_label)

        self.setStyleSheet(
            "SensorCard { background-color: #2b2b2b; border-radius: 10px; padding: 15px; }"
        )

    def set_warnings_visible(self, visible: bool):
        self._warnings_visible = visible
        if not visible:
            self._value_label.setStyleSheet("font-size: 50px; font-weight: bold; color: #ffffff;")
            self._warn_label.setText("")

    def refresh(self):
        val = self._sensor.value()
        self._value_label.setText(str(val))

        if not self._warnings_visible:
            return

        if self._sensor.warn_high is not None and val > self._sensor.warn_high:
            self._value_label.setStyleSheet("font-size: 50px; font-weight: bold; color: #e53935;")
            self._warn_label.setStyleSheet("font-size: 15px; color: #e53935;")
            self._warn_label.setText("⚠ Too High")

        elif self._sensor.warn_low is not None and val < self._sensor.warn_low:
            self._value_label.setStyleSheet("font-size: 50px; font-weight: bold; color: #e53935;")
            self._warn_label.setStyleSheet("font-size: 15px; color: #e53935;")
            self._warn_label.setText("⚠ Too Low")

        else:
            self._value_label.setStyleSheet("font-size: 50px; font-weight: bold; color: #ffffff;")
            self._warn_label.setStyleSheet("font-size: 15px; color: #66bb6a;")
            self._warn_label.setText("Safe")


class SensorChart(pg.PlotWidget):
    MAX_POINTS = 30

    def __init__(self, sensor, color, parent=None):
        super().__init__(parent=parent, background="#1e1e1e")
        self._sensor = sensor
        self._data = deque(maxlen=self.MAX_POINTS)

        self.setTitle(sensor.name, color="#aaaaaa", size="10pt")
        self.getPlotItem().hideAxis("bottom")
        self.getPlotItem().getAxis("left").setTextPen("#888888")
        self.setMouseEnabled(x=False, y=False)
        self.setMenuEnabled(False)
        self.setMinimumHeight(150)

        self._high_line = None
        self._low_line = None
        if sensor.warn_high is not None:
            self._high_line = self.addLine(y=sensor.warn_high, pen=pg.mkPen("#e53935", width=1, style=Qt.PenStyle.DashLine))
        if sensor.warn_low is not None:
            self._low_line = self.addLine(y=sensor.warn_low, pen=pg.mkPen("#e53935", width=1, style=Qt.PenStyle.DashLine))

        self._curve = self.plot(pen=pg.mkPen(color, width=2))

    def set_lines_visible(self, visible: bool):
        if self._high_line is not None:
            self._high_line.setVisible(visible)
        if self._low_line is not None:
            self._low_line.setVisible(visible)

    def refresh(self):
        self._data.append(self._sensor.value())
        self._curve.setData(list(self._data))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Device Monitor Dashboard")
        self.resize(1000, 700)
        self.setStyleSheet("background-color: #1e1e1e;")

        self._simulator = DataSimulator(self)
        self._simulator.data_updated.connect(self._on_data_updated)
        self._warnings_enabled = True

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(30, 25, 30, 25)
        root.setSpacing(25)

        # title bar
        title = QLabel("Device Monitor Dashboard")
        title.setAlignment( Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 25px; font-weight: bold; color: #ffffff;")
        root.addWidget(title)

        # sensor cards 
        cards_row = QHBoxLayout()
        cards_row.setSpacing(20)
        self._cards = []
        for sensor in self._simulator.sensors:
            card = SensorCard(sensor)
            self._cards.append(card)
            cards_row.addWidget(card)
        root.addLayout(cards_row)

        # charts
        charts_row = QHBoxLayout()
        charts_row.setSpacing(20)
        self._charts = []
        for sensor, color in zip(self._simulator.sensors, _CHART_COLORS):
            chart = SensorChart(sensor, color)
            self._charts.append(chart)
            charts_row.addWidget(chart)
        root.addLayout(charts_row)

        # controls row: warnings toggle | start/stop  | reset
        controls_row = QHBoxLayout()
        controls_row.setSpacing(15)
        self._toggle_btn = QPushButton()
        self._toggle_btn.setFixedHeight(50)
        self._toggle_btn.setMinimumWidth(100)
        self._toggle_btn.clicked.connect(self._toggle_simulation)
        self._set_toggle_style(False)
        self._warn_toggle_btn = QPushButton("Warnings: ON")
        self._warn_toggle_btn.setFixedHeight(50)
        self._warn_toggle_btn.setMinimumWidth(130)
        self._warn_toggle_btn.setStyleSheet(
            "QPushButton { font-size: 13px; font-weight: bold; color: #ffffff;"
            " background-color: #1565c0; border-radius: 10px; }"
            "QPushButton:hover { background-color: #1976d2; }"
        )
        self._warn_toggle_btn.clicked.connect(self._on_toggle_warnings)
        self._reset_btn = QPushButton("Reset")
        self._reset_btn.setFixedHeight(50)
        self._reset_btn.setMinimumWidth(100)
        self._reset_btn.setStyleSheet(
            "QPushButton { font-size: 13px; font-weight: bold; color: #ffffff;"
            " background-color: #37474f; border-radius: 10px; }"
            "QPushButton:hover { background-color: #455a64; }"
        )
        self._reset_btn.clicked.connect(self._on_reset)
        controls_row.addStretch()
        controls_row.addWidget(self._warn_toggle_btn)
        controls_row.addWidget(self._toggle_btn)
        controls_row.addWidget(self._reset_btn)
        controls_row.addStretch()
        root.addLayout(controls_row)

        # status
        self._status_label = QLabel("Not started yet")
        self._status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._status_label.setStyleSheet("font-size: 15px; color: #666666;")
        root.addWidget(self._status_label)

    def _set_toggle_style(self, running: bool):
        if running:
            label, bg, hover = "Stop", "#c62828", "#d32f2f"
        else:
            label, bg, hover = "Start", "#2e7d32", "#388e3c"

        self._toggle_btn.setText(label)
        self._toggle_btn.setStyleSheet(
            "QPushButton { font-size: 15px; font-weight: bold; color: #ffffff;"
            f" background-color: {bg}; border-radius: 10px; }}"
            f"QPushButton:hover {{ background-color: {hover}; }}"
        )

    def _on_toggle_warnings(self):
        self._warnings_enabled = not self._warnings_enabled
        for card in self._cards:
            card.set_warnings_visible(self._warnings_enabled)
        for chart in self._charts:
            chart.set_lines_visible(self._warnings_enabled)
        if self._warnings_enabled:
            label, bg, hover = "Warnings: ON", "#1565c0", "#1976d2"

        else:
            label, bg, hover = "Warnings: OFF", "#546e7a", "#607d8b"

        self._warn_toggle_btn.setText(label)
        self._warn_toggle_btn.setStyleSheet(
            "QPushButton { font-size: 15px; font-weight: bold; color: #ffffff;"
            f" background-color: {bg}; border-radius: 10px; }}"
            f"QPushButton:hover {{ background-color: {hover}; }}"
        )

    def _on_reset(self):
        self._simulator.stop()
        self._set_toggle_style(False)
        for sensor in self._simulator.sensors:
            sensor._tick = 0
        for chart in self._charts:
            chart._data.clear()
            chart._curve.setData([])
        for card in self._cards:
            card._value_label.setText("--")
            card._value_label.setStyleSheet("font-size: 50px; font-weight: bold; color: #ffffff;")
            card._warn_label.setText("")
        self._status_label.setText("Not started yet")

    def _toggle_simulation(self):
        self._simulator.toggle()
        self._set_toggle_style(self._simulator.running)

    def _on_data_updated(self):
        for card in self._cards:
            card.refresh()
        for chart in self._charts:
            chart.refresh()
        now = QDateTime.currentDateTime().toString("hh:mm:ss AP")
        self._status_label.setText(f"Last updated at {now}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
