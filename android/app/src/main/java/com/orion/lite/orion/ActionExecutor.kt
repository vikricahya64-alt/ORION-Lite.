package com.orion.lite.orion

import android.content.Context
import android.content.Intent
import android.provider.Settings

data class ExecutionResult(
    val actionId: String,
    val executed: Boolean,
    val message: String,
)

class ActionExecutor(
    private val context: Context,
) {
    fun execute(action: OrionAction): ExecutionResult {
        return when (action.id) {
            "LOW_POWER_NOTICE",
            "BATTERY_ATTENTION",
            -> {
                val intent = Intent(
                    Settings.ACTION_BATTERY_SAVER_SETTINGS,
                ).apply {
                    addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                }

                try {
                    context.startActivity(intent)

                    ExecutionResult(
                        actionId = action.id,
                        executed = true,
                        message = "Battery settings opened.",
                    )
                } catch (_: Exception) {
                    ExecutionResult(
                        actionId = action.id,
                        executed = false,
                        message = "Unable to open battery settings.",
                    )
                }
            }

            "MONITOR" -> {
                ExecutionResult(
                    actionId = action.id,
                    executed = true,
                    message = "Normal monitoring continues.",
                )
            }

            else -> {
                ExecutionResult(
                    actionId = action.id,
                    executed = false,
                    message = "Action not available.",
                )
            }
        }
    }
}
