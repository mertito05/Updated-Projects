package com.car.dashboard.service

import android.Manifest
import android.annotation.SuppressLint
import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothDevice
import android.bluetooth.BluetoothManager
import android.bluetooth.BluetoothProfile
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.content.pm.PackageManager
import androidx.core.app.ActivityCompat
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow

data class BluetoothDeviceInfo(
    val name: String,
    val address: String,
    val isConnected: Boolean = false,
    val isPaired: Boolean = false
)

enum class BluetoothState {
    UNKNOWN, TURNING_ON, ON, TURNING_OFF, OFF, ERROR
}

class BluetoothService private constructor(context: Context) {
    
    private val context: Context = context.applicationContext
    private val bluetoothManager: BluetoothManager =
        context.getSystemService(Context.BLUETOOTH_SERVICE) as BluetoothManager
    private val bluetoothAdapter: BluetoothAdapter? = bluetoothManager.adapter
    
    private val _bluetoothState = MutableStateFlow(BluetoothState.UNKNOWN)
    val bluetoothState: StateFlow<BluetoothState> = _bluetoothState
    
    private val _pairedDevices = MutableStateFlow<List<BluetoothDeviceInfo>>(emptyList())
    val pairedDevices: StateFlow<List<BluetoothDeviceInfo>> = _pairedDevices
    
    private val _availableDevices = MutableStateFlow<List<BluetoothDeviceInfo>>(emptyList())
    val availableDevices: StateFlow<List<BluetoothDeviceInfo>> = _availableDevices
    
    private val _connectedDevice = MutableStateFlow<BluetoothDeviceInfo?>(null)
    val connectedDevice: StateFlow<BluetoothDeviceInfo?> = _connectedDevice
    
    private val bluetoothReceiver = object : BroadcastReceiver() {
        override fun onReceive(context: Context, intent: Intent) {
            when (intent.action) {
                BluetoothAdapter.ACTION_STATE_CHANGED -> {
                    val state = intent.getIntExtra(BluetoothAdapter.EXTRA_STATE, BluetoothAdapter.ERROR)
                    updateBluetoothState(state)
                }
                BluetoothDevice.ACTION_FOUND -> {
                    val device: BluetoothDevice? = intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE)
                    device?.let { addAvailableDevice(it) }
                }
                BluetoothAdapter.ACTION_DISCOVERY_FINISHED -> {
                    // Discovery finished
                }
                BluetoothDevice.ACTION_ACL_CONNECTED -> {
                    val device: BluetoothDevice? = intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE)
                    device?.let { updateConnectedDevice(it, true) }
                }
                BluetoothDevice.ACTION_ACL_DISCONNECTED -> {
                    val device: BluetoothDevice? = intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE)
                    device?.let { updateConnectedDevice(it, false) }
                }
            }
        }
    }
    
    init {
        registerBluetoothReceiver()
        updateBluetoothState()
        loadPairedDevices()
    }
    
    private fun registerBluetoothReceiver() {
        val filter = IntentFilter().apply {
            addAction(BluetoothAdapter.ACTION_STATE_CHANGED)
            addAction(BluetoothDevice.ACTION_FOUND)
            addAction(BluetoothAdapter.ACTION_DISCOVERY_FINISHED)
            addAction(BluetoothDevice.ACTION_ACL_CONNECTED)
            addAction(BluetoothDevice.ACTION_ACL_DISCONNECTED)
        }
        context.registerReceiver(bluetoothReceiver, filter)
    }
    
    private fun updateBluetoothState(state: Int? = null) {
        val currentState = state ?: bluetoothAdapter?.state ?: BluetoothAdapter.ERROR
        _bluetoothState.value = when (currentState) {
            BluetoothAdapter.STATE_TURNING_ON -> BluetoothState.TURNING_ON
            BluetoothAdapter.STATE_ON -> BluetoothState.ON
            BluetoothState.TURNING_OFF.ordinal -> BluetoothState.TURNING_OFF
            BluetoothAdapter.STATE_OFF -> BluetoothState.OFF
            else -> BluetoothState.ERROR
        }
    }
    
    @SuppressLint("MissingPermission")
    private fun loadPairedDevices() {
        if (hasBluetoothPermissions() && bluetoothAdapter != null) {
            val pairedDevicesList = bluetoothAdapter.bondedDevices?.map { device ->
                BluetoothDeviceInfo(
                    name = device.name ?: "Unknown",
                    address = device.address,
                    isPaired = true,
                    isConnected = isDeviceConnected(device)
                )
            } ?: emptyList()
            
            _pairedDevices.value = pairedDevicesList
            
            // Check if any paired device is connected
            val connectedDevice = pairedDevicesList.firstOrNull { it.isConnected }
            _connectedDevice.value = connectedDevice
        }
    }
    
    @SuppressLint("MissingPermission")
    private fun isDeviceConnected(device: BluetoothDevice): Boolean {
        return try {
            bluetoothManager.getConnectionState(device, BluetoothProfile.A2DP) == BluetoothProfile.STATE_CONNECTED ||
                    bluetoothManager.getConnectionState(device, BluetoothProfile.HEADSET) == BluetoothProfile.STATE_CONNECTED
        } catch (e: SecurityException) {
            false
        }
    }
    
    @SuppressLint("MissingPermission")
    private fun addAvailableDevice(device: BluetoothDevice) {
        val deviceInfo = BluetoothDeviceInfo(
            name = device.name ?: "Unknown",
            address = device.address,
            isPaired = device.bondState == BluetoothDevice.BOND_BONDED,
            isConnected = isDeviceConnected(device)
        )
        
        val currentList = _availableDevices.value.toMutableList()
        if (!currentList.any { it.address == deviceInfo.address }) {
            currentList.add(deviceInfo)
            _availableDevices.value = currentList
        }
    }
    
    @SuppressLint("MissingPermission")
    private fun updateConnectedDevice(device: BluetoothDevice, isConnected: Boolean) {
        val deviceInfo = BluetoothDeviceInfo(
            name = device.name ?: "Unknown",
            address = device.address,
            isPaired = device.bondState == BluetoothDevice.BOND_BONDED,
            isConnected = isConnected
        )
        
        _connectedDevice.value = if (isConnected) deviceInfo else null
        
        // Update paired devices list
        loadPairedDevices()
    }
    
    fun enableBluetooth(): Boolean {
        return bluetoothAdapter?.enable() ?: false
    }
    
    fun disableBluetooth(): Boolean {
        return bluetoothAdapter?.disable() ?: false
    }
    
    fun isBluetoothEnabled(): Boolean {
        return bluetoothAdapter?.isEnabled ?: false
    }
    
    @SuppressLint("MissingPermission")
    fun startDiscovery(): Boolean {
        return if (hasBluetoothPermissions() && bluetoothAdapter != null) {
            _availableDevices.value = emptyList()
            bluetoothAdapter.startDiscovery()
        } else {
            false
        }
    }
    
    fun cancelDiscovery() {
        bluetoothAdapter?.cancelDiscovery()
    }
    
    @SuppressLint("MissingPermission")
    fun pairDevice(address: String): Boolean {
        if (!hasBluetoothPermissions()) return false
        
        val device = bluetoothAdapter?.getRemoteDevice(address)
        return device?.createBond() ?: false
    }
    
    @SuppressLint("MissingPermission")
    fun connectDevice(address: String): Boolean {
        if (!hasBluetoothPermissions()) return false
        
        // This would typically involve creating a BluetoothSocket and connecting
        // For simplicity, we'll just simulate the connection
        val device = bluetoothAdapter?.getRemoteDevice(address)
        device?.let {
            updateConnectedDevice(it, true)
            return true
        }
        return false
    }
    
    @SuppressLint("MissingPermission")
    fun disconnectDevice(): Boolean {
        // This would typically involve closing the BluetoothSocket
        // For simplicity, we'll just simulate the disconnection
        _connectedDevice.value?.let {
            val device = bluetoothAdapter?.getRemoteDevice(it.address)
            device?.let { updateConnectedDevice(it, false) }
            return true
        }
        return false
    }
    
    fun hasBluetoothPermissions(): Boolean {
        return ActivityCompat.checkSelfPermission(
            context,
            Manifest.permission.BLUETOOTH_CONNECT
        ) == PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(
            context,
            Manifest.permission.BLUETOOTH_SCAN
        ) == PackageManager.PERMISSION_GRANTED
    }
    
    fun cleanup() {
        try {
            context.unregisterReceiver(bluetoothReceiver)
        } catch (e: IllegalArgumentException) {
            // Receiver was not registered
        }
    }
    
    companion object {
        @SuppressLint("StaticFieldLeak")
        private var instance: BluetoothService? = null
        
        fun initialize(context: Context): BluetoothService {
            if (instance == null) {
                instance = BluetoothService(context.applicationContext)
            }
            return instance!!
        }
        
        fun getInstance(): BluetoothService? {
            return instance
        }
    }
}
