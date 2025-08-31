package main

import (
	"encoding/json"
	"fmt"
	"math/rand"
	"net/http"
	"os"
	"strings"
	"sync"
	"time"
)

type WeatherData struct {
	City        string    `json:"city"`
	Temperature float64   `json:"temperature"`
	Humidity    int       `json:"humidity"`
	WindSpeed   float64   `json:"wind_speed"`
	Conditions  string    `json:"conditions"`
	Timestamp   time.Time `json:"timestamp"`
}

type WeatherAPI struct {
	cache      map[string]WeatherData
	cacheMutex sync.RWMutex
}

func NewWeatherAPI() *WeatherAPI {
	return &WeatherAPI{
		cache: make(map[string]WeatherData),
	}
}

func (wa *WeatherAPI) GetWeather(city string) WeatherData {
	wa.cacheMutex.RLock()
	cached, exists := wa.cache[city]
	wa.cacheMutex.RUnlock()

	// Return cached data if it's less than 5 minutes old
	if exists && time.Since(cached.Timestamp) < 5*time.Minute {
		return cached
	}

	// Generate random weather data (simulating API call)
	weather := wa.generateWeatherData(city)

	wa.cacheMutex.Lock()
	wa.cache[city] = weather
	wa.cacheMutex.Unlock()

	return weather
}

func (wa *WeatherAPI) generateWeatherData(city string) WeatherData {
	// Simulate different weather patterns based on city
	rand.New(rand.NewSource(time.Now().UnixNano()))

	// Base temperature varies by city (simulating different climates)
	baseTemp := 20.0
	switch city {
	case "london":
		baseTemp = 15.0
	case "newyork":
		baseTemp = 18.0
	case "tokyo":
		baseTemp = 22.0
	case "sydney":
		baseTemp = 25.0
	case "moscow":
		baseTemp = 10.0
	}

	// Add some randomness
	temperature := baseTemp + rand.Float64()*10 - 5
	humidity := 40 + rand.Intn(40)
	windSpeed := 5.0 + rand.Float64()*15

	// Determine weather conditions based on temperature and humidity
	var conditions string
	switch {
	case temperature < 0:
		conditions = "Snow"
	case temperature < 10:
		conditions = "Cold"
	case humidity > 70:
		conditions = "Rain"
	case humidity > 50:
		conditions = "Cloudy"
	default:
		conditions = "Sunny"
	}

	return WeatherData{
		City:        city,
		Temperature: temperature,
		Humidity:    humidity,
		WindSpeed:   windSpeed,
		Conditions:  conditions,
		Timestamp:   time.Now(),
	}
}

func (wa *WeatherAPI) GetCachedCities() []string {
	wa.cacheMutex.RLock()
	defer wa.cacheMutex.RUnlock()

	cities := make([]string, 0, len(wa.cache))
	for city := range wa.cache {
		cities = append(cities, city)
	}
	return cities
}

func main() {
	weatherAPI := NewWeatherAPI()

	// API endpoints
	http.HandleFunc("/api/weather/", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "GET, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type")

		if r.Method == http.MethodOptions {
			w.WriteHeader(http.StatusOK)
			return
		}

		if r.Method != http.MethodGet {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		city := r.URL.Path[len("/api/weather/"):]
		if city == "" {
			http.Error(w, "City name required", http.StatusBadRequest)
			return
		}

		weather := weatherAPI.GetWeather(city)
		json.NewEncoder(w).Encode(weather)
	})

	http.HandleFunc("/api/weather", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "GET, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type")

		if r.Method == http.MethodOptions {
			w.WriteHeader(http.StatusOK)
			return
		}

		if r.Method != http.MethodGet {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		// Get multiple cities from query parameter
		citiesParam := r.URL.Query().Get("cities")
		if citiesParam == "" {
			http.Error(w, "Cities parameter required", http.StatusBadRequest)
			return
		}

		cities := strings.Split(citiesParam, ",")
		weatherData := make([]WeatherData, 0, len(cities))

		for _, city := range cities {
			city = strings.TrimSpace(city)
			if city != "" {
				weatherData = append(weatherData, weatherAPI.GetWeather(city))
			}
		}

		json.NewEncoder(w).Encode(weatherData)
	})

	http.HandleFunc("/api/cities", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.Header().Set("Access-Control-Allow-Origin", "*")

		if r.Method != http.MethodGet {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		cities := weatherAPI.GetCachedCities()
		json.NewEncoder(w).Encode(map[string]interface{}{
			"cities": cities,
			"count":  len(cities),
		})
	})

	// Health check endpoint
	http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(map[string]interface{}{
			"status":        "healthy",
			"timestamp":     time.Now().Format(time.RFC3339),
			"cached_cities": len(weatherAPI.GetCachedCities()),
		})
	})

	fmt.Println("Weather API server started on :8080")
	fmt.Println("Endpoints:")
	fmt.Println("  GET /api/weather/{city}     - Get weather for specific city")
	fmt.Println("  GET /api/weather?cities=city1,city2 - Get weather for multiple cities")
	fmt.Println("  GET /api/cities            - List all cached cities")
	fmt.Println("  GET /health               - Health check")

	err := http.ListenAndServe(":8080", nil)
	if err != nil {
		fmt.Println("Error starting server:", err)
		os.Exit(1)
	}
}
