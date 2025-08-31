# Weather API

A simple RESTful weather API built with Go that provides simulated weather data for various cities.

## Features

- Get weather data for individual cities
- Health check endpoint
- CORS support for cross-origin requests
- Random weather generation with city-specific patterns
- JSON response format

## API Endpoints

### Get Weather for a City
```
GET /api/weather/{city}
```

Example:
```bash
curl http://localhost:8080/api/weather/london
```

Response:
```json
{
  "city": "london",
  "temperature": 18.5,
  "humidity": 45,
  "conditions": "Cloudy"
}
```

### Health Check
```
GET /health
```

Example:
```bash
curl http://localhost:8080/health
```

Response:
```json
{
  "status": "healthy"
}
```

## Supported Cities

The API supports weather generation for the following cities with different base temperature patterns:
- london (15°C base)
- newyork (18°C base) 
- tokyo (22°C base)
- sydney (25°C base)
- moscow (10°C base)
- Other cities (20°C base)

## Weather Conditions

Weather conditions are determined based on temperature and humidity:
- Below 0°C: Snow
- 0-10°C: Cold
- Humidity > 70%: Rain
- Humidity > 50%: Cloudy
- Otherwise: Sunny

## Installation and Setup

1. Make sure you have Go installed (version 1.16+ recommended)
2. Clone or navigate to the project directory
3. Run the server:

```bash
go run main.go
```

The server will start on `http://localhost:8080`

## Usage Examples

### Get weather for London
```bash
curl http://localhost:8080/api/weather/london
```

### Health check
```bash
curl http://localhost:8080/health
```

## Development

The API is built with standard Go libraries:
- `net/http` for HTTP server
- `encoding/json` for JSON handling
- `math/rand` for random weather generation

## License

This project is part of a learning exercise and is available for educational purposes.
