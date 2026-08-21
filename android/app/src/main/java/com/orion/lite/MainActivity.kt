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
import com.orion.lite.orion.MemoryRecord
import com.orion.lite.orion.OrionCore
import com.orion.lite.orion.OrionKernel
import com.orion.lite.orion.OrionMemory
import com.orion.lite.orion.SafetyPolicy

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val kernel = OrionKernel()
        val monitor = DeviceMonitor(this)
        val core = OrionCore()
        val router = ActionRouter()
        val safety = SafetyPolicy()
        val executor = ActionExecutor(this)
        val memory = OrionMemory(this)

        kernel.register("device_monitor", monitor)
        kernel.register("core", core)
        kernel.register("action_router", router)
        kernel.register("safety_policy", safety)
        kernel.register("action_executor", executor)

        kernel.boot()

        setContent {
            val state = remember { mutableStateOf("BOOTING") }
            val battery = remember { mutableStateOf(-1) }
            val safetyState = remember { mutableStateOf("CHECKING") }
            val action = remember { mutableStateOf("Starting...") }
            val recall = remember { mutableStateOf("No previous event.") }

            LaunchedEffect(Unit) {
                kernel.heartbeat()

                val previous = memory.recall()
                recall.value = if (previous != null) {
                    "Previous: ${previous.state} | Battery: ${previous.battery}% | " +
                        "Action: ${previous.actionId} | Result: ${previous.result}"
                } else {
                    "No previous event."
                }

                val device = monitor.read()
                val decision = core.analyze(
                    device,
                    previous,
                )
                val routedAction = router.route(decision)
                val safetyResult = safety.check(routedAction)

                if (safetyResult.allowed) {
                    val result = executor.execute(routedAction)
                    action.value = result.message
                    safetyState.value = "ALLOWED"

                    memory.remember(
                        MemoryRecord(
                            timestamp = System.currentTimeMillis(),
                            battery = device.batteryPercent,
                            state = decision.state,
                            actionId = routedAction.id,
                            safety = "ALLOWED",
                            result = result.message,
                        ),
                    )
                } else {
                    action.value = "Action blocked by safety policy."
                    safetyState.value = "BLOCKED"
                }

                battery.value = device.batteryPercent
                state.value = decision.state
            }

            MaterialTheme {
                Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(24.dp),
                    verticalArrangement = Arrangement.Center,
                ) {
                    Text(
                        text = "ORION Lite",
                        style = MaterialTheme.typography.headlineMedium,
                    )

                    Text(
                        text = "Kernel: ${
                            if (kernel.running) {
                                "ONLINE"
                            } else {
                                "OFFLINE"
                            }
                        }",
                        modifier = Modifier.padding(top = 16.dp),
                    )

                    Text(
                        text = "State: ${state.value}",
                        modifier = Modifier.padding(top = 8.dp),
                    )

                    Text(
                        text = "Battery: ${battery.value}%",
                        modifier = Modifier.padding(top = 8.dp),
                    )

                    Text(
                        text = "Safety: ${safetyState.value}",
                        modifier = Modifier.padding(top = 8.dp),
                    )

                    Text(
                        text = "Action: ${action.value}",
                        modifier = Modifier.padding(top = 8.dp),
                    )

                    Text(
                        text = "Recall: ${recall.value}",
                        modifier = Modifier.padding(top = 8.dp),
                    )
                }
            }
        }
    }
}
