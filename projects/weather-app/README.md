# Weather App

A Python application that fetches weather data from the OpenWeatherMap API and displays it in a user-friendly format.

## Features
- Fetch current weather data for any city
- Display temperature, humidity, wind speed, and weather conditions
- Uses metric units (Celsius)
- Simple command-line interface

## Prerequisites
- Python 3.x
- Free OpenWeatherMap API key

## Setup
1. Get a free API key from [OpenWeatherMap](https://openweathermap.org/api)
2. Replace `your_api_key_here` in `main.py` with your actual API key
3. Install required packages:
   ```bash
   pip install requests
   ```

## How to Run
```bash
python main.py
```

## Usage
- Run the application
- Choose option 1 to get weather for a city
- Enter the city name when prompted
- View the weather information displayed

## API Information
This app uses the OpenWeatherMap Current Weather Data API:
- Endpoint: `api.openweathermap.org/data/2.5/weather`
- Free tier: 60 calls per minute
- Requires API key registration
