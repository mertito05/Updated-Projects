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
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.Call
import androidx.compose.material.icons.filled.Contacts
import androidx.compose.material.icons.filled.Dialpad
import androidx.compose.material.icons.filled.History
import androidx.compose.material.icons.filled.Phone
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.navigation.NavHostController

data class Contact(
    val name: String,
    val number: String,
    val initial: Char
)

data class CallHistory(
    val name: String,
    val number: String,
    val time: String,
    val type: String // "incoming", "outgoing", "missed"
)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PhoneScreen(navController: NavHostController) {
    val phoneNumber = remember { mutableStateOf("") }
    val activeTab = remember { mutableStateOf("dialpad") } // "dialpad", "contacts", "history"
    
    val contacts = listOf(
        Contact("John Doe", "+1 (555) 123-4567", 'J'),
        Contact("Jane Smith", "+1 (555) 987-6543", 'J'),
        Contact("Bob Johnson", "+1 (555) 456-7890", 'B'),
        Contact("Alice Brown", "+1 (555) 321-0987", 'A')
    )
    
    val callHistory = listOf(
        CallHistory("John Doe", "+1 (555) 123-4567", "2:30 PM", "outgoing"),
        CallHistory("Unknown", "+1 (555) 999-8888", "1:45 PM", "missed"),
        CallHistory("Jane Smith", "+1 (555) 987-6543", "12:15 PM", "incoming"),
        CallHistory("Bob Johnson", "+1 (555) 456-7890", "Yesterday", "outgoing")
    )

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
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
                text = "Phone",
                style = MaterialTheme.typography.headlineMedium,
                fontWeight = FontWeight.Bold
            )
        }

        Spacer(modifier = Modifier.height(24.dp))

        // Phone number display and call button
        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            OutlinedTextField(
                value = phoneNumber.value,
                onValueChange = { phoneNumber.value = it },
                placeholder = { Text("Enter phone number") },
                modifier = Modifier.weight(1f),
                leadingIcon = {
                    Icon(Icons.Default.Phone, "Phone")
                }
            )
            Spacer(modifier = Modifier.width(8.dp))
            IconButton(
                onClick = { /* Make call */ },
                modifier = Modifier
                    .size(56.dp)
                    .clip(CircleShape),
                enabled = phoneNumber.value.isNotBlank()
            ) {
                Icon(
                    Icons.Default.Call,
                    "Call",
                    modifier = Modifier.size(32.dp)
                )
            }
        }

        Spacer(modifier = Modifier.height(24.dp))

        // Tab navigation
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceEvenly
        ) {
            IconButton(
                onClick = { activeTab.value = "dialpad" },
                modifier = Modifier.size(48.dp)
            ) {
                Icon(
                    Icons.Default.Dialpad,
                    "Dialpad",
                    tint = if (activeTab.value == "dialpad") MaterialTheme.colorScheme.primary 
                          else MaterialTheme.colorScheme.onSurface
                )
            }
            IconButton(
                onClick = { activeTab.value = "contacts" },
                modifier = Modifier.size(48.dp)
            ) {
                Icon(
                    Icons.Default.Contacts,
                    "Contacts",
                    tint = if (activeTab.value == "contacts") MaterialTheme.colorScheme.primary 
                          else MaterialTheme.colorScheme.onSurface
                )
            }
            IconButton(
                onClick = { activeTab.value = "history" },
                modifier = Modifier.size(48.dp)
            ) {
                Icon(
                    Icons.Default.History,
                    "History",
                    tint = if (activeTab.value == "history") MaterialTheme.colorScheme.primary 
                          else MaterialTheme.colorScheme.onSurface
                )
            }
        }

        Spacer(modifier = Modifier.height(24.dp))

        // Content based on active tab
        when (activeTab.value) {
            "dialpad" -> DialpadContent(phoneNumber)
            "contacts" -> ContactsContent(contacts)
            "history" -> CallHistoryContent(callHistory)
        }
    }
}

@Composable
fun DialpadContent(phoneNumber: androidx.compose.runtime.MutableState<String>) {
    val dialpadButtons = listOf(
        listOf("1", "2", "3"),
        listOf("4", "5", "6"),
        listOf("7", "8", "9"),
        listOf("*", "0", "#")
    )

    Column(
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        dialpadButtons.forEach { row ->
            Row(
                horizontalArrangement = Arrangement.SpaceEvenly,
                modifier = Modifier.fillMaxWidth()
            ) {
                row.forEach { digit ->
                    IconButton(
                        onClick = { phoneNumber.value += digit },
                        modifier = Modifier.size(64.dp)
                    ) {
                        Text(
                            text = digit,
                            style = MaterialTheme.typography.headlineMedium,
                            fontWeight = FontWeight.Bold
                        )
                    }
                }
            }
        }
    }
}

@Composable
fun ContactsContent(contacts: List<Contact>) {
    LazyColumn {
        items(contacts) { contact ->
            Card(
                onClick = { /* Call this contact */ },
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
                    // Contact avatar
                    Card(
                        shape = CircleShape,
                        colors = CardDefaults.cardColors(
                            containerColor = MaterialTheme.colorScheme.primary
                        ),
                        modifier = Modifier.size(40.dp)
                    ) {
                        Column(
                            modifier = Modifier.fillMaxSize(),
                            horizontalAlignment = Alignment.CenterHorizontally,
                            verticalArrangement = Arrangement.Center
                        ) {
                            Text(
                                text = contact.initial.toString(),
                                style = MaterialTheme.typography.bodyLarge,
                                fontWeight = FontWeight.Bold,
                                color = MaterialTheme.colorScheme.onPrimary
                            )
                        }
                    }
                    Spacer(modifier = Modifier.width(16.dp))
                    Column(modifier = Modifier.weight(1f)) {
                        Text(
                            text = contact.name,
                            style = MaterialTheme.typography.bodyMedium,
                            fontWeight = FontWeight.Medium
                        )
                        Text(
                            text = contact.number,
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f)
                        )
                    }
                    IconButton(
                        onClick = { /* Call this contact */ },
                        modifier = Modifier.size(32.dp)
                    ) {
                        Icon(Icons.Default.Call, "Call")
                    }
                }
            }
        }
    }
}

@Composable
fun CallHistoryContent(history: List<CallHistory>) {
    LazyColumn {
        items(history) { call ->
            Card(
                onClick = { /* Call back */ },
                colors = CardDefaults.cardColors(
                    containerColor = when (call.type) {
                        "missed" -> MaterialTheme.colorScheme.errorContainer
                        else -> MaterialTheme.colorScheme.surfaceVariant
                    }
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
                    Column(modifier = Modifier.weight(1f)) {
                        Text(
                            text = call.name,
                            style = MaterialTheme.typography.bodyMedium,
                            fontWeight = FontWeight.Medium,
                            color = when (call.type) {
                                "missed" -> MaterialTheme.colorScheme.error
                                else -> MaterialTheme.colorScheme.onSurface
                            }
                        )
                        Text(
                            text = "${call.number} • ${call.time}",
                            style = MaterialTheme.typography.bodySmall,
                            color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f)
                        )
                    }
                    Text(
                        text = when (call.type) {
                            "incoming" -> "Incoming"
                            "outgoing" -> "Outgoing"
                            "missed" -> "Missed"
                            else -> call.type
                        },
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f)
                    )
                }
            }
        }
    }
}
