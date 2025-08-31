package com.car.dashboard.service

import android.annotation.SuppressLint
import android.content.Context
import android.media.AudioAttributes
import android.media.AudioManager
import android.media.MediaPlayer
import android.net.Uri
import androidx.core.content.ContextCompat
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import java.io.IOException

data class MediaItem(
    val id: String,
    val title: String,
    val artist: String,
    val album: String,
    val duration: Long,
    val uri: Uri,
    val albumArtUri: Uri? = null
)

enum class PlaybackState {
    IDLE, PLAYING, PAUSED, STOPPED, ERROR, COMPLETED
}

class MediaService private constructor(context: Context) {
    
    private val context: Context = context.applicationContext
    private var mediaPlayer: MediaPlayer? = null
    private var currentMediaItem: MediaItem? = null
    
    private val _playbackState = MutableStateFlow(PlaybackState.IDLE)
    val playbackState: StateFlow<PlaybackState> = _playbackState
    
    private val _currentPosition = MutableStateFlow(0L)
    val currentPosition: StateFlow<Long> = _currentPosition
    
    private val _volume = MutableStateFlow(0.5f) // 0.0 to 1.0
    val volume: StateFlow<Float> = _volume
    
    private val _playlist = MutableStateFlow<List<MediaItem>>(emptyList())
    val playlist: StateFlow<List<MediaItem>> = _playlist
    
    private val _currentTrackIndex = MutableStateFlow(0)
    val currentTrackIndex: StateFlow<Int> = _currentTrackIndex
    
    private val audioManager: AudioManager =
        context.getSystemService(Context.AUDIO_SERVICE) as AudioManager
    
    init {
        initializeMediaPlayer()
        setupAudioFocus()
    }
    
    private fun initializeMediaPlayer() {
        mediaPlayer = MediaPlayer().apply {
            setOnPreparedListener {
                _playbackState.value = PlaybackState.PLAYING
                start()
            }
            setOnCompletionListener {
                _playbackState.value = PlaybackState.COMPLETED
                playNext()
            }
            setOnErrorListener { _, what, extra ->
                _playbackState.value = PlaybackState.ERROR
                false
            }
        }
    }
    
    private fun setupAudioFocus() {
        val audioAttributes = AudioAttributes.Builder()
            .setUsage(AudioAttributes.USAGE_MEDIA)
            .setContentType(AudioAttributes.CONTENT_TYPE_MUSIC)
            .build()
        
        mediaPlayer?.setAudioAttributes(audioAttributes)
    }
    
    fun play(mediaItem: MediaItem) {
        currentMediaItem = mediaItem
        mediaPlayer?.reset()
        
        try {
            mediaPlayer?.setDataSource(context, mediaItem.uri)
            mediaPlayer?.prepareAsync()
            _playbackState.value = PlaybackState.IDLE
        } catch (e: IOException) {
            _playbackState.value = PlaybackState.ERROR
        }
    }
    
    fun playFromPlaylist(index: Int) {
        if (index in _playlist.value.indices) {
            _currentTrackIndex.value = index
            play(_playlist.value[index])
        }
    }
    
    fun pause() {
        mediaPlayer?.pause()
        _playbackState.value = PlaybackState.PAUSED
    }
    
    fun resume() {
        mediaPlayer?.start()
        _playbackState.value = PlaybackState.PLAYING
    }
    
    fun stop() {
        mediaPlayer?.stop()
        mediaPlayer?.reset()
        _playbackState.value = PlaybackState.STOPPED
        _currentPosition.value = 0L
    }
    
    fun seekTo(position: Long) {
        mediaPlayer?.seekTo(position.toInt())
        _currentPosition.value = position
    }
    
    fun setVolume(volume: Float) {
        val clampedVolume = volume.coerceIn(0f, 1f)
        _volume.value = clampedVolume
        mediaPlayer?.setVolume(clampedVolume, clampedVolume)
    }
    
    fun playNext() {
        val nextIndex = (_currentTrackIndex.value + 1) % _playlist.value.size
        playFromPlaylist(nextIndex)
    }
    
    fun playPrevious() {
        val prevIndex = if (_currentTrackIndex.value == 0) {
            _playlist.value.size - 1
        } else {
            _currentTrackIndex.value - 1
        }
        playFromPlaylist(prevIndex)
    }
    
    fun setPlaylist(playlist: List<MediaItem>, startIndex: Int = 0) {
        _playlist.value = playlist
        if (playlist.isNotEmpty()) {
            playFromPlaylist(startIndex)
        }
    }
    
    fun shufflePlaylist() {
        val shuffled = _playlist.value.shuffled()
        _playlist.value = shuffled
        playFromPlaylist(0)
    }
    
    fun getDuration(): Long {
        return mediaPlayer?.duration?.toLong() ?: 0L
    }
    
    fun isPlaying(): Boolean {
        return mediaPlayer?.isPlaying ?: false
    }
    
    fun release() {
        mediaPlayer?.release()
        mediaPlayer = null
        _playbackState.value = PlaybackState.IDLE
    }
    
    fun requestAudioFocus(): Boolean {
        val result = audioManager.requestAudioFocus(
            audioFocusChangeListener,
            AudioManager.STREAM_MUSIC,
            AudioManager.AUDIOFOCUS_GAIN
        )
        return result == AudioManager.AUDIOFOCUS_REQUEST_GRANTED
    }
    
    fun abandonAudioFocus() {
        audioManager.abandonAudioFocus(audioFocusChangeListener)
    }
    
    private val audioFocusChangeListener = AudioManager.OnAudioFocusChangeListener { focusChange ->
        when (focusChange) {
            AudioManager.AUDIOFOCUS_LOSS -> {
                pause()
            }
            AudioManager.AUDIOFOCUS_LOSS_TRANSIENT -> {
                pause()
            }
            AudioManager.AUDIOFOCUS_LOSS_TRANSIENT_CAN_DUCK -> {
                setVolume(_volume.value * 0.2f)
            }
            AudioManager.AUDIOFOCUS_GAIN -> {
                setVolume(_volume.value)
                resume()
            }
        }
    }
    
    companion object {
        @SuppressLint("StaticFieldLeak")
        private var instance: MediaService? = null
        
        fun initialize(context: Context): MediaService {
            if (instance == null) {
                instance = MediaService(context.applicationContext)
            }
            return instance!!
        }
        
        fun getInstance(): MediaService? {
            return instance
        }
    }
}
