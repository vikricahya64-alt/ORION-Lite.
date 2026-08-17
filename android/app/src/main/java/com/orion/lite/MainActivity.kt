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
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.orion.lite.orion.ActionExecutor
import com.orion.lite.orion.ActionRouter
import com.orion.lite.orion.DeviceMonitor
import com.orion.lite.orion.OrionCore
import com.orion.lite.orion.OrionKernel

class MainActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val kernel = OrionKernel()
        val monitor = DeviceMonitor(this)
        val core = OrionCore()
        val router = ActionRouter()
        val executor = ActionExecutor()

        kernel.register("device_monitor", monitor)
        kernel.register("core", core)
        kernel.register("action_router", router)
        kernel.register("action_executor", executor)

        kernel.boot()

        setContent {

            var state = remember {
                mutableStateOf("BOOTING")
            }

            var battery = remember {
                mutableStateOf(-1)
            }

            var action = remember {
                mutableStateOf("Starting...")
            }

            LaunchedEffect(Unit) {

                kernel.heartbeat()

                val device = monitor.read()
                val decision = core.analyze(device)
                val routedAction = router.route(decision)
                val result = executor.execute(routedAction)

                battery.value = device.batteryPercent
                state.value = decision.state
                action.value = result.message
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
                        text = "State: ${state.value}",
                        modifier =
                            Modifier.padding(top = 8.dp)
                    )

                    Text(
                        text = "Battery: ${battery.value}%",
                        modifier =
                            Modifier.padding(top = 8.dp)
                    )

                    Text(
                        text = "Action: ${action.value}",
                        modifier =
                            Modifier.padding(top = 8.dp)
                    )
                }
            }
        }
    }
}
