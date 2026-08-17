package com.orion.lite.orion

data class SafetyResult(
    val allowed: Boolean,
    val reason: String
)

class SafetyPolicy {

    fun check(action: OrionAction): SafetyResult {

        return when (action.id) {

            "BATTERY_ATTENTION" -> SafetyResult(
                allowed = true,
                reason = "Battery attention action is allowed."
            )

            "LOW_POWER_NOTICE" -> SafetyResult(
                allowed = true,
                reason = "Low power action is allowed."
            )

            "MONITOR" -> SafetyResult(
                allowed = true,
                reason = "Normal monitoring is allowed."
            )

            else -> SafetyResult(
                allowed = false,
                reason = "Action is not authorized."
            )
        }
    }
}
