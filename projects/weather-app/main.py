import requests
import json
import os

API_KEY = "your_api_key_here"  # Replace with your OpenWeatherMap API key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(city_name):
    """Fetch weather data for a given city"""
    try:
        params = {
            'q': city_name,
            'appid': API_KEY,
            'units': 'metric'  # Use metric units (Celsius)
        }
        
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        data = response.json()
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None
    except json.JSONDecodeError:
        print("Error parsing weather data")
        return None

def display_weather(data):
    """Display weather information in a user-friendly format"""
    if not data:
        return
    
    try:
        city = data['name']
        country = data['sys']['country']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        description = data['weather'][0]['description'].title()
        wind_speed = data['wind']['speed']
        
        print(f"\nWeather in {city}, {country}:")
        print(f"Temperature: {temp}°C (Feels like: {feels_like}°C)")
        print(f"Conditions: {description}")
        print(f"Humidity: {humidity}%")
        print(f"Wind Speed: {wind_speed} m/s")
        
    except KeyError as e:
        print(f"Unexpected data format: {e}")

def main():
    print("Weather App")
    print("===========")
    
    # Check if API key is set
    if API_KEY == "your_api_key_here":
        print("\n⚠️  Please get a free API key from OpenWeatherMap:")
        print("https://openweathermap.org/api")
        print("Replace 'your_api_key_here' in main.py with your actual API key")
        return
    
    while True:
        print("\nOptions:")
        print("1. Get weather for a city")
        print("2. Exit")
        
        choice = input("\nEnter your choice (1-2): ").strip()
        
        if choice == "1":
            city = input("Enter city name: ").strip()
            if city:
                weather_data = get_weather(city)
                if weather_data:
                    display_weather(weather_data)
                else:
                    print("Could not fetch weather data. Please try again.")
            else:
                print("Please enter a valid city name.")
        
        elif choice == "2":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
