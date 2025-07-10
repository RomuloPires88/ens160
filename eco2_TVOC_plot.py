import time
import board
import adafruit_ens160
import matplotlib.pyplot as plt
import csv
import os
from datetime import datetime
from matplotlib.widgets import Button
import tkinter as tk
from tkinter import messagebox

# Setup tkinter root (invisible)
#root = tk.Tk()
#root.withdraw()

# Dialog for Temperature and Humidity
def get_enviroment_conditions():
    def submit():
        try:
            temp = float(temp_entry.get())
            hum = float(hum_entry.get())
            env_values['temp'] = temp
            env_values['hum'] = hum
            env_window.destroy()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid number for temperature and humudity.")
            
    env_values = {}
    env_window = tk.Tk()
    env_window.title("Ambient Conditions")
    
    tk.Label(env_window, text="Temperature (ÂºC):").grid(row=0,column=0)
    temp_entry = tk.Entry(env_window)
    temp_entry.insert(0,"22") # Default value
    temp_entry.grid(row=0, column=1)
    
    tk.Label(env_window, text="Humidity (%):").grid(row=1, column=0)
    hum_entry = tk.Entry(env_window)
    hum_entry.insert(0, "50")  # Default value
    hum_entry.grid(row=1, column=1)
    
    tk.Button(env_window, text="OK", command=submit).grid(row=2, columnspan=2)
    env_window.wait_window()
    
    return env_values['temp'], env_values['hum']
   
# Sensor setup
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
ens = adafruit_ens160.ENS160(i2c)


# Ask user for Temperature and Humidity
user_temp, user_hum = get_enviroment_conditions()

# Apply Temperature and Humidity
ens.temperature_compensation = user_temp
ens.humidity_compensation = user_hum

# Lists to store time, eCO2 and TVOC values
time_values = []
eCO2_values = []
TVOC_values = [] 
start_time = time.time()  # Capture the starting time
marker_time = None # button
collecting = True # Controls data collection
running = True # Controls main loop

# Keyboard shortcut handler
def on_key_press(event):
    if event.key ==' ':
        marker_event(event)
      

# Button: Initial Time
def marker_event(event):
    global marker_time
    marker_time = time.time() - start_time
    print(f"Initial time defined at {marker_time:.2f} seconds")
    
# Button: Restart Reading
def restart_reading_event(event):
    global collecting, time_values, eCO2_values, TVOC_values, start_time, marker_time
    collecting = True
    time_values.clear()
    eCO2_values.clear()
    TVOC_values.clear()
    start_time = time.time()
    marker_time = None
    ax.clear()  # Clear the plot when restarting
    ax.set_title('eCO2 vs Time')
    ax.set_xlabel('Time (s)')
    print("Data collection restarted and graph reset")
    
# Button: Stop Reading
def stop_reading_event(event):
    global collecting
    collecting = False
    print("Data collection stopped")
    
# Button: Save 
def save_event(event):
    if marker_time is None:
        messagebox.showwarning("Initial Time not set", "Please press 'Initial Time' before saving the data.")
        print("Initial Time not set", "Please press 'Initial Time' before saving the data.")
        return
    save_directory = "/home/europi/Resultados"
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    filename = f"CO2_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    file_path = os.path.join(save_directory, filename)
    try:
        with open(file_path, mode = 'w', newline = '') as file:
            writer = csv.writer(file)
            writer.writerow(['Time (s)', 'eCO2 (ppm)','TVOC (ppb)']) # Header
            for t, eco2, tvoc in zip(time_values, eCO2_values, TVOC_values):
                if t >= marker_time:
                    writer.writerow([t - marker_time, eco2, tvoc])
        messagebox.showinfo("Save Successful", f"Data saved to {file_path}")
        print(f"Data saved to {file_path}")
    except Exception as e:
        messagebox.showwarning("Error saving data", f"Error saving data: {e}")
        print(f"Error saving data: {e}")

# Button: Enviroment
def ajust_env_event(event):
    try:
        new_temp, new_hum = get_enviroment_conditions()
        ens.temperature_compensation = new_temp
        ens.humidity_compensation = new_hum
        global user_temp, user_hum
        user_temp, user_hum = new_temp, new_hum
        messagebox.showinfo("New enviroment conditions set", f"Temperature: {user_temp} ºC, Humidity: {user_hum} %")
        print("New enviroment conditions set: T=", {user_temp}, "ºC, H=",{user_hum},"%")
    except Exception as e:
        messagebox.showinfo("Error", f"Failed to update ambient conditions")
        print(f"Failed to update ambient conditions: {e}")
        
# Button: Close
def close_event(event):
    global running
    answer = messagebox.askyesno ("Close Software", "Do you really want to close the software?")
    if answer:
        print("Closing the software")
        running = False
        plt.close()


# Button setup
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.35)
fig.canvas.mpl_connect('key_press_event', on_key_press)
# Initial Time setup
ax_marker = plt.axes([0.05,0.05,0.10,0.05]) # postition
btn_marker = Button(ax_marker, 'Initial Time',color='lightgray', hovercolor='lightblue')
btn_marker.on_clicked(marker_event)
# Restart setup
ax_restart = plt.axes([0.20,0.05,0.10,0.05])
btn_restart = Button(ax_restart, 'Restart', color='lightgray', hovercolor='lightblue')
btn_restart.on_clicked(restart_reading_event)
# Stop setup
ax_stop = plt.axes([0.35,0.05,0.10,0.05])
btn_stop = Button(ax_stop, 'Stop', color='lightgray', hovercolor='lightblue')
btn_stop.on_clicked(stop_reading_event)
# Save setup
ax_save = plt.axes([0.50,0.05,0.10,0.05])
btn_save = Button(ax_save, 'Save Results',color='lightgray', hovercolor='lightblue')
btn_save.on_clicked(save_event)
# Enviroment setup
ax_env = plt.axes([0.65,0.05,0.10,0.05])
btn_env = Button(ax_env, 'New T(ÂºC) and H(%)', color='lightgray', hovercolor='lightblue')
btn_env.on_clicked(ajust_env_event)
# Close setup
ax_close = plt.axes([0.80,0.05,0.10,0.05])
btn_close = Button(ax_close, 'Exit',color='lightgray', hovercolor='red')
btn_close.on_clicked(close_event)
# Resize the graph
manager = plt.get_current_fig_manager()
try:
    manager.resize(1920, 1080)  
except Exception as e:
    print(f"Error: {e}")

            
# main loop
while running:
    if collecting:
        # Capture the current time and eCO2 reading
        elapsed_time = time.time() - start_time
        eCO2 = ens.eCO2
        TVOC = ens.TVOC

        # Append the current time and eCO2 value to the lists
        time_values.append(elapsed_time)
        eCO2_values.append(eCO2)
        TVOC_values.append(TVOC)

        # Print the eCO2 value (optional)
        print(f"Time: {elapsed_time:.2f}s, eCO2 (ppm): {eCO2}")

    # Plot the graph
    ax.clear()
    ax.plot(time_values, eCO2_values, label = 'eCO2 (ppm)')
    ax.plot(time_values, TVOC_values, label = 'TVOC (ppb)')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('ppm')
    ax.set_title('eCO2 vs Time')
    ax.text(0.20, 0.90, f"Temperature: {user_temp:.1f} ÂºC | Humidity: {user_hum:.1f} %",
                   transform=ax.transAxes, ha='right', fontsize=10, bbox=dict(boxstyle="round", fc="w"))
    
    if marker_time is not None:
        ax.axvline(marker_time, color = 'red', linestyle = '--', label = 'Initial Time')
              
    ax.legend()
    plt.pause(0.5)
