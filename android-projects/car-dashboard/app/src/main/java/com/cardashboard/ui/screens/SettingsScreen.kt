package com.car.dashboard.ui.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.Bluetooth
import androidx.compose.material.icons.filled.DarkMode
import androidx.compose.material.icons.filled.Language
import androidx.compose.material.icons.filled.Notifications
import androidx.compose.material.icons.filled.PrivacyTip
import androidx.compose.material.icons.filled.Security
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material.icons.filled.Storage
import androidx.compose.material.icons.filled.VolumeUp
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.navigation.NavHostController

data class SettingItem(
    val title: String,
    val description: String,
    val icon: androidx.compose.ui.graphics.vector.ImageVector,
    val hasSwitch: Boolean = false,
    val hasChevron: Boolean = true
)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsScreen(navController: NavHostController) {
    val darkModeEnabled = remember { mutableStateOf(false) }
    val notificationsEnabled = remember { mutableStateOf(true) }
    val autoLaunchEnabled = remember { mutableStateOf(true) }
    val voiceControlEnabled = remember { mutableStateOf(true) }
    
    val settingsCategories = listOf(
        "Appearance",
        "Notifications",
        "Audio",
        "Connectivity",
        "Privacy & Security",
        "About"
    )
    
    val settingsItems = listOf(
        SettingItem("Dark Mode", "Enable dark theme", Icons.Default.DarkMode, true),
        SettingItem("Notifications", "Manage notification settings", Icons.Default.Notifications, true),
        SettingItem("Audio Settings", "Volume and sound preferences", Icons.Default.VolumeUp),
        SettingItem("Bluetooth", "Manage Bluetooth devices", Icons.Default.Bluetooth),
        SettingItem("Language", "App language settings", Icons.Default.Language),
        SettingItem("Auto Launch", "Start app automatically", Icons.Default.Settings, true),
        SettingItem("Voice Control", "Voice command settings", Icons.Default.Mic, true),
        SettingItem("Storage", "Clear cache and data", Icons.Default.Storage),
        SettingItem("Privacy", "Privacy settings and permissions", Icons.Default.PrivacyTip),
        SettingItem("Security", "Security and lock settings", Icons.Default.Security),
        SettingItem("About", "App version and information", Icons.Default.Settings, hasChevron = true)
    )

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
            .verticalScroll(rememberScrollState())
    ) {
        // Header with back button
        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            IconButton(
                onClick = { navController.popBackStack() }
            ) {
                Icon(
                    imageVector = Icons.Default.ArrowBack,
                    contentDescription = "Back"
                )
            }
            Spacer(modifier = Modifier.width(8.dp))
            Text(
                text = "Settings",
                style = MaterialTheme.typography.headlineMedium,
                fontWeight = FontWeight.Bold
            )
        }

        Spacer(modifier = Modifier.height(24.dp))

        // Settings categories
        settingsCategories.forEach { category ->
            Text(
                text = category,
                style = MaterialTheme.typography.titleLarge,
                fontWeight = FontWeight.Bold,
                modifier = Modifier.padding(vertical = 8.dp)
            )
            
            settingsItems.filter { it.title in getCategoryItems(category) }.forEach { setting ->
                SettingCard(setting, getSettingState(setting, darkModeEnabled, notificationsEnabled, autoLaunchEnabled, voiceControlEnabled))
            }
            
            Spacer(modifier = Modifier.height(16.dp))
        }
    }
}

private fun getCategoryItems(category: String): List<String> {
    return when (category) {
        "Appearance" -> listOf("Dark Mode")
        "Notifications" -> listOf("Notifications")
        "Audio" -> listOf("Audio Settings", "Voice Control")
        "Connectivity" -> listOf("Bluetooth", "Auto Launch")
        "Privacy & Security" -> listOf("Privacy", "Security", "Storage")
        "About" -> listOf("About", "Language")
        else -> emptyList()
    }
}

private fun getSettingState(
    setting: SettingItem,
    darkMode: androidx.compose.runtime.MutableState<Boolean>,
    notifications: androidx.compose.runtime.MutableState<Boolean>,
    autoLaunch: androidx.compose.runtime.MutableState<Boolean>,
    voiceControl: androidx.compose.runtime.MutableState<Boolean>
): Boolean {
    return when (setting.title) {
        "Dark Mode" -> darkMode.value
        "Notifications" -> notifications.value
        "Auto Launch" -> autoLaunch.value
        "Voice Control" -> voiceControl.value
        else -> false
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingCard(
    setting: SettingItem,
    switchState: Boolean = false,
    onSwitchChange: ((Boolean) -> Unit)? = null
) {
    Card(
        onClick = { if (!setting.hasSwitch) { /* Handle click */ } },
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surfaceVariant
        ),
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 4.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(
                imageVector = setting.icon,
                contentDescription = setting.title,
                modifier = Modifier.size(24.dp),
                tint = MaterialTheme.colorScheme.primary
            )
            Spacer(modifier = Modifier.width(16.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = setting.title,
                    style = MaterialTheme.typography.bodyMedium,
                    fontWeight = FontWeight.Medium
                )
                Text(
                    text = setting.description,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f)
                )
            }
            
            if (setting.hasSwitch) {
                Switch(
                    checked = switchState,
                    onCheckedChange = onSwitchChange
                )
            } else if (setting.hasChevron) {
                Icon(
                    imageVector = Icons.Default.ArrowBack,
                    contentDescription = "More",
                    modifier = Modifier.size(16.dp)
                )
            }
        }
    }
}

// Add missing import for Mic icon
private val Icons.Default.Mic: androidx.compose.ui.graphics.vector.ImageVector
    get() = androidx.compose.material.icons.Icons.Filled.Mic
