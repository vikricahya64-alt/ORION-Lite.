package com.orion.lite

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.orion.lite.orion.DeviceMonitor
import com.orion.lite.orion.OrionCore
import com.orion.lite.orion.OrionKernel

class MainActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val kernel = OrionKernel()
        val monitor = DeviceMonitor(this)
        val core = OrionCore()

        kernel.register("device_monitor", monitor)
        kernel.register("core", core)

        kernel.boot()

        setContent {

            var state by remember {
                mutableStateOf("BOOTING")
            }

            var message by remember {
                mutableStateOf("ORION starting...")
            }

            LaunchedEffect(Unit) {

                kernel.heartbeat()

                val device = monitor.read()
                val decision = core.analyze(device)

                state = decision.state
                message =
                    "${decision.message}\nBattery: ${device.batteryPercent}%"
            }

            MaterialTheme {

                Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(24.dp),
                    verticalArrangement =
                        Arrangement.Center
                ) {

                    Text(
                        text = "ORION Lite",
                        style =
                            MaterialTheme.typography.headlineMedium
                    )

                    Text(
                        text = "Kernel: ${
                            if (kernel.running)
                                "ONLINE"
                            else
                                "OFFLINE"
                        }",
                        modifier =
                            Modifier.padding(top = 16.dp)
                    )

                    Text(
                        text = "State: $state",
                        modifier =
                            Modifier.padding(top = 8.dp)
                    )

                    Text(
                        text = message,
                        modifier =
                            Modifier.padding(top = 8.dp)
                    )
                }
            }
        }
    }
}
