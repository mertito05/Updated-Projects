package com.car.dashboard.service

import android.content.Context
import android.util.Log
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow

data class LaneInfo(
    val leftLaneDetected: Boolean = false,
    val rightLaneDetected: Boolean = false,
    val centerOffset: Float = 0f, // -1.0 (left) to +1.0 (right)
    val laneWidth: Float = 3.5f, // Standard lane width in meters
    val confidence: Float = 0f
)

data class VehicleState(
    val speed: Float = 0f, // km/h
    val steeringAngle: Float = 0f, // degrees
    val acceleration: Float = 0f, // m/s²
    val yawRate: Float = 0f, // degrees per second
    val timestamp: Long = System.currentTimeMillis()
)

data class TrafficObject(
    val type: TrafficObjectType,
    val distance: Float, // meters
    val relativeSpeed: Float, // m/s
    val bearing: Float, // degrees
    val confidence: Float = 0f
)

enum class TrafficObjectType {
    VEHICLE, PEDESTRIAN, BICYCLE, OBSTACLE, UNKNOWN
}

enum class AutopilotMode {
    DISABLED, LANE_KEEP, ADAPTIVE_CRUISE, FULL_AUTONOMY, EMERGENCY
}

enum class AutopilotStatus {
    READY, ACTIVE, WARNING, ERROR, DISENGAGED
}

class AutopilotService private constructor(context: Context) {
    
    private val context: Context = context.applicationContext
    
    private val _autopilotMode = MutableStateFlow(AutopilotMode.DISABLED)
    val autopilotMode: StateFlow<AutopilotMode> = _autopilotMode
    
    private val _autopilotStatus = MutableStateFlow(AutopilotStatus.READY)
    val autopilotStatus: StateFlow<AutopilotStatus> = _autopilotStatus
    
    private val _laneInfo = MutableStateFlow(LaneInfo())
    val laneInfo: StateFlow<LaneInfo> = _laneInfo
    
    private val _vehicleState = MutableStateFlow(VehicleState())
    val vehicleState: StateFlow<VehicleState> = _vehicleState
    
    private val _trafficObjects = MutableStateFlow<List<TrafficObject>>(emptyList())
    val trafficObjects: StateFlow<List<TrafficObject>> = _trafficObjects
    
    private val _targetSpeed = MutableStateFlow(80f) // km/h
    val targetSpeed: StateFlow<Float> = _targetSpeed
    
    private val _followingDistance = MutableStateFlow(2.0f) // seconds
    val followingDistance: StateFlow<Float> = _followingDistance
    
    init {
        // Initialize with default values
        Log.d("AutopilotService", "Autopilot service initialized")
    }
    
    fun enableAutopilot(mode: AutopilotMode = AutopilotMode.LANE_KEEP) {
        if (_autopilotStatus.value == AutopilotStatus.ERROR) {
            Log.w("AutopilotService", "Cannot enable autopilot - system in error state")
            return
        }
        
        _autopilotMode.value = mode
        _autopilotStatus.value = AutopilotStatus.ACTIVE
        Log.i("AutopilotService", "Autopilot enabled in mode: $mode")
    }
    
    fun disableAutopilot() {
        _autopilotMode.value = AutopilotMode.DISABLED
        _autopilotStatus.value = AutopilotStatus.READY
        Log.i("AutopilotService", "Autopilot disabled")
    }
    
    fun setTargetSpeed(speed: Float) {
        _targetSpeed.value = speed.coerceIn(30f, 130f) // Limit to reasonable speeds
        Log.d("AutopilotService", "Target speed set to: ${_targetSpeed.value} km/h")
    }
    
    fun setFollowingDistance(distance: Float) {
        _followingDistance.value = distance.coerceIn(1.0f, 4.0f) // 1-4 seconds
        Log.d("AutopilotService", "Following distance set to: ${_followingDistance.value} seconds")
    }
    
    fun updateLaneInfo(laneInfo: LaneInfo) {
        _laneInfo.value = laneInfo
        if (_autopilotMode.value != AutopilotMode.DISABLED) {
            performLaneKeeping()
        }
    }
    
    fun updateVehicleState(vehicleState: VehicleState) {
        _vehicleState.value = vehicleState
        if (_autopilotMode.value != AutopilotMode.DISABLED) {
            performSpeedControl()
        }
    }
    
    fun updateTrafficObjects(objects: List<TrafficObject>) {
        _trafficObjects.value = objects
        if (_autopilotMode.value != AutopilotMode.DISABLED) {
            performCollisionAvoidance()
        }
    }
    
    private fun performLaneKeeping() {
        val laneInfo = _laneInfo.value
        val vehicleState = _vehicleState.value
        
        if (laneInfo.leftLaneDetected && laneInfo.rightLaneDetected) {
            // Center the vehicle in the lane
            val steeringCorrection = calculateSteeringCorrection(laneInfo.centerOffset)
            Log.d("AutopilotService", "Lane keeping - steering correction: $steeringCorrection°")
            
            // Apply steering correction (in real implementation, this would control the steering)
            applySteering(steeringCorrection)
        } else {
            Log.w("AutopilotService", "Lane markings not detected clearly")
        }
    }
    
    private fun performSpeedControl() {
        val vehicleState = _vehicleState.value
        val targetSpeed = _targetSpeed.value
        
        if (vehicleState.speed < targetSpeed - 5) {
            // Accelerate to reach target speed
            val acceleration = calculateAcceleration(vehicleState.speed, targetSpeed)
            Log.d("AutopilotService", "Accelerating: $acceleration m/s²")
        } else if (vehicleState.speed > targetSpeed + 5) {
            // Decelerate to reach target speed
            val deceleration = calculateDeceleration(vehicleState.speed, targetSpeed)
            Log.d("AutopilotService", "Decelerating: $deceleration m/s²")
        }
    }
    
    private fun performCollisionAvoidance() {
        val trafficObjects = _trafficObjects.value
        val vehicleState = _vehicleState.value
        
        // Check for immediate collision threats
        val criticalObjects = trafficObjects.filter { 
            it.distance < 50f && it.relativeSpeed < -5f // Objects within 50m closing quickly
        }
        
        if (criticalObjects.isNotEmpty()) {
            Log.w("AutopilotService", "Collision threat detected! Objects: $criticalObjects")
            
            // Emergency braking or evasive maneuver
            if (_autopilotMode.value == AutopilotMode.FULL_AUTONOMY) {
                performEmergencyManeuver(criticalObjects)
            } else {
                // Alert driver to take control
                _autopilotStatus.value = AutopilotStatus.WARNING
                Log.w("AutopilotService", "Driver intervention required!")
            }
        }
    }
    
    private fun calculateSteeringCorrection(centerOffset: Float): Float {
        // Proportional control for lane centering
        return centerOffset * 5f // Scale factor for steering correction
    }
    
    private fun calculateAcceleration(currentSpeed: Float, targetSpeed: Float): Float {
        val speedDifference = targetSpeed - currentSpeed
        return (speedDifference / 10f).coerceIn(0.5f, 3.0f) // Gentle acceleration
    }
    
    private fun calculateDeceleration(currentSpeed: Float, targetSpeed: Float): Float {
        val speedDifference = currentSpeed - targetSpeed
        return (speedDifference / 8f).coerceIn(-3.0f, -0.5f) // Gentle deceleration
    }
    
    private fun applySteering(angle: Float) {
        // In real implementation, this would interface with vehicle's steering system
        Log.d("AutopilotService", "Applying steering angle: $angle°")
    }
    
    private fun performEmergencyManeuver(threats: List<TrafficObject>) {
        Log.e("AutopilotService", "EMERGENCY: Performing evasive maneuver!")
        _autopilotStatus.value = AutopilotStatus.EMERGENCY
        
        // Emergency braking and/or steering avoidance
        // This would interface with vehicle's braking and steering systems
        
        // After emergency maneuver, disengage autopilot
        disableAutopilot()
    }
    
    fun getAutopilotStatusMessage(): String {
        return when (_autopilotStatus.value) {
            AutopilotStatus.READY -> "Autopilot Ready"
            AutopilotStatus.ACTIVE -> "Autopilot Active (${_autopilotMode.value})"
            AutopilotStatus.WARNING -> "Warning: Intervention Required"
            AutopilotStatus.ERROR -> "Autopilot System Error"
            AutopilotStatus.DISENGAGED -> "Autopilot Disengaged"
        }
    }
    
    fun simulateSensorData() {
        // Simulate sensor data for testing
        val simulatedLaneInfo = LaneInfo(
            leftLaneDetected = true,
            rightLaneDetected = true,
            centerOffset = 0.1f,
            laneWidth = 3.5f,
            confidence = 0.9f
        )
        updateLaneInfo(simulatedLaneInfo)
        
        val simulatedVehicleState = VehicleState(
            speed = 80f,
            steeringAngle = 2.0f,
            acceleration = 0.2f,
            yawRate = 0.5f
        )
        updateVehicleState(simulatedVehicleState)
        
        val simulatedObjects = listOf(
            TrafficObject(TrafficObjectType.VEHICLE, 120f, -5f, -10f, 0.8f)
        )
        updateTrafficObjects(simulatedObjects)
    }
    
    companion object {
        @SuppressLint("StaticFieldLeak")
        private var instance: AutopilotService? = null
        
        fun initialize(context: Context): AutopilotService {
            if (instance == null) {
                instance = AutopilotService(context.applicationContext)
            }
            return instance!!
        }
        
        fun getInstance(): AutopilotService? {
            return instance
        }
    }
}
