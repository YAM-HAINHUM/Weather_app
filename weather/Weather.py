import tkinter as tk
import requests
from tkinter import messagebox

def get_weather(api_key, location):
    """Fetch weather data from OpenWeatherMap API for the specified location."""
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': location,
        'appid': api_key,
        'units': 'metric'  # Use 'imperial' for Fahrenheit
    }
    response = requests.get(base_url, params=params)  # Make a GET request to the API
    return response.json()  # Return the JSON response

def display_weather(data):
    """Display the weather information in the GUI."""
    if data.get("cod") != 200:  # Check if the response is successful
        messagebox.showerror("Error", data.get("message"))  # Show error message
        return

    # Extract relevant data from the response
    city = data["name"]
    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    weather_description = data["weather"][0]["description"]

    # Update the labels with the weather information
    city_label.config(text=f"City: {city}")
    temperature_label.config(text=f"Temperature: {temperature}°C")
    humidity_label.config(text=f"Humidity: {humidity}%")
    conditions_label.config(text=f"Conditions: {weather_description.capitalize()}")

def on_get_weather():
    """Handle the button click to get weather data."""
    location = location_entry.get()  # Get user input for location
    if not location:
        messagebox.showwarning("Input Error", "Please enter a city name or ZIP code.")
        return
    api_key = "3146cecf414d4adc3c7327074abe7947"  # 🔐 Replace with your actual API key
    weather_data = get_weather(api_key, location)  # Fetch weather data
    display_weather(weather_data)  # Display the weather information

# Create the main window
root = tk.Tk()
root.title("Weather App")

# Create and place labels and entry fields
tk.Label(root, text="Enter city name or ZIP code:").pack(pady=10)
location_entry = tk.Entry(root)
location_entry.pack(pady=5)

# Create and place the Get Weather button
get_weather_button = tk.Button(root, text="Get Weather", command=on_get_weather)
get_weather_button.pack(pady=10)

# Labels to display the weather information
city_label = tk.Label(root, text="")
city_label.pack(pady=5)

temperature_label = tk.Label(root, text="")
temperature_label.pack(pady=5)

humidity_label = tk.Label(root, text="")
humidity_label.pack(pady=5)

conditions_label = tk.Label(root, text="")
conditions_label.pack(pady=5)

# Run the application
root.mainloop()
