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
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.CarRental
import androidx.compose.material.icons.filled.Directions
import androidx.compose.material.icons.filled.Error
import androidx.compose.material.icons.filled.Speed
import androidx.compose.material.icons.filled.Warning
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Slider
import androidx.compose.material3.Surface
import androidx.compose.material3.Switch
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
import com.car.dashboard.service.AutopilotMode
import com.car.dashboard.service.AutopilotService
import com.car.dashboard.service.AutopilotStatus
import com.car.dashboard.service.LaneInfo
import com.car.dashboard.service.TrafficObject
import com.car.dashboard.service.TrafficObjectType
import com.car.dashboard.service.VehicleState
import com.car.dashboard.ui.components.CarOutline
import com.car.dashboard.ui.theme.Typography

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AutopilotScreen() {
    val autopilotService = AutopilotService.getInstance()
    val autopilotMode = autopilotService?.autopilotMode?.value ?: AutopilotMode.DISABLED
    val autopilotStatus = autopilotService?.autopilotStatus?.value ?: AutopilotStatus.READY
    val laneInfo = autopilotService?.laneInfo?.value ?: LaneInfo()
    val vehicleState = autopilotService?.vehicleState?.value ?: VehicleState()
    val trafficObjects = autopilotService?.trafficObjects?.value ?: emptyList()
    val targetSpeed = autopilotService?.targetSpeed?.value ?: 80f
    val followingDistance = autopilotService?.followingDistance?.value ?: 2.0f

    var currentTargetSpeed by remember { mutableStateOf(targetSpeed) }
    var currentFollowingDistance by remember { mutableStateOf(followingDistance) }
    var isSimulationEnabled by remember { mutableStateOf(false) }

    LaunchedEffect(targetSpeed) {
        currentTargetSpeed = targetSpeed
    }

    LaunchedEffect(followingDistance) {
        currentFollowingDistance = followingDistance
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Autopilot System") }
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
                // Autopilot status
                AutopilotStatusCard(autopilotStatus, autopilotMode)
                
                // Mode selection and controls
                AutopilotControls(
                    autopilotService = autopilotService,
                    autopilotMode = autopilotMode,
                    targetSpeed = currentTargetSpeed,
                    followingDistance = currentFollowingDistance,
                    onTargetSpeedChange = { speed ->
                        currentTargetSpeed = speed
                        autopilotService?.setTargetSpeed(speed)
                    },
                    onFollowingDistanceChange = { distance ->
                        currentFollowingDistance = distance
                        autopilotService?.setFollowingDistance(distance)
                    }
                )
                
                // Simulation toggle
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    Switch(
                        checked = isSimulationEnabled,
                        onCheckedChange = { enabled ->
                            isSimulationEnabled = enabled
                            if (enabled) {
                                autopilotService?.simulateSensorData()
                            }
                        }
                    )
                    Text("Enable Simulation")
                }
            }

            // Visualization area
            AutopilotVisualization(
                laneInfo = laneInfo,
                vehicleState = vehicleState,
                trafficObjects = trafficObjects,
                autopilotMode = autopilotMode
            )

            // Detailed information
            AutopilotInformation(
                vehicleState = vehicleState,
                laneInfo = laneInfo,
                trafficObjects = trafficObjects
            )
        }
    }
}

@Composable
private fun AutopilotStatusCard(status: AutopilotStatus, mode: AutopilotMode) {
    val (backgroundColor, textColor) = when (status) {
        AutopilotStatus.ERROR -> Color.Red to Color.White
        AutopilotStatus.WARNING -> Color(0xFFFF9800) to Color.Black
        AutopilotStatus.ACTIVE -> Color(0xFF4CAF50) to Color.White
        AutopilotStatus.READY -> Color(0xFF2196F3) to Color.White
        AutopilotStatus.DISENGAGED -> Color(0xFF9E9E9E) to Color.White
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
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    if (status == AutopilotStatus.ERROR || status == AutopilotStatus.WARNING) {
                        Icon(
                            imageVector = Icons.Default.Warning,
                            contentDescription = "Warning",
                            tint = textColor
                        )
                    }
                    Text(
                        text = when (status) {
                            AutopilotStatus.ERROR -> "SYSTEM ERROR"
                            AutopilotStatus.WARNING -> "WARNING: Intervention Required"
                            AutopilotStatus.ACTIVE -> "AUTOPILOT ACTIVE"
                            AutopilotStatus.READY -> "AUTOPILOT READY"
                            AutopilotStatus.DISENGAGED -> "AUTOPILOT DISENGAGED"
                        },
                        color = textColor,
                        fontWeight = FontWeight.Bold,
                        fontSize = 18.sp
                    )
                }
                
                if (status == AutopilotStatus.ACTIVE) {
                    Text(
                        text = "Mode: ${mode.name}",
                        color = textColor,
                        fontSize = 14.sp
                    )
                }
            }
        }
    }
}

@Composable
private fun AutopilotControls(
    autopilotService: AutopilotService?,
    autopilotMode: AutopilotMode,
    targetSpeed: Float,
    followingDistance: Float,
    onTargetSpeedChange: (Float) -> Unit,
    onFollowingDistanceChange: (Float) -> Unit
) {
    Column(
        modifier = Modifier.fillMaxWidth(),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        // Mode selection buttons
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceEvenly
        ) {
            Button(
                onClick = { autopilotService?.enableAutopilot(AutopilotMode.LANE_KEEP) },
                enabled = autopilotMode != AutopilotMode.LANE_KEEP
            ) {
                Text("Lane Keep")
            }
            
            Button(
                onClick = { autopilotService?.enableAutopilot(AutopilotMode.ADAPTIVE_CRUISE) },
                enabled = autopilotMode != AutopilotMode.ADAPTIVE_CRUISE
            ) {
                Text("Adaptive Cruise")
            }
            
            Button(
                onClick = { autopilotService?.enableAutopilot(AutopilotMode.FULL_AUTONOMY) },
                enabled = autopilotMode != AutopilotMode.FULL_AUTONOMY
            ) {
                Text("Full Autonomy")
            }
        }

        // Disable button
        Button(
            onClick = { autopilotService?.disableAutopilot() },
            modifier = Modifier.align(Alignment.CenterHorizontally),
            enabled = autopilotMode != AutopilotMode.DISABLED
        ) {
            Text("Disable Autopilot")
        }

        // Speed control
        Card(modifier = Modifier.fillMaxWidth()) {
            Column(modifier = Modifier.padding(16.dp)) {
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    Icon(Icons.Default.Speed, contentDescription = "Speed")
                    Text("Target Speed: ${targetSpeed.toInt()} km/h")
                }
                Slider(
                    value = targetSpeed,
                    onValueChange = onTargetSpeedChange,
                    valueRange = 30f..130f,
                    steps = 19
                )
            }
        }

        // Following distance
        Card(modifier = Modifier.fillMaxWidth()) {
            Column(modifier = Modifier.padding(16.dp)) {
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    Icon(Icons.Default.Directions, contentDescription = "Distance")
                    Text("Following Distance: ${"%.1f".format(followingDistance)} s")
                }
                Slider(
                    value = followingDistance,
                    onValueChange = onFollowingDistanceChange,
                    valueRange = 1f..4f,
                    steps = 5
                )
            }
        }
    }
}

@Composable
private fun AutopilotVisualization(
    laneInfo: LaneInfo,
    vehicleState: VehicleState,
    trafficObjects: List<TrafficObject>,
    autopilotMode: AutopilotMode
) {
    Box(
        modifier = Modifier
            .size(350.dp)
            .padding(16.dp)
            .background(Color(0xFF2C3E50), RoundedCornerShape(16.dp)),
        contentAlignment = Alignment.Center
    ) {
        // Road visualization
        RoadVisualization(laneInfo)
        
        // Car visualization
        CarOutline(
            modifier = Modifier
                .size(100.dp)
                .align(Alignment.Center)
        )
        
        // Traffic objects
        TrafficObjectsVisualization(trafficObjects)
        
        // Status overlay
        Box(
            modifier = Modifier
                .align(Alignment.TopEnd)
                .padding(8.dp)
                .background(Color.Black.copy(alpha = 0.7f), RoundedCornerShape(8.dp))
                .padding(4.dp)
        ) {
            Text(
                text = "${vehicleState.speed.toInt()} km/h",
                color = Color.White,
                fontSize = 14.sp
            )
        }
    }
}

@Composable
private fun RoadVisualization(laneInfo: LaneInfo) {
    // Simplified road visualization with lane markings
    Column(
        modifier = Modifier.fillMaxSize(),
        verticalArrangement = Arrangement.SpaceEvenly
    ) {
        // Lane markings
        repeat(3) {
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(2.dp)
                    .background(Color.Yellow.copy(alpha = 0.7f))
            )
            Spacer(modifier = Modifier.height(40.dp))
        }
    }
}

@Composable
private fun TrafficObjectsVisualization(trafficObjects: List<TrafficObject>) {
    trafficObjects.forEach { obj ->
        val position = calculateObjectPosition(obj)
        val color = when (obj.type) {
            TrafficObjectType.VEHICLE -> Color.Red
            TrafficObjectType.PEDESTRIAN -> Color.Yellow
            TrafficObjectType.BICYCLE -> Color.Green
            TrafficObjectType.OBSTACLE -> Color(0xFF8B4513)
            TrafficObjectType.UNKNOWN -> Color.Gray
        }
        
        Box(
            modifier = Modifier
                .align(position)
                .size(20.dp)
                .background(color, CircleShape)
        )
    }
}

@Composable
private fun AutopilotInformation(
    vehicleState: VehicleState,
    laneInfo: LaneInfo,
    trafficObjects: List<TrafficObject>
) {
    Column(
        modifier = Modifier.fillMaxWidth(),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        // Vehicle state
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceEvenly) {
            InfoItem("Speed", "${vehicleState.speed.toInt()} km/h")
            InfoItem("Steering", "${"%.1f".format(vehicleState.steeringAngle)}°")
            InfoItem("Accel", "${"%.1f".format(vehicleState.acceleration)} m/s²")
        }
        
        // Lane info
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceEvenly) {
            InfoItem("Left Lane", if (laneInfo.leftLaneDetected) "Detected" else "Not detected")
            InfoItem("Right Lane", if (laneInfo.rightLaneDetected) "Detected" else "Not detected")
            InfoItem("Offset", "${"%.2f".format(laneInfo.centerOffset)}")
        }
        
        // Traffic objects
        if (trafficObjects.isNotEmpty()) {
            Text(
                text = "Detected Objects: ${trafficObjects.size}",
                style = Typography.labelMedium,
                modifier = Modifier.align(Alignment.CenterHorizontally)
            )
        }
    }
}

@Composable
private fun InfoItem(label: String, value: String) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Text(text = label, style = Typography.labelSmall)
        Text(text = value, style = Typography.bodySmall.copy(fontWeight = FontWeight.Bold))
    }
}

private fun calculateObjectPosition(obj: TrafficObject): Alignment {
    // Simplified position calculation based on bearing and distance
    val x = (obj.bearing / 90f).coerceIn(-1f, 1f)
    val y = (1f - (obj.distance
