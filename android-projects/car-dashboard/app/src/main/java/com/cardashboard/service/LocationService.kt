package com.car.dashboard.service

import android.Manifest
import android.annotation.SuppressLint
import android.content.Context
import android.content.pm.PackageManager
import android.location.Location
import android.location.LocationListener
import android.location.LocationManager
import android.os.Looper
import androidx.core.app.ActivityCompat
import com.google.android.gms.location.FusedLocationProviderClient
import com.google.android.gms.location.LocationCallback
import com.google.android.gms.location.LocationRequest
import com.google.android.gms.location.LocationResult
import com.google.android.gms.location.LocationServices
import com.google.android.gms.location.Priority
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow

class LocationService private constructor(context: Context) {
    
    private val fusedLocationClient: FusedLocationProviderClient =
        LocationServices.getFusedLocationProviderClient(context)
    
    private val locationManager: LocationManager =
        context.getSystemService(Context.LOCATION_SERVICE) as LocationManager
    
    private val _currentLocation = MutableStateFlow<Location?>(null)
    val currentLocation: StateFlow<Location?> = _currentLocation
    
    private val _locationUpdates = MutableStateFlow<List<Location>>(emptyList())
    val locationUpdates: StateFlow<List<Location>> = _locationUpdates
    
    private val locationCallback = object : LocationCallback() {
        override fun onLocationResult(locationResult: LocationResult) {
            super.onLocationResult(locationResult)
            locationResult.lastLocation?.let { location ->
                _currentLocation.value = location
                _locationUpdates.value = _locationUpdates.value + location
            }
        }
    }
    
    @SuppressLint("MissingPermission")
    fun startLocationUpdates() {
        if (hasLocationPermission()) {
            val locationRequest = LocationRequest.Builder(
                Priority.PRIORITY_HIGH_ACCURACY,
                5000L // 5 seconds
            ).setMinUpdateIntervalMillis(2000L) // 2 seconds
                .build()
            
            fusedLocationClient.requestLocationUpdates(
                locationRequest,
                locationCallback,
                Looper.getMainLooper()
            )
        }
    }
    
    fun stopLocationUpdates() {
        fusedLocationClient.removeLocationUpdates(locationCallback)
    }
    
    @SuppressLint("MissingPermission")
    fun getLastKnownLocation(): Location? {
        return if (hasLocationPermission()) {
            var lastLocation: Location? = null
            try {
                lastLocation = fusedLocationClient.lastLocation.result
            } catch (e: Exception) {
                // Handle exception
            }
            lastLocation
        } else {
            null
        }
    }
    
    fun hasLocationPermission(): Boolean {
        return ActivityCompat.checkSelfPermission(
            fusedLocationClient.applicationContext,
            Manifest.permission.ACCESS_FINE_LOCATION
        ) == PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(
            fusedLocationClient.applicationContext,
            Manifest.permission.ACCESS_COARSE_LOCATION
        ) == PackageManager.PERMISSION_GRANTED
    }
    
    fun isGpsEnabled(): Boolean {
        return locationManager.isProviderEnabled(LocationManager.GPS_PROVIDER)
    }
    
    fun isNetworkEnabled(): Boolean {
        return locationManager.isProviderEnabled(LocationManager.NETWORK_PROVIDER)
    }
    
    companion object {
        @SuppressLint("StaticFieldLeak")
        private var instance: LocationService? = null
        
        fun initialize(context: Context): LocationService {
            if (instance == null) {
                instance = LocationService(context.applicationContext)
            }
            return instance!!
        }
        
        fun getInstance(): LocationService? {
            return instance
        }
    }
}
