import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
import geocoder
from PIL import Image, ImageTk, ImageGrab
import io
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import random

API_KEY = "3146cecf414d4adc3c7327074abe7947"

# --------------------- Theme Setup ---------------------
themes = {
    "light": {
        "bg": "#dff6f9",
        "fg": "black",
        "button_bg": "#00bcd4",
        "button_fg": "white"
    },
    "dark": {
        "bg": "#2c3e50",
        "fg": "white",
        "button_bg": "#34495e",
        "button_fg": "white"
    }
}
current_theme = "light"

# --------------------- Weather Functions ---------------------
def get_weather(api_key, location):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': location,
        'appid': api_key,
        'units': 'metric' if unit_var.get() == 'Celsius' else 'imperial'
    }
    response = requests.get(base_url, params=params)
    return response.json()

def get_weather_icon(icon_id):
    url = f"http://openweathermap.org/img/wn/{icon_id}@2x.png"
    response = requests.get(url)
    return Image.open(io.BytesIO(response.content)) if response.status_code == 200 else None

def display_weather(data):
    if data.get("cod") != 200:
        messagebox.showerror("Error", data.get("message"))
        return

    city = data["name"]
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    desc = data["weather"][0]["description"].capitalize()
    icon_id = data["weather"][0]["icon"]

    city_label.config(text=f"City: {city}")
    temperature_label.config(text=f"Temperature: {temp}°{unit_var.get()[0]}")
    humidity_label.config(text=f"Humidity: {humidity}%")
    conditions_label.config(text=f"Conditions: {desc}")

    icon_image = get_weather_icon(icon_id)
    if icon_image:
        icon = ImageTk.PhotoImage(icon_image)
        weather_icon_label.config(image=icon)
        weather_icon_label.image = icon

def on_get_weather():
    location = location_entry.get().strip()
    if not location:
        messagebox.showwarning("Input Error", "Please enter a city name or ZIP code.")
        return
    data = get_weather(API_KEY, location)
    display_weather(data)

def detect_location():
    g = geocoder.ip('me')
    if g.ok:
        location_entry.delete(0, tk.END)
        location_entry.insert(0, g.city or g.state or "")
        on_get_weather()
    else:
        messagebox.showerror("Error", "Could not detect location.")

# --------------------- Theme ---------------------
def apply_theme():
    theme = themes[current_theme]
    root.config(bg=theme["bg"])

    def apply_to_widget(widget):
        if isinstance(widget, (tk.Label, tk.Entry, tk.Text)):
            widget.config(bg=theme["bg"], fg=theme["fg"])
        elif isinstance(widget, tk.Button):
            widget.config(bg=theme["button_bg"], fg=theme["button_fg"], activebackground=theme["button_bg"])
        elif isinstance(widget, tk.Frame):
            widget.config(bg=theme["bg"])
        for sub_widget in widget.winfo_children():
            try:
                apply_to_widget(sub_widget)
            except tk.TclError:
                continue

    for widget in root.winfo_children():
        try:
            apply_to_widget(widget)
        except tk.TclError:
            continue

def toggle_theme():
    global current_theme
    current_theme = "dark" if current_theme == "light" else "light"
    apply_theme()

# --------------------- Chart Functions ---------------------
def generate_sample_5_day_forecast():
    today = datetime.now()
    forecast = []
    for i in range(5):
        day = today + timedelta(days=i)
        forecast.append({
            "date": day.strftime("%Y-%m-%d"),
            "temperature": random.uniform(22.0, 35.0)
        })
    return forecast

def generate_sample_hourly_forecast():
    now = datetime.now()
    hourly = []
    for i in range(24):
        hour = now + timedelta(hours=i)
        hourly.append({
            "time": hour.strftime("%H:%M"),
            "temperature": random.uniform(20.0, 36.0)
        })
    return hourly

def show_5_day_forecast_chart():
    data = generate_sample_5_day_forecast()
    dates = [d['date'] for d in data]
    temps = [d['temperature'] for d in data]

    plt.figure(figsize=(8, 4))
    plt.plot(dates, temps, marker='o', linestyle='-', color='teal')
    plt.title("5-Day Temperature Forecast")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°{})".format('C' if unit_var.get() == 'Celsius' else 'F'))
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def export_chart():
    data = generate_sample_5_day_forecast()
    dates = [d['date'] for d in data]
    temps = [d['temperature'] for d in data]

    plt.figure(figsize=(8, 4))
    plt.plot(dates, temps, marker='o', linestyle='-', color='green')
    plt.title("5-Day Temperature Forecast")
    plt.xlabel("Date")
    plt.ylabel("Temperature")
    plt.grid(True)
    plt.tight_layout()

    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if file_path:
        plt.savefig(file_path)
        plt.close()
        messagebox.showinfo("Exported", f"Chart saved to:\n{file_path}")

def show_hourly_forecast_chart():
    data = generate_sample_hourly_forecast()
    times = [d['time'] for d in data]
    temps = [d['temperature'] for d in data]

    plt.figure(figsize=(10, 4))
    plt.plot(times, temps, marker='x', linestyle='--', color='purple')
    plt.title("Hourly Temperature Forecast")
    plt.xlabel("Time")
    plt.ylabel("Temperature (°{})".format('C' if unit_var.get() == 'Celsius' else 'F'))
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def save_report():
    x = root.winfo_rootx() + city_label.winfo_x()
    y = root.winfo_rooty() + city_label.winfo_y()
    w = city_label.winfo_width()
    h = conditions_label.winfo_y() + conditions_label.winfo_height() - city_label.winfo_y()
    bbox = (x, y, x + w + 100, y + h + 60)
    img = ImageGrab.grab(bbox)

    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if file_path:
        img.save(file_path)
        messagebox.showinfo("Saved", f"Report saved to:\n{file_path}")

# --------------------- GUI Setup ---------------------
root = tk.Tk()
root.title("Advanced Weather App")
root.geometry("700x550")

# Title
tk.Label(root, text="🌤 Weather Forecast", font=("Helvetica", 20, "bold")).pack(pady=5)

# City Input and ZIP Code
input_frame = tk.Frame(root)
input_frame.pack(pady=5)
location_entry = tk.Entry(input_frame, width=40)
location_entry.insert(0, "Enter city name or click Detect")
location_entry.pack(side='left', padx=10)
zip_entry = tk.Entry(input_frame, width=25)
zip_entry.insert(0, "Enter ZIP/Pin Code (optional)")
zip_entry.pack(side='right', padx=10)

# Dropdown + Radio Buttons for units
dropdown_frame = tk.Frame(root)
dropdown_frame.pack()
unit_var = tk.StringVar(value='Celsius')
unit_combo = ttk.Combobox(dropdown_frame, textvariable=unit_var, values=["Celsius", "Fahrenheit"], state='readonly', width=12)
unit_combo.pack()
radio_frame = tk.Frame(root)
radio_frame.pack()
tk.Radiobutton(radio_frame, text="Celsius", variable=unit_var, value='Celsius').pack(side='left')
tk.Radiobutton(radio_frame, text="Fahrenheit", variable=unit_var, value='Fahrenheit').pack(side='left')

# Detect & Get Weather Buttons
tk.Button(root, text="📍 Detect Location", command=detect_location, width=20).pack(pady=5)
tk.Button(root, text="🔍 Get Weather", command=on_get_weather, width=20).pack()

# Weather Info
weather_icon_label = tk.Label(root)
weather_icon_label.pack()
city_label = tk.Label(root, text="")
city_label.pack(pady=2)
temperature_label = tk.Label(root, text="")
temperature_label.pack(pady=2)
humidity_label = tk.Label(root, text="")
humidity_label.pack(pady=2)
conditions_label = tk.Label(root, text="")
conditions_label.pack(pady=2)

# 5-Day Forecast Section
forecast_frame = tk.Frame(root)
forecast_frame.pack(pady=10)
tk.Label(forecast_frame, text="🗕 5-Day Forecast", font=("Arial", 12, "bold")).pack()

btns = [
    ("✅ Show Chart", show_5_day_forecast_chart),
    ("📤 Export Chart", export_chart),
    ("⏱ Hourly Forecast", show_hourly_forecast_chart),
    ("💾 Save Report", save_report),
    ("🌓 Toggle Theme", toggle_theme)
]

for text, cmd in btns:
    tk.Button(forecast_frame, text=text, command=cmd, width=20).pack(pady=2)

# Auto Refresh Checkbox
refresh_var = tk.BooleanVar()
tk.Checkbutton(root, text="🔁 Auto Refresh (2 mins)", variable=refresh_var).pack(pady=5)

# Apply initial theme
apply_theme()

root.mainloop()
