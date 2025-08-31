package com.car.dashboard.ui.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.LocationOn
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material.icons.filled.WbSunny
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.navigation.NavHostController

data class WeatherData(
    val location: String,
    val temperature: Double,
    val condition: String,
    val humidity: Int,
    val windSpeed: Double,
    val feelsLike: Double,
    val high: Double,
    val low: Double
)

data class HourlyForecast(
    val time: String,
    val temperature: Double,
    val condition: String,
    val precipitation: Int
)

data class DailyForecast(
    val day: String,
    val high: Double,
    val low: Double,
    val condition: String,
    val precipitation: Int
)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun WeatherScreen(navController: NavHostController) {
    val isLoading = remember { mutableStateOf(false) }
    val currentLocation = remember { mutableStateOf("Current Location") }
    
    val weatherData = WeatherData(
        location = "New York, NY",
        temperature = 72.5,
        condition = "Sunny",
        humidity = 65,
        windSpeed = 8.2,
        feelsLike = 75.0,
        high = 78.0,
        low = 65.0
    )
    
    val hourlyForecast = listOf(
        HourlyForecast("Now", 72.5, "Sunny", 0),
        HourlyForecast("1 PM", 74.0, "Sunny", 0),
        HourlyForecast("2 PM", 75.5, "Partly Cloudy", 0),
        HourlyForecast("3 PM", 76.0, "Partly Cloudy", 0),
        HourlyForecast("4 PM", 75.0, "Cloudy", 10),
        HourlyForecast("5 PM", 73.0, "Cloudy", 20),
        HourlyForecast("6 PM", 70.0, "Rain", 60),
        HourlyForecast("7 PM", 68.0, "Rain", 70)
    )
    
    val dailyForecast = listOf(
        DailyForecast("Today", 78.0, 65.0, "Sunny", 0),
        DailyForecast("Tomorrow", 76.0, 64.0, "Partly Cloudy", 10),
        DailyForecast("Wed", 72.0, 62.0, "Rain", 70),
        DailyForecast("Thu", 74.0, 63.0, "Cloudy", 30),
        DailyForecast("Fri", 77.0, 65.0, "Sunny", 0),
        DailyForecast("Sat", 79.0, 67.0, "Sunny", 0),
        DailyForecast("Sun", 81.0, 69.0, "Sunny", 0)
    )

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        // Header with back button and refresh
        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            IconButton(
                onClick = { navController.popBackStack() }
            ) {
                Icon(
                    imageVector = Icons.Default.ArrowBack,
                    contentDescription = "Back"
                )
            }
            Spacer(modifier = Modifier.width(8.dp))
            Text(
                text = "Weather",
                style = MaterialTheme.typography.headlineMedium,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.weight(1f))
            IconButton(
                onClick = { /* Refresh weather */ isLoading.value = true }
            ) {
                if (isLoading.value) {
                    CircularProgressIndicator(
                        modifier = Modifier.size(24.dp),
                        strokeWidth = 2.dp
                    )
                } else {
                    Icon(
                        imageVector = Icons.Default.Refresh,
                        contentDescription = "Refresh"
                    )
                }
            }
        }

        Spacer(modifier = Modifier.height(24.dp))

        // Current weather
        Card(
            colors = CardDefaults.cardColors(
                containerColor = MaterialTheme.colorScheme.primaryContainer
            ),
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(
                modifier = Modifier.padding(24.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.Center
                ) {
                    Icon(
                        imageVector = Icons.Default.LocationOn,
                        contentDescription = "Location",
                        modifier = Modifier.size(20.dp)
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    Text(
                        text = weatherData.location,
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.Bold
                    )
                }
                
                Spacer(modifier = Modifier.height(16.dp))
                
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.Center
                ) {
                    Icon(
                        imageVector = Icons.Default.WbSunny,
                        contentDescription = weatherData.condition,
                        modifier = Modifier.size(48.dp)
                    )
                    Spacer(modifier = Modifier.width(16.dp))
                    Text(
                        text = "${weatherData.temperature}°F",
                        style = MaterialTheme.typography.displaySmall,
                        fontWeight = FontWeight.Bold
                    )
                }
                
                Text(
                    text = weatherData.condition,
                    style = MaterialTheme.typography.titleMedium
                )
                
                Spacer(modifier = Modifier.height(16.dp))
                
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceEvenly
                ) {
                    WeatherDetail("Feels like", "${weatherData.feelsLike}°F")
                    WeatherDetail("Humidity", "${weatherData.humidity}%")
                    WeatherDetail("Wind", "${weatherData.windSpeed} mph")
                }
                
                Spacer(modifier = Modifier.height(16.dp))
                
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceEvenly
                ) {
                    WeatherDetail("High", "${weatherData.high}°F")
                    WeatherDetail("Low", "${weatherData.low}°F")
                }
            }
        }

        Spacer(modifier = Modifier.height(24.dp))

        // Hourly forecast
        Text(
            text = "Hourly Forecast",
            style = MaterialTheme.typography.titleLarge,
            fontWeight = FontWeight.Bold
        )
        
        Spacer(modifier = Modifier.height(8.dp))
        
        LazyRow(
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            items(hourlyForecast) { hour ->
                HourlyForecastCard(hour)
            }
        }

        Spacer(modifier = Modifier.height(24.dp))

        // Daily forecast
        Text(
            text = "7-Day Forecast",
            style = MaterialTheme.typography.titleLarge,
            fontWeight = FontWeight.Bold
        )
        
        Spacer(modifier = Modifier.height(8.dp))
        
        Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
            dailyForecast.forEach { day ->
                DailyForecastCard(day)
            }
        }
    }
}

@Composable
fun WeatherDetail(label: String, value: String) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Text(
            text = label,
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f)
        )
        Text(
            text = value,
            style = MaterialTheme.typography.bodyMedium,
            fontWeight = FontWeight.Medium
        )
    }
}

@Composable
fun HourlyForecastCard(hour: HourlyForecast) {
    Card(
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surfaceVariant
        ),
        modifier = Modifier
            .width(80.dp)
            .height(120.dp)
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(8.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.SpaceAround
        ) {
            Text(
                text = hour.time,
                style = MaterialTheme.typography.bodySmall,
                fontWeight = FontWeight.Medium
            )
            Icon(
                imageVector = Icons.Default.WbSunny,
                contentDescription = hour.condition,
                modifier = Modifier.size(24.dp)
            )
            Text(
                text = "${hour.temperature}°",
                style = MaterialTheme.typography.bodyMedium,
                fontWeight = FontWeight.Bold
            )
            if (hour.precipitation > 0) {
                Text(
                    text = "${hour.precipitation}%",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.primary
                )
            }
        }
    }
}

@Composable
fun DailyForecastCard(day: DailyForecast) {
    Card(
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surfaceVariant
        ),
        modifier = Modifier.fillMaxWidth()
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Text(
                text = day.day,
                style = MaterialTheme.typography.bodyMedium,
                fontWeight = FontWeight.Medium,
                modifier = Modifier.weight(1f)
            )
            
            Icon(
                imageVector = Icons.Default.WbSunny,
                contentDescription = day.condition,
                modifier = Modifier.size(24.dp)
            )
            
            Spacer(modifier = Modifier.width(16.dp))
            
            if (day.precipitation > 0) {
                Text(
                    text = "${day.precipitation}%",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.primary,
                    modifier = Modifier.width(32.dp)
                )
            } else {
                Spacer(modifier = Modifier.width(32.dp))
            }
            
            Text(
                text = "${day.high}° / ${day.low}°",
                style = MaterialTheme.typography.bodyMedium,
                fontWeight = FontWeight.Medium
            )
        }
    }
}
