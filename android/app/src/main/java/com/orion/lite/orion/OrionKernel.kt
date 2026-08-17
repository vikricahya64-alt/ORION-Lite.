package com.orion.lite.orion

class OrionKernel {

    private val services = mutableMapOf<String, Any>()

    var running: Boolean = false
        private set

    var cycle: Long = 0
        private set

    fun register(name: String, service: Any) {
        services[name] = service
    }

    fun resolve(name: String): Any? {
        return services[name]
    }

    fun boot() {
        running = true
    }

    fun heartbeat() {
        if (running) {
            cycle++
        }
    }

    fun shutdown() {
        running = false
    }

    fun serviceNames(): List<String> {
        return services.keys.toList()
    }
}
