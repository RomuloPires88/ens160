# ENS160 MOX Gas Sensor
Script for CO2 sensor

# eCO_2 Sensor Logger with Real-Time Plotting

This Python application interfaces with the **Adafruit ENS160** air quality sensor via I2C to monitor and log **eCOâ‚‚ (equivalent COâ‚‚)** concentrations in real time. It includes a graphical interface using `matplotlib` with control buttons and keyboard shortcuts to define initial time markers, adjust environment parameters, save data, and more.

## Features

- ðŸ“Š Real-time plotting of eCOâ‚‚ data
- ðŸ•’ Marker button or **spacebar shortcut** to define an initial reference time
- ðŸ’¾ Save data to CSV (starting from the initial time)
- ðŸŒ¡ï¸ Manual input for temperature and humidity compensation
- ðŸ” Restart and stop data collection
- âŒ Exit button with confirmation dialog
- ðŸ§­ Simple GUI for setting environmental parameters using `tkinter`

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

