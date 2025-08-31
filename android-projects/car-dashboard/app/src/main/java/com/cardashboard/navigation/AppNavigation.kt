package com.car.dashboard.navigation

import androidx.compose.runtime.Composable
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.car.dashboard.ui.screens.DashboardScreen
import com.car.dashboard.ui.screens.NavigationScreen
import com.car.dashboard.ui.screens.MediaScreen
import com.car.dashboard.ui.screens.PhoneScreen
import com.car.dashboard.ui.screens.MessagingScreen
import com.car.dashboard.ui.screens.WeatherScreen
import com.car.dashboard.ui.screens.SettingsScreen
import com.car.dashboard.ui.screens.ParktronicScreen
import com.car.dashboard.ui.screens.AutopilotScreen

sealed class Screen(val route: String) {
    object Dashboard : Screen("dashboard")
    object Navigation : Screen("navigation")
    object Media : Screen("media")
    object Phone : Screen("phone")
    object Messaging : Screen("messaging")
    object Weather : Screen("weather")
    object Settings : Screen("settings")
    object Parktronic : Screen("parktronic")
    object Autopilot : Screen("autopilot")
}

@Composable
fun AppNavigation(navController: NavHostController = rememberNavController()) {
    NavHost(
        navController = navController,
        startDestination = Screen.Dashboard.route
    ) {
        composable(Screen.Dashboard.route) {
            DashboardScreen(navController)
        }
        composable(Screen.Navigation.route) {
            NavigationScreen(navController)
        }
        composable(Screen.Media.route) {
            MediaScreen(navController)
        }
        composable(Screen.Phone.route) {
            PhoneScreen(navController)
        }
        composable(Screen.Messaging.route) {
            MessagingScreen(navController)
        }
        composable(Screen.Weather.route) {
            WeatherScreen(navController)
        }
        composable(Screen.Settings.route) {
            SettingsScreen(navController)
        }
        composable(Screen.Parktronic.route) {
            ParktronicScreen()
        }
        composable(Screen.Autopilot.route) {
            AutopilotScreen()
        }
    }
}

@Composable
fun navigateTo(navController: NavHostController, screen: Screen) {
    navController.navigate(screen.route) {
        // Pop up to the start destination of the graph to
        // avoid building up a large stack of destinations
        // on the back stack as users select items
        popUpTo(navController.graph.startDestinationId) {
            saveState = true
        }
        // Avoid multiple copies of the same destination when
        // reselecting the same item
        launchSingleTop = true
        // Restore state when reselecting a previously selected item
        restoreState = true
    }
}
