from datetime import datetime, timedelta


class CronTask:
    def __init__(self, delta: timedelta, on_trigger):
        self.delta = delta
        self.on_trigger = on_trigger
        self.next_trigger_time: datetime | None = None

    def _get_next_trigger_time(self, dt) -> datetime:
        return dt + self.delta

    def schedule(self, dt):
        self.next_trigger_time = dt

    async def try_trigger(self, dt) -> bool:
        if dt > self.next_trigger_time:
            self.next_trigger_time = self._get_next_trigger_time(dt)
            await self.on_trigger()
            return True

        return False
