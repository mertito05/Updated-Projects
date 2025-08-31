package com.car.dashboard.service

import android.Manifest
import android.annotation.SuppressLint
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.speech.RecognitionListener
import android.speech.RecognizerIntent
import android.speech.SpeechRecognizer
import androidx.core.app.ActivityCompat
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow

data class VoiceCommand(
    val text: String,
    val confidence: Float,
    val timestamp: Long = System.currentTimeMillis()
)

enum class VoiceRecognitionState {
    IDLE, LISTENING, PROCESSING, ERROR, SUCCESS
}

class VoiceService private constructor(context: Context) {
    
    private val context: Context = context.applicationContext
    private var speechRecognizer: SpeechRecognizer? = null
    
    private val _recognitionState = MutableStateFlow(VoiceRecognitionState.IDLE)
    val recognitionState: StateFlow<VoiceRecognitionState> = _recognitionState
    
    private val _lastCommand = MutableStateFlow<VoiceCommand?>(null)
    val lastCommand: StateFlow<VoiceCommand?> = _lastCommand
    
    private val _commandHistory = MutableStateFlow<List<VoiceCommand>>(emptyList())
    val commandHistory: StateFlow<List<VoiceCommand>> = _commandHistory
    
    private val recognitionListener = object : RecognitionListener {
        override fun onReadyForSpeech(params: android.os.Bundle?) {
            _recognitionState.value = VoiceRecognitionState.LISTENING
        }
        
        override fun onBeginningOfSpeech() {
            // Speech started
        }
        
        override fun onRmsChanged(rmsdB: Float) {
            // RMS changed - can be used for visual feedback
        }
        
        override fun onBufferReceived(buffer: ByteArray?) {
            // Buffer received
        }
        
        override fun onEndOfSpeech() {
            _recognitionState.value = VoiceRecognitionState.PROCESSING
        }
        
        override fun onError(error: Int) {
            _recognitionState.value = VoiceRecognitionState.ERROR
            // Handle specific errors if needed
        }
        
        override fun onResults(results: android.os.Bundle?) {
            val matches = results?.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)
            val confidences = results?.getFloatArray(SpeechRecognizer.CONFIDENCE_SCORES)
            
            if (!matches.isNullOrEmpty()) {
                val bestMatch = matches[0]
                val confidence = confidences?.getOrNull(0) ?: 0f
                
                val command = VoiceCommand(
                    text = bestMatch,
                    confidence = confidence
                )
                
                _lastCommand.value = command
                _commandHistory.value = _commandHistory.value + command
                _recognitionState.value = VoiceRecognitionState.SUCCESS
                
                // Process the command
                processVoiceCommand(command)
            } else {
                _recognitionState.value = VoiceRecognitionState.ERROR
            }
        }
        
        override fun onPartialResults(partialResults: android.os.Bundle?) {
            // Partial results - can be used for real-time feedback
        }
        
        override fun onEvent(eventType: Int, params: android.os.Bundle?) {
            // Event occurred
        }
    }
    
    init {
        initializeSpeechRecognizer()
    }
    
    private fun initializeSpeechRecognizer() {
        if (SpeechRecognizer.isRecognitionAvailable(context)) {
            speechRecognizer = SpeechRecognizer.createSpeechRecognizer(context).apply {
                setRecognitionListener(recognitionListener)
            }
        }
    }
    
    @SuppressLint("MissingPermission")
    fun startListening() {
        if (!hasVoiceRecognitionPermission()) {
            _recognitionState.value = VoiceRecognitionState.ERROR
            return
        }
        
        if (speechRecognizer == null) {
            initializeSpeechRecognizer()
        }
        
        val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
            putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
            putExtra(RecognizerIntent.EXTRA_PROMPT, "Say a command...")
            putExtra(RecognizerIntent.EXTRA_MAX_RESULTS, 5)
            putExtra(RecognizerIntent.EXTRA_PARTIAL_RESULTS, true)
        }
        
        speechRecognizer?.startListening(intent)
    }
    
    fun stopListening() {
        speechRecognizer?.stopListening()
        _recognitionState.value = VoiceRecognitionState.IDLE
    }
    
    fun cancelListening() {
        speechRecognizer?.cancel()
        _recognitionState.value = VoiceRecognitionState.IDLE
    }
    
    private fun processVoiceCommand(command: VoiceCommand) {
        val text = command.text.lowercase()
        
        when {
            text.contains("call") || text.contains("phone") -> handleCallCommand(text)
            text.contains("navigate") || text.contains("directions") -> handleNavigationCommand(text)
            text.contains("play") || text.contains("music") -> handleMediaCommand(text)
            text.contains("message") || text.contains("text") -> handleMessageCommand(text)
            text.contains("weather") -> handleWeatherCommand(text)
            text.contains("settings") -> handleSettingsCommand(text)
            else -> handleGenericCommand(text)
        }
    }
    
    private fun handleCallCommand(command: String) {
        // Extract phone number or contact name and initiate call
        // This would integrate with the PhoneService
    }
    
    private fun handleNavigationCommand(command: String) {
        // Extract destination and start navigation
        // This would integrate with the NavigationService
    }
    
    private fun handleMediaCommand(command: String) {
        // Control media playback
        // This would integrate with the MediaService
        when {
            command.contains("play") -> MediaService.getInstance()?.resume()
            command.contains("pause") -> MediaService.getInstance()?.pause()
            command.contains("next") -> MediaService.getInstance()?.playNext()
            command.contains("previous") -> MediaService.getInstance()?.playPrevious()
            command.contains("volume up") -> adjustVolume(true)
            command.contains("volume down") -> adjustVolume(false)
        }
    }
    
    private fun handleMessageCommand(command: String) {
        // Handle messaging commands
        // This would integrate with the MessagingService
    }
    
    private fun handleWeatherCommand(command: String) {
        // Handle weather queries
        // This would integrate with the WeatherService
    }
    
    private fun handleSettingsCommand(command: String) {
        // Handle settings commands
        when {
            command.contains("bluetooth") -> handleBluetoothCommand(command)
            command.contains("wifi") -> handleWifiCommand(command)
            // Add other setting commands
        }
    }
    
    private fun handleBluetoothCommand(command: String) {
        // Handle Bluetooth commands
        val bluetoothService = BluetoothService.getInstance()
        when {
            command.contains("turn on") || command.contains("enable") -> bluetoothService?.enableBluetooth()
            command.contains("turn off") || command.contains("disable") -> bluetoothService?.disableBluetooth()
            command.contains("connect") -> {
                // Extract device name and connect
            }
            command.contains("disconnect") -> bluetoothService?.disconnectDevice()
        }
    }
    
    private fun handleWifiCommand(command: String) {
        // Handle WiFi commands
        // This would require a WiFi service
    }
    
    private fun handleGenericCommand(command: String) {
        // Handle generic commands or provide feedback
    }
    
    private fun adjustVolume(increase: Boolean) {
        val mediaService = MediaService.getInstance()
        val currentVolume = mediaService?.volume?.value ?: 0.5f
        val newVolume = if (increase) {
            (currentVolume + 0.1f).coerceAtMost(1.0f)
        } else {
            (currentVolume - 0.1f).coerceAtLeast(0.0f)
        }
        mediaService?.setVolume(newVolume)
    }
    
    fun hasVoiceRecognitionPermission(): Boolean {
        return ActivityCompat.checkSelfPermission(
            context,
            Manifest.permission.RECORD_AUDIO
        ) == PackageManager.PERMISSION_GRANTED
    }
    
    fun isSpeechRecognitionAvailable(): Boolean {
        return SpeechRecognizer.isRecognitionAvailable(context)
    }
    
    fun destroy() {
        speechRecognizer?.destroy()
        speechRecognizer = null
    }
    
    companion object {
        @SuppressLint("StaticFieldLeak")
        private var instance: VoiceService? = null
        
        fun initialize(context: Context): VoiceService {
            if (instance == null) {
                instance = VoiceService(context.applicationContext)
            }
            return instance!!
        }
        
        fun getInstance(): VoiceService? {
            return instance
        }
    }
}
