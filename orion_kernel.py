from datetime import datetime
from typing import Any


class ORIONKernel:
    """
    ORION Kernel v2

    Kernel bertugas sebagai:
    - Dependency Container
    - Service Registry
    - Shared State
    - Boot Manager
    - Shutdown Manager
    """

    def __init__(self):

        self.services = {}
        self.singletons = {}

        self.state = {
            "boot_time": datetime.now().isoformat(),
            "running": False,
            "cycle": 0,
            "version": "3.0.0"
        }

        print("ORION KERNEL INITIALIZED")

    # =======================================
    # SERVICE REGISTRY
    # =======================================

    def register(self, name: str, service: Any):

        self.services[name] = service

        return service

    # =======================================
    # SINGLETON REGISTRY
    # =======================================

    def singleton(self, name: str, instance: Any):

        self.singletons[name] = instance

        return instance

    # =======================================
    # RESOLVE
    # =======================================

    def resolve(self, name: str):

        if name in self.singletons:
            return self.singletons[name]

        return self.services.get(name)

    # =======================================
    # STATE
    # =======================================

    def set(self, key, value):

        self.state[key] = value

    def get(self, key, default=None):

        return self.state.get(key, default)

    # =======================================
    # BOOT
    # =======================================

    def boot(self):

        self.state["running"] = True

        print("ORION KERNEL ONLINE")

    # =======================================
    # HEARTBEAT
    # =======================================

    def heartbeat(self):

        self.state["cycle"] += 1

        return {
            "cycle": self.state["cycle"],
            "running": self.state["running"],
            "services": list(self.services.keys()),
            "singletons": list(self.singletons.keys()),
            "time": datetime.now().isoformat()
        }

    # =======================================
    # SHUTDOWN
    # =======================================

    def shutdown(self):

        self.state["running"] = False

        print("ORION KERNEL SHUTDOWN")
