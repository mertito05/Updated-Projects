package com.car.dashboard

import android.app.Application
import android.content.Context
import com.car.dashboard.service.BluetoothService
import com.car.dashboard.service.LocationService
import com.car.dashboard.service.MediaService
import com.car.dashboard.service.VoiceService

class CarDashboardApp : Application() {
    
    companion object {
        private lateinit var instance: CarDashboardApp
        
        fun getAppContext(): Context {
            return instance.applicationContext
        }
    }
    
    override fun onCreate() {
        super.onCreate()
        instance = this
        
        // Initialize all services
        initializeServices()
    }
    
    private fun initializeServices() {
        // Initialize Location Service
        LocationService.initialize(this)
        
        // Initialize Media Service
        MediaService.initialize(this)
        
        // Initialize Bluetooth Service
        BluetoothService.initialize(this)
        
        // Initialize Voice Service
        VoiceService.initialize(this)
    }
    
    override fun onTerminate() {
        // Clean up services
        cleanupServices()
        super.onTerminate()
    }
    
    private fun cleanupServices() {
        // Clean up Media Service
        MediaService.getInstance()?.release()
        
        // Clean up Bluetooth Service
        BluetoothService.getInstance()?.cleanup()
        
        // Clean up Voice Service
        VoiceService.getInstance()?.destroy()
        
        // Stop location updates
        LocationService.getInstance()?.stopLocationUpdates()
    }
    
    fun restartServices() {
        cleanupServices()
        initializeServices()
    }
}
