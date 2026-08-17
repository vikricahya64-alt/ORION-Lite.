package com.orion.lite.orion

data class ExecutionResult(
    val actionId: String,
    val executed: Boolean,
    val message: String
)

class ActionExecutor {

    fun execute(action: OrionAction): ExecutionResult {

        return when (action.id) {

            "LOW_POWER_NOTICE" ->
                ExecutionResult(
                    action.id,
                    true,
                    action.description
                )

            "BATTERY_ATTENTION" ->
                ExecutionResult(
                    action.id,
                    true,
                    action.description
                )

            "MONITOR" ->
                ExecutionResult(
                    action.id,
                    true,
                    action.description
                )

            else ->
                ExecutionResult(
                    action.id,
                    false,
                    "Action not available."
                )
        }
    }
}
