package com.car.dashboard.service

import android.annotation.SuppressLint
import android.content.Context
import android.hardware.Sensor
import android.hardware.SensorEvent
import android.hardware.SensorEventListener
import android.hardware.SensorManager
import android.util.Log
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow

data class ParkingDistance(
    val frontLeft: Float = 0f,
    val frontCenter: Float = 0f,
    val frontRight: Float = 0f,
    val rearLeft: Float = 0f,
    val rearCenter: Float = 0f,
    val rearRight: Float = 0f,
    val timestamp: Long = System.currentTimeMillis()
)

enum class ParkingAlertLevel {
    NONE, INFO, WARNING, DANGER, CRITICAL
}

class ParktronicService private constructor(context: Context) : SensorEventListener {
    
    private val context: Context = context.applicationContext
    private val sensorManager: SensorManager = context.getSystemService(Context.SENSOR_SERVICE) as SensorManager
    private val ultrasonicSensor: Sensor? = sensorManager.getDefaultSensor(Sensor.TYPE_PROXIMITY)
    
    private val _parkingDistances = MutableStateFlow(ParkingDistance())
    val parkingDistances: StateFlow<ParkingDistance> = _parkingDistances
    
    private val _alertLevel = MutableStateFlow(ParkingAlertLevel.NONE)
    val alertLevel: StateFlow<ParkingAlertLevel> = _alertLevel
    
    private val _isActive = MutableStateFlow(false)
    val isActive: StateFlow<Boolean> = _isActive
    
    private val alertThresholds = mapOf(
        ParkingAlertLevel.NONE to 2.0f,      // > 2m
        ParkingAlertLevel.INFO to 1.5f,      // 1.5m - 2m
        ParkingAlertLevel.WARNING to 1.0f,   // 1m - 1.5m
        ParkingAlertLevel.DANGER to 0.5f,    // 0.5m - 1m
        ParkingAlertLevel.CRITICAL to 0.2f   // < 0.5m
    )
    
    init {
        initializeSensors()
    }
    
    private fun initializeSensors() {
        ultrasonicSensor?.let {
            sensorManager.registerListener(this, it, SensorManager.SENSOR_DELAY_NORMAL)
        }
    }
    
    fun startParkingAssistance() {
        _isActive.value = true
        Log.d("ParktronicService", "Parking assistance started")
    }
    
    fun stopParkingAssistance() {
        _isActive.value = false
        _alertLevel.value = ParkingAlertLevel.NONE
        Log.d("ParktronicService", "Parking assistance stopped")
    }
    
    @SuppressLint("MissingPermission")
    override fun onSensorChanged(event: SensorEvent?) {
        if (!_isActive.value) return
        
        event?.let {
            if (event.sensor.type == Sensor.TYPE_PROXIMITY) {
                val distance = event.values[0]
                updateParkingDistances(distance)
                updateAlertLevel(distance)
            }
        }
    }
    
    private fun updateParkingDistances(distance: Float) {
        // Simulate multiple sensor readings (in real app, this would come from actual sensors)
        val currentDistances = _parkingDistances.value.copy(
            frontCenter = distance,
            frontLeft = distance * 0.8f,
            frontRight = distance * 0.9f,
            rearCenter = distance * 1.1f,
            rearLeft = distance * 1.2f,
            rearRight = distance * 1.3f,
            timestamp = System.currentTimeMillis()
        )
        _parkingDistances.value = currentDistances
    }
    
    private fun updateAlertLevel(distance: Float) {
        val level = when {
            distance <= alertThresholds[ParkingAlertLevel.CRITICAL]!! -> ParkingAlertLevel.CRITICAL
            distance <= alertThresholds[ParkingAlertLevel.DANGER]!! -> ParkingAlertLevel.DANGER
            distance <= alertThresholds[ParkingAlertLevel.WARNING]!! -> ParkingAlertLevel.WARNING
            distance <= alertThresholds[ParkingAlertLevel.INFO]!! -> ParkingAlertLevel.INFO
            else -> ParkingAlertLevel.NONE
        }
        _alertLevel.value = level
    }
    
    fun getAlertMessage(): String {
        return when (_alertLevel.value) {
            ParkingAlertLevel.CRITICAL -> "STOP! Critical distance!"
            ParkingAlertLevel.DANGER -> "Danger! Very close!"
            ParkingAlertLevel.WARNING -> "Warning! Close distance!"
            ParkingAlertLevel.INFO -> "Approaching obstacle"
            ParkingAlertLevel.NONE -> "Clear"
        }
    }
    
    fun getAlertSoundFrequency(): Int {
        return when (_alertLevel.value) {
            ParkingAlertLevel.CRITICAL -> 1000 // High frequency beep
            ParkingAlertLevel.DANGER -> 800
            ParkingAlertLevel.WARNING -> 600
            ParkingAlertLevel.INFO -> 400
            ParkingAlertLevel.NONE -> 0 // No sound
        }
    }
    
    override fun onAccuracyChanged(sensor: Sensor?, accuracy: Int) {
        // Handle accuracy changes if needed
    }
    
    fun cleanup() {
        sensorManager.unregisterListener(this)
        _isActive.value = false
    }
    
    companion object {
        @SuppressLint("StaticFieldLeak")
        private var instance: ParktronicService? = null
        
        fun initialize(context: Context): ParktronicService {
            if (instance == null) {
                instance = ParktronicService(context.applicationContext)
            }
            return instance!!
        }
        
        fun getInstance(): ParktronicService? {
            return instance
        }
    }
}
