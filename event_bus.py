import asyncio


class EventBus:

    def __init__(self):
        self.listeners = {}


    def subscribe(self, event_name, callback):
        if event_name not in self.listeners:
            self.listeners[event_name] = []

        self.listeners[event_name].append(callback)


    async def publish(self, event_name, data):
        callbacks = self.listeners.get(event_name, [])

        results = []

        for callback in callbacks:

            if asyncio.iscoroutinefunction(callback):
                result = await callback(data)
            else:
                result = callback(data)

            results.append(result)


        return {
            "event": event_name,
            "listeners": len(callbacks),
            "results": results
        }
