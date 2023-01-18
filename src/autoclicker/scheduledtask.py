from datetime import datetime, timedelta


class ScheduledTask:
    def __init__(self, delta: timedelta, on_trigger, initial_offset: timedelta | None = None, single_shot=False):
        self.delta = delta
        self.initial_offset: datetime | None = initial_offset
        self.on_trigger = on_trigger
        self.next_trigger_time: datetime | None = None
        self.single_shot: bool = single_shot

    def _get_next_trigger_time(self, dt) -> datetime:
        return dt + self.delta

    def schedule(self, dt):
        self.next_trigger_time = dt
        if self.initial_offset:
            self.next_trigger_time += self.initial_offset

    def request_early_trigger(self):
        self.next_trigger_time = datetime.min

    async def try_trigger(self, dt) -> bool:
        if dt >= self.next_trigger_time:
            self.next_trigger_time = self._get_next_trigger_time(dt)
            await self.on_trigger()
            return True

        return False
