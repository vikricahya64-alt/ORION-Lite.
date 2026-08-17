package com.orion.lite.orion

data class OrionAction(
    val id: String,
    val description: String
)

class ActionRouter {

    fun route(decision: OrionDecision): OrionAction {

        return when (decision.state) {

            "LOW_POWER" -> OrionAction(
                id = "LOW_POWER_NOTICE",
                description = "Battery is low. Reduce unnecessary activity."
            )

            "ATTENTION" -> OrionAction(
                id = "BATTERY_ATTENTION",
                description = "Battery level requires attention."
            )

            "NORMAL" -> OrionAction(
                id = "MONITOR",
                description = "Continue normal monitoring."
            )

            else -> OrionAction(
                id = "UNKNOWN",
                description = "Unable to determine required action."
            )
        }
    }
}
