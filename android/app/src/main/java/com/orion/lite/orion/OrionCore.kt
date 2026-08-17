package com.orion.lite.orion

data class OrionDecision(
    val state: String,
    val message: String
)

class OrionCore {

    fun analyze(
    device: DeviceState,
    previous: MemoryRecord?
): OrionDecision {

        val repeatBatteryAttention =
            previous != null &&
            previous.state == "ATTENTION" &&
            previous.actionId == "BATTERY_ATTENTION" &&
            previous.result.contains(
                "Battery Settings",
                ignoreCase = true
            ) &&
            device.batteryPercent <= 50

        if (repeatBatteryAttention) {
            return OrionDecision(
                "NORMAL",
                "Previous battery attention already handled"
            )
        }

        return when {
            device.batteryPercent < 0 ->
                OrionDecision(
                    "UNKNOWN",
                    "Battery information unavailable"
                )

            device.batteryPercent <= 20 ->
                OrionDecision(
                    "LOW_POWER",
                    "Battery low"
                )

            device.batteryPercent <= 50 ->
                OrionDecision(
                    "ATTENTION",
                    "Battery needs attention"
                )

            else ->
                OrionDecision(
                    "NORMAL",
                    "System operating normally"
                )
        }
    }
}
