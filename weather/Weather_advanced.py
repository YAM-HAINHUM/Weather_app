import tkinter as tk
from tkinter import ttk, messagebox
import requests
import geocoder
from PIL import Image, ImageTk
import io

API_KEY = "3146cecf414d4adc3c7327074abe7947"  # Replace with your actual API key


def get_weather(api_key, location):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': location,
        'appid': api_key,
        'units': 'metric'
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

    # Show weather icon
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
    units = 'metric' if unit_var.get() == 'Celsius' else 'imperial'
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


# GUI Setup
root = tk.Tk()
root.title("Advanced Weather App")
root.geometry("350x400")

# Location Input
tk.Label(root, text="Enter City or ZIP:").pack(pady=5)
location_entry = tk.Entry(root)
location_entry.pack(pady=5)

# Unit Selector
unit_var = tk.StringVar(value='Celsius')
unit_frame = tk.Frame(root)
unit_frame.pack(pady=5)
tk.Label(unit_frame, text="Temperature Unit:").pack(side='left')
ttk.Combobox(unit_frame, textvariable=unit_var, values=["Celsius", "Fahrenheit"], state='readonly', width=10).pack(side='left')

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)
tk.Button(btn_frame, text="Get Weather", command=on_get_weather).pack(side='left', padx=5)
tk.Button(btn_frame, text="Use My Location", command=detect_location).pack(side='left')

# Weather Info Labels
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

root.mainloop()
