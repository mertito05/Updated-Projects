package com.car.dashboard.utils

import android.Manifest
import android.app.Activity
import android.content.Context
import android.content.pm.PackageManager
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat

object PermissionsUtils {
    
    // Location permissions
    val LOCATION_PERMISSIONS = arrayOf(
        Manifest.permission.ACCESS_FINE_LOCATION,
        Manifest.permission.ACCESS_COARSE_LOCATION
    )
    
    // Bluetooth permissions (for Android 12+)
    val BLUETOOTH_PERMISSIONS = arrayOf(
        Manifest.permission.BLUETOOTH_CONNECT,
        Manifest.permission.BLUETOOTH_SCAN
    )
    
    // Audio permissions
    val AUDIO_PERMISSIONS = arrayOf(
        Manifest.permission.RECORD_AUDIO
    )
    
    // Phone permissions
    val PHONE_PERMISSIONS = arrayOf(
        Manifest.permission.CALL_PHONE,
        Manifest.permission.READ_PHONE_STATE
    )
    
    // Contacts permissions
    val CONTACTS_PERMISSIONS = arrayOf(
        Manifest.permission.READ_CONTACTS
    )
    
    // SMS permissions
    val SMS_PERMISSIONS = arrayOf(
        Manifest.permission.SEND_SMS,
        Manifest.permission.READ_SMS
    )
    
    // All required permissions for the app
    val ALL_REQUIRED_PERMISSIONS = arrayOf(
        *LOCATION_PERMISSIONS,
        *BLUETOOTH_PERMISSIONS,
        *AUDIO_PERMISSIONS,
        *PHONE_PERMISSIONS,
        *CONTACTS_PERMISSIONS,
        *SMS_PERMISSIONS
    ).distinct().toTypedArray()
    
    fun hasPermissions(context: Context, permissions: Array<String>): Boolean {
        return permissions.all { permission ->
            ContextCompat.checkSelfPermission(context, permission) == PackageManager.PERMISSION_GRANTED
        }
    }
    
    fun hasLocationPermissions(context: Context): Boolean {
        return hasPermissions(context, LOCATION_PERMISSIONS)
    }
    
    fun hasBluetoothPermissions(context: Context): Boolean {
        return hasPermissions(context, BLUETOOTH_PERMISSIONS)
    }
    
    fun hasAudioPermissions(context: Context): Boolean {
        return hasPermissions(context, AUDIO_PERMISSIONS)
    }
    
    fun hasPhonePermissions(context: Context): Boolean {
        return hasPermissions(context, PHONE_PERMISSIONS)
    }
    
    fun hasContactsPermissions(context: Context): Boolean {
        return hasPermissions(context, CONTACTS_PERMISSIONS)
    }
    
    fun hasSmsPermissions(context: Context): Boolean {
        return hasPermissions(context, SMS_PERMISSIONS)
    }
    
    fun requestPermissions(activity: Activity, permissions: Array<String>, requestCode: Int) {
        ActivityCompat.requestPermissions(activity, permissions, requestCode)
    }
    
    fun shouldShowRequestPermissionRationale(activity: Activity, permission: String): Boolean {
        return ActivityCompat.shouldShowRequestPermissionRationale(activity, permission)
    }
    
    fun getMissingPermissions(context: Context, permissions: Array<String>): List<String> {
        return permissions.filter { permission ->
            ContextCompat.checkSelfPermission(context, permission) != PackageManager.PERMISSION_GRANTED
        }
    }
    
    fun getMissingLocationPermissions(context: Context): List<String> {
        return getMissingPermissions(context, LOCATION_PERMISSIONS)
    }
    
    fun getMissingBluetoothPermissions(context: Context): List<String> {
        return getMissingPermissions(context, BLUETOOTH_PERMISSIONS)
    }
    
    fun getMissingAudioPermissions(context: Context): List<String> {
        return getMissingPermissions(context, AUDIO_PERMISSIONS)
    }
    
    fun getMissingPhonePermissions(context: Context): List<String> {
        return getMissingPermissions(context, PHONE_PERMISSIONS)
    }
    
    fun getMissingContactsPermissions(context: Context): List<String> {
        return getMissingPermissions(context, CONTACTS_PERMISSIONS)
    }
    
    fun getMissingSmsPermissions(context: Context): List<String> {
        return getMissingPermissions(context, SMS_PERMISSIONS)
    }
    
    fun getPermissionDisplayName(permission: String): String {
        return when (permission) {
            Manifest.permission.ACCESS_FINE_LOCATION -> "Precise Location"
            Manifest.permission.ACCESS_COARSE_LOCATION -> "Approximate Location"
            Manifest.permission.BLUETOOTH_CONNECT -> "Bluetooth Connection"
            Manifest.permission.BLUETOOTH_SCAN -> "Bluetooth Scanning"
            Manifest.permission.RECORD_AUDIO -> "Microphone"
            Manifest.permission.CALL_PHONE -> "Phone Calls"
            Manifest.permission.READ_PHONE_STATE -> "Phone Status"
            Manifest.permission.READ_CONTACTS -> "Contacts"
            Manifest.permission.SEND_SMS -> "Send SMS"
            Manifest.permission.READ_SMS -> "Read SMS"
            else -> permission
        }
    }
    
    fun getPermissionExplanation(permission: String): String {
        return when (permission) {
            Manifest.permission.ACCESS_FINE_LOCATION -> "Required for accurate navigation and location-based services"
            Manifest.permission.ACCESS_COARSE_LOCATION -> "Required for approximate location services"
            Manifest.permission.BLUETOOTH_CONNECT -> "Required to connect to Bluetooth devices for calls and audio"
            Manifest.permission.BLUETOOTH_SCAN -> "Required to discover nearby Bluetooth devices"
            Manifest.permission.RECORD_AUDIO -> "Required for voice commands and hands-free operation"
            Manifest.permission.CALL_PHONE -> "Required to make phone calls from the dashboard"
            Manifest.permission.READ_PHONE_STATE -> "Required to monitor call status and manage calls"
            Manifest.permission.READ_CONTACTS -> "Required to access your contacts for calling and messaging"
            Manifest.permission.SEND_SMS -> "Required to send text messages"
            Manifest.permission.READ_SMS -> "Required to read incoming messages"
            else -> "Required for app functionality"
        }
    }
    
    fun areAllRequiredPermissionsGranted(context: Context): Boolean {
        return hasPermissions(context, ALL_REQUIRED_PERMISSIONS)
    }
    
    fun getMissingRequiredPermissions(context: Context): List<String> {
        return getMissingPermissions(context, ALL_REQUIRED_PERMISSIONS)
    }
    
    fun getPermissionRequestCode(permission: String): Int {
        return when (permission) {
            in LOCATION_PERMISSIONS -> 1001
            in BLUETOOTH_PERMISSIONS -> 1002
            in AUDIO_PERMISSIONS -> 1003
            in PHONE_PERMISSIONS -> 1004
            in CONTACTS_PERMISSIONS -> 1005
            in SMS_PERMISSIONS -> 1006
            else -> 1000
        }
    }
}
