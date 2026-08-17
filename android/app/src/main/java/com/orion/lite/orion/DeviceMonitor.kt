package com.orion.lite.orion

import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.os.BatteryManager

data class DeviceState(
    val batteryPercent: Int,
    val charging: Boolean
)

class DeviceMonitor(
    private val context: Context
) {

    fun read(): DeviceState {

        val intent = context.registerReceiver(
            null,
            IntentFilter(Intent.ACTION_BATTERY_CHANGED)
        )

        if (intent == null) {
            return DeviceState(
                batteryPercent = -1,
                charging = false
            )
        }

        val level = intent.getIntExtra(
            BatteryManager.EXTRA_LEVEL,
            -1
        )

        val scale = intent.getIntExtra(
            BatteryManager.EXTRA_SCALE,
            -1
        )

        val status = intent.getIntExtra(
            BatteryManager.EXTRA_STATUS,
            -1
        )

        val percent =
            if (level >= 0 && scale > 0) {
                (level * 100) / scale
            } else {
                -1
            }

        val charging =
            status == BatteryManager.BATTERY_STATUS_CHARGING ||
            status == BatteryManager.BATTERY_STATUS_FULL

        return DeviceState(
            batteryPercent = percent,
            charging = charging
        )
    }
}
