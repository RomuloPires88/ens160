# eCO₂ Sensor Logger with Real-Time Plotting

This Python application interfaces with the **Adafruit ENS160** air quality sensor via I2C to monitor and log **eCO₂ (equivalent CO₂)** concentrations in real time. It includes a graphical interface using `matplotlib` with control buttons and keyboard shortcuts to define initial time markers, adjust environment parameters, save data, and more.

## Features

- 📊 Real-time plotting of eCO₂ data
- 🕒 Marker button or **spacebar shortcut** to define an initial reference time
- 💾 Save data to CSV (starting from the initial time)
- 🌡️ Manual input for temperature and humidity compensation
- 🔁 Restart and stop data collection
- ❌ Exit button with confirmation dialog
- 🧭 Simple GUI for setting environmental parameters using `tkinter`

## Dependencies

Make sure you have the following Python libraries installed:

- `adafruit-circuitpython-ens160`
- `matplotlib`
- `tkinter` (comes with most Python installations)
- `board`
- `csv`
- `datetime`
- `os`

You can install the required libraries using `pip`:

```bash
pip install matplotlib adafruit-circuitpython-ens160
