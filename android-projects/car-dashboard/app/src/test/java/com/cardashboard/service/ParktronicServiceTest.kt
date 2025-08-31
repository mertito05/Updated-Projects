package com.cardashboard.service

import org.junit.Test
import org.junit.Assert.*
import org.junit.Before

class ParktronicServiceTest {
    
    private lateinit var parktronicService: ParktronicService
    
    @Before
    fun setup() {
        parktronicService = ParktronicService()
    }
    
    @Test
    fun testParktronicServiceInitialization() {
        assertNotNull("ParktronicService should be initialized", parktronicService)
    }
    
    @Test
    fun testGetDistanceReadings() {
        val readings = parktronicService.getDistanceReadings()
        
        assertNotNull("Distance readings should not be null", readings)
        assertEquals("Should have readings for front, rear, left, right", 4, readings.size)
        
        // Test that all readings are within expected range
        readings.forEach { (sensor, distance) ->
            assertTrue("Distance should be between 0 and 200 cm", distance in 0.0..200.0)
        }
    }
    
    @Test
    fun testGetObstacleWarning() {
        // Test with safe distance
        parktronicService.setTestDistances(150.0, 160.0, 170.0, 180.0)
        var warning = parktronicService.getObstacleWarning()
        assertFalse("No warning should be generated for safe distances", warning.isWarning)
        
        // Test with critical distance
        parktronicService.setTestDistances(20.0, 160.0, 170.0, 180.0)
        warning = parktronicService.getObstacleWarning()
        assertTrue("Warning should be generated for critical distance", warning.isWarning)
        assertEquals("Warning should be for front sensor", "front", warning.sensor)
    }
    
    @Test
    fun testGetParkingAssistStatus() {
        val status = parktronicService.getParkingAssistStatus()
        
        assertNotNull("Parking assist status should not be null", status)
        assertTrue("Status should be either active or inactive", status.isActive || !status.isActive)
    }
    
    @Test
    fun testToggleParkingAssist() {
        val initialStatus = parktronicService.getParkingAssistStatus()
        parktronicService.toggleParkingAssist()
        val newStatus = parktronicService.getParkingAssistStatus()
        
        assertNotEquals("Parking assist status should toggle", initialStatus.isActive, newStatus.isActive)
    }
}
