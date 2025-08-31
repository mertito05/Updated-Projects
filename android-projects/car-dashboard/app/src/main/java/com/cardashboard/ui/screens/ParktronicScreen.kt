package com.car.dashboard.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Warning
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.car.dashboard.service.ParktronicService
import com.car.dashboard.service.ParkingAlertLevel
import com.car.dashboard.ui.components.CarOutline
import com.car.dashboard.ui.theme.Typography

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ParktronicScreen() {
    val parktronicService = ParktronicService.getInstance()
    val distances = parktronicService?.parkingDistances?.value ?: ParkingDistance()
    val alertLevel = parktronicService?.alertLevel?.value ?: ParkingAlertLevel.NONE
    val isActive = parktronicService?.isActive?.value ?: false
    
    var isEnabled by remember { mutableStateOf(isActive) }

    LaunchedEffect(isActive) {
        isEnabled = isActive
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Parking Assistance") }
            )
        }
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .padding(innerPadding)
                .fillMaxSize()
                .padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.SpaceBetween
        ) {
            // Status and controls
            Column(
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                // Alert status
                AlertStatus(alertLevel)
                
                // Enable/disable button
                Button(
                    onClick = {
                        isEnabled = !isEnabled
                        if (isEnabled) {
                            parktronicService?.startParkingAssistance()
                        } else {
                            parktronicService?.stopParkingAssistance()
                        }
                    }
                ) {
                    Text(if (isEnabled) "Disable Parking Assist" else "Enable Parking Assist")
                }
            }

            // Car visualization with distance indicators
            CarVisualization(distances, alertLevel)

            // Detailed distance readings
            DistanceReadings(distances)
        }
    }
}

@Composable
private fun AlertStatus(alertLevel: ParkingAlertLevel) {
    val (backgroundColor, textColor) = when (alertLevel) {
        ParkingAlertLevel.CRITICAL -> Color.Red to Color.White
        ParkingAlertLevel.DANGER -> Color(0xFFFF5252) to Color.White
        ParkingAlertLevel.WARNING -> Color(0xFFFF9800) to Color.Black
        ParkingAlertLevel.INFO -> Color(0xFF2196F3) to Color.White
        ParkingAlertLevel.NONE -> Color(0xFF4CAF50) to Color.White
    }

    Card(
        modifier = Modifier.fillMaxWidth()
    ) {
        Box(
            modifier = Modifier
                .background(backgroundColor)
                .padding(16.dp)
                .fillMaxWidth(),
            contentAlignment = Alignment.Center
        ) {
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                if (alertLevel != ParkingAlertLevel.NONE) {
                    Icon(
                        imageVector = Icons.Default.Warning,
                        contentDescription = "Warning",
                        tint = textColor
                    )
                }
                Text(
                    text = when (alertLevel) {
                        ParkingAlertLevel.CRITICAL -> "CRITICAL! STOP IMMEDIATELY"
                        ParkingAlertLevel.DANGER -> "DANGER! Very close"
                        ParkingAlertLevel.WARNING -> "WARNING! Close distance"
                        ParkingAlertLevel.INFO -> "CAUTION! Approaching obstacle"
                        ParkingAlertLevel.NONE -> "CLEAR - No obstacles detected"
                    },
                    color = textColor,
                    fontWeight = FontWeight.Bold,
                    fontSize = 18.sp
                )
            }
        }
    }
}

@Composable
private fun CarVisualization(distances: ParkingDistance, alertLevel: ParkingAlertLevel) {
    Box(
        modifier = Modifier
            .size(300.dp)
            .padding(16.dp),
        contentAlignment = Alignment.Center
    ) {
        // Car outline
        CarOutline(modifier = Modifier.size(200.dp))
        
        // Distance indicators around the car
        // Front sensors
        DistanceIndicator(
            distance = distances.frontLeft,
            alertLevel = getAlertLevelForDistance(distances.frontLeft),
            modifier = Modifier
                .align(Alignment.TopStart)
                .offset(x = (-40).dp, y = (-40).dp)
        )
        
        DistanceIndicator(
            distance = distances.frontCenter,
            alertLevel = getAlertLevelForDistance(distances.frontCenter),
            modifier = Modifier
                .align(Alignment.TopCenter)
                .offset(y = (-50).dp)
        )
        
        DistanceIndicator(
            distance = distances.frontRight,
            alertLevel = getAlertLevelForDistance(distances.frontRight),
            modifier = Modifier
                .align(Alignment.TopEnd)
                .offset(x = 40.dp, y = (-40).dp)
        )
        
        // Rear sensors
        DistanceIndicator(
            distance = distances.rearLeft,
            alertLevel = getAlertLevelForDistance(distances.rearLeft),
            modifier = Modifier
                .align(Alignment.BottomStart)
                .offset(x = (-40).dp, y = 40.dp)
        )
        
        DistanceIndicator(
            distance = distances.rearCenter,
            alertLevel = getAlertLevelForDistance(distances.rearCenter),
            modifier = Modifier
                .align(Alignment.BottomCenter)
                .offset(y = 50.dp)
        )
        
        DistanceIndicator(
            distance = distances.rearRight,
            alertLevel = getAlertLevelForDistance(distances.rearRight),
            modifier = Modifier
                .align(Alignment.BottomEnd)
                .offset(x = 40.dp, y = 40.dp)
        )
    }
}

@Composable
private fun DistanceIndicator(distance: Float, alertLevel: ParkingAlertLevel, modifier: Modifier = Modifier) {
    val color = when (alertLevel) {
        ParkingAlertLevel.CRITICAL -> Color.Red
        ParkingAlertLevel.DANGER -> Color(0xFFFF5252)
        ParkingAlertLevel.WARNING -> Color(0xFFFF9800)
        ParkingAlertLevel.INFO -> Color(0xFF2196F3)
        ParkingAlertLevel.NONE -> Color(0xFF4CAF50)
    }

    Box(
        modifier = modifier
            .size(40.dp)
            .clip(CircleShape)
            .background(color)
            .padding(4.dp),
        contentAlignment = Alignment.Center
    ) {
        Text(
            text = if (distance > 0) "%.1fm".format(distance) else "N/A",
            color = Color.White,
            fontSize = 10.sp,
            fontWeight = FontWeight.Bold,
            textAlign = TextAlign.Center
        )
    }
}

@Composable
private fun DistanceReadings(distances: ParkingDistance) {
    Column(
        modifier = Modifier.fillMaxWidth(),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Text(
            text = "Detailed Distance Readings",
            style = Typography.titleMedium,
            modifier = Modifier.align(Alignment.CenterHorizontally)
        )
        
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceEvenly) {
            DistanceReadingItem("Front Left", distances.frontLeft)
            DistanceReadingItem("Front Center", distances.frontCenter)
            DistanceReadingItem("Front Right", distances.frontRight)
        }
        
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceEvenly) {
            DistanceReadingItem("Rear Left", distances.rearLeft)
            DistanceReadingItem("Rear Center", distances.rearCenter)
            DistanceReadingItem("Rear Right", distances.rearRight)
        }
    }
}

@Composable
private fun DistanceReadingItem(label: String, distance: Float) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Text(text = label, style = Typography.labelSmall)
        Text(
            text = if (distance > 0) "%.1f m".format(distance) else "---",
            style = Typography.bodyLarge.copy(fontWeight = FontWeight.Bold),
            color = when (getAlertLevelForDistance(distance)) {
                ParkingAlertLevel.CRITICAL -> Color.Red
                ParkingAlertLevel.DANGER -> Color(0xFFFF5252)
                ParkingAlertLevel.WARNING -> Color(0xFFFF9800)
                ParkingAlertLevel.INFO -> Color(0xFF2196F3)
                ParkingAlertLevel.NONE -> Color(0xFF4CAF50)
            }
        )
    }
}

private fun getAlertLevelForDistance(distance: Float): ParkingAlertLevel {
    return when {
        distance <= 0.2f -> ParkingAlertLevel.CRITICAL
        distance <= 0.5f -> ParkingAlertLevel.DANGER
        distance <= 1.0f -> ParkingAlertLevel.WARNING
        distance <= 1.5f -> ParkingAlertLevel.INFO
        else -> ParkingAlertLevel.NONE
    }
}

private fun Modifier.offset(x: Int.dp, y: Int.dp): Modifier {
    return this then Modifier.offset(x = x, y = y)
}
