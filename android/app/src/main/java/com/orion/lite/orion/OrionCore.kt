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
