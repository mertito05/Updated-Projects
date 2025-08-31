package com.car.dashboard.ui.components

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.size
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.unit.dp

@Composable
fun CarOutline(modifier: Modifier = Modifier) {
    Canvas(modifier = modifier.size(200.dp)) {
        val width = size.width
        val height = size.height
        
        // Car body
        drawRoundRect(
            color = Color(0xFF333333),
            topLeft = Offset(width * 0.2f, height * 0.3f),
            size = Size(width * 0.6f, height * 0.4f),
            cornerRadius = androidx.compose.ui.geometry.CornerRadius(width * 0.1f, height * 0.1f)
        )
        
        // Windshield
        drawRect(
            color = Color(0xFF87CEEB).copy(alpha = 0.3f),
            topLeft = Offset(width * 0.3f, height * 0.35f),
            size = Size(width * 0.4f, height * 0.15f)
        )
        
        // Wheels
        drawCircle(
            color = Color.Black,
            center = Offset(width * 0.25f, height * 0.7f),
            radius = width * 0.08f
        )
        
        drawCircle(
            color = Color.Black,
            center = Offset(width * 0.75f, height * 0.7f),
            radius = width * 0.08f
        )
        
        // Headlights
        drawCircle(
            color = Color.Yellow,
            center = Offset(width * 0.25f, height * 0.35f),
            radius = width * 0.04f
        )
        
        drawCircle(
            color = Color.Yellow,
            center = Offset(width * 0.75f, height * 0.35f),
            radius = width * 0.04f
        )
        
        // Outline
        drawRoundRect(
            color = Color.White,
            topLeft = Offset(width * 0.2f, height * 0.3f),
            size = Size(width * 0.6f, height * 0.4f),
            cornerRadius = androidx.compose.ui.geometry.CornerRadius(width * 0.1f, height * 0.1f),
            style = Stroke(width = 2.dp.toPx())
        )
    }
}
