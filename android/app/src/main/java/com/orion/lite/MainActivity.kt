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
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
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
    private lateinit var kernel: OrionKernel
    private lateinit var monitor: DeviceMonitor
    private lateinit var core: OrionCore
    private lateinit var router: ActionRouter
    private lateinit var safety: SafetyPolicy
    private lateinit var executor: ActionExecutor
    private lateinit var memory: OrionMemory

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        kernel = OrionKernel()
        monitor = DeviceMonitor(this)
        core = OrionCore()
        router = ActionRouter()
        safety = SafetyPolicy()
        executor = ActionExecutor(this)
        memory = OrionMemory(this)

        kernel.boot()

        setContent {
            var state =
                remember {
                    mutableStateOf("BOOTING")
                }

            var battery =
                remember {
                    mutableStateOf(-1)
                }

            var safetyState =
                remember {
                    mutableStateOf("CHECKING")
                }

            var action =
                remember {
                    mutableStateOf("Starting...")
                }

            var recall =
                remember {
                    mutableStateOf("No previous event.")
                }

            LaunchedEffect(Unit) {
                kernel.heartbeat()

                val previous = memory.recall()

                recall.value =
                    if (previous != null) {
                        "Previous: ${previous.state} | Battery: ${previous.battery}% | " +
                            "Action: ${previous.actionId} | Result: ${previous.result}"
                    } else {
                        "No previous event."
                    }

                val device = monitor.read()

                val decision =
                    core.analyze(
                        device,
                        previous,
                    )

                val routedAction = router.route(decision)

                val safetyResult =
                    safety.check(routedAction)

                if (safetyResult.allowed) {
                    val result =
                        executor.execute(routedAction)

                    action.value = result.message
                    safetyState.value = "ALLOWED"

                    memory.save(
                        MemoryRecord(
                            state = decision.state,
                            battery = device.batteryPercent,
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
                    modifier =
                        Modifier
                            .fillMaxSize()
                            .padding(24.dp),
                    verticalArrangement = Arrangement.Center,
                ) {
                    Text(
                        text = "ORION Lite",
                        style = MaterialTheme.typography.headlineMedium,
                    )

                    Text(
                        text =
                            "Kernel: ${
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
