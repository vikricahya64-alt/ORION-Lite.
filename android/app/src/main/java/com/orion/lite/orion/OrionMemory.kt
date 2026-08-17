package com.orion.lite.orion

import android.content.Context
import org.json.JSONObject

data class MemoryRecord(
    val timestamp: Long,
    val battery: Int,
    val state: String,
    val actionId: String,
    val safety: String,
    val result: String
)

class OrionMemory(
    context: Context
) {

    private val preferences =
        context.getSharedPreferences(
            "orion_memory",
            Context.MODE_PRIVATE
        )

    fun remember(record: MemoryRecord) {

        val json = JSONObject().apply {
            put("timestamp", record.timestamp)
            put("battery", record.battery)
            put("state", record.state)
            put("action", record.actionId)
            put("safety", record.safety)
            put("result", record.result)
        }

        preferences.edit()
            .putString("last_event", json.toString())
            .apply()
    }

    fun recall(): MemoryRecord? {

        val raw =
            preferences.getString(
                "last_event",
                null
            ) ?: return null

        return try {

            val json = JSONObject(raw)

            MemoryRecord(
                timestamp =
                    json.getLong("timestamp"),
                battery =
                    json.getInt("battery"),
                state =
                    json.getString("state"),
                actionId =
                    json.getString("action"),
                safety =
                    json.getString("safety"),
                result =
                    json.getString("result")
            )

        } catch (_: Exception) {
            null
        }
    }
}
