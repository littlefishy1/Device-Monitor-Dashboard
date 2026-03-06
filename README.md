# Device Monitor Dashboard

## Option Chosen

I chose **Option A (Python + PyQt6)**.

Python is the language I am most comfortable with and PyQt6 provides a straightforward way to build desktop user interfaces. I also used **pyqtgraph** for plotting because it integrates well with PyQt and supports real time updates efficiently. This option allowed me to focus more on application structure and UI interaction

---

# How to Build and Run

### 1. Clone the repository

```bash
git clone https://github.com/littlefishy1/Device-Monitor-Dashboard
cd Device-Monitor-Dashboard
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```


### 3. Run the application

```bash
python main.py
```

A dashboard window should appear.  
Press **Start** to begin the simulated sensor updates.

---

# Code Architecture

The project is divided into two main layers: the **logic layer** and the **UI layer**.

```
project/
│
├── main.py
│
├── core/
│   ├── sensor.py
│   └── simulator.py
│
└── tests/
    └── test_sensors.py
```

---

## Sensors (`sensor.py`)

This file defines the simulated sensors:

- `TemperatureSensor`
- `HumiditySensor`
- `PressureSensor`

Each sensor contains:

- Sensor name
- Measurement unit
- Minimum and maximum values
- Warning thresholds
- Current simulated value

The sensors generate data using a simple update function. I kept the sensor classes in a separate file so the data generation logic is isolated from the UI and easier to test.

---

## Data Simulator (`simulator.py`)

The `DataSimulator` class manages sensor updates.

It uses a **QTimer** to update sensor values every second and emits a signal whenever new data is generated.

Responsibilities include:

- Updating sensor values
- Starting and stopping the simulation
- Notifying the UI when data changes

I separated the simulator from the UI so the timer and update loop are handled in one place instead of being mixed into the window code.


---

## User Interface (`main.py`)

The UI is built in `main.py`.

Main components include:

### MainWindow

The main dashboard window.  
It creates the layout, connects the simulator to the UI, and handles user controls. 

### SensorCard

Displays the current value of a sensor and shows warning messages if thresholds are exceeded.

### SensorChart

Displays a real-time graph of sensor data using **pyqtgraph**.

I kept the UI components in `main.py` because they are mainly responsible for display and interaction, while the sensor logic stays in the core layer.


---

# Design Patterns Used

### Observer Pattern

Qt’s **signal / slot system** is used to update the UI whenever new sensor data is generated.

Example flow:

```
DataSimulator updates sensors
        ↓
DataSimulator emits signal
        ↓
MainWindow receives signal
        ↓
UI components refresh
```

This allows the data logic and UI to remain loosely coupled.

---

# Architecture Diagram

```
          +-------------------+
          |   DataSimulator   |
          |-------------------|
          | updates sensors   |
          | emits signal      |
          +---------+---------+
                    |
              data_updated
                    |
                    v
             +------+------+
             |  MainWindow |
             +------+------+
                    |
       +------------+-------------+
       |                          |
       v                          v
   SensorCard                 SensorChart
 (display values)        (display data graph)
```

---

# Features Implemented

The application includes the following features:

- Main window with organized layout
- Three simulated sensors (temperature, humidity, pressure)
- Automatic updates every second
- Real time chart showing recent sensor values
- Start / Stop button for the simulation
- Reset button
- Warning indicators when thresholds are exceeded
- Warning toggle button


Additional bonus features:

- Export sensor data to CSV
- Unit tests for the sensor logic

---

# Unit Tests

Basic unit tests are included for the sensor logic.

The tests verify:

- Sensor metadata (name and unit)
- Generated values remain within valid ranges
- Warning detection works correctly

To run the tests:

```bash
python tests/test_sensors.py
```

---

# Known Issues / Possible Improvements

If I had more time, I would improve several things:

- Improve chart axis labeling and scaling
- Make warning thresholds configurable instead of hard-coded
- Improve UI styling and layout responsiveness
- Add more unit tests for the simulator logic
- Further separate UI and logic layers

---

# Notes

The goal of this project was to keep the application simple while demonstrating:

- Clean code structure
- Separation of logic and UI
- Object oriented design
- Rreal time updates using timers
- Basic testing of the data layer

Thus, I chose not to implement theme toggle which will make the application too complicated
