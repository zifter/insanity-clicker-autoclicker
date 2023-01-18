from datetime import datetime, timedelta


class ScheduledTask:
    def __init__(self, period: timedelta, on_trigger, offset: timedelta = timedelta(), single_shot=False):
        self.delta = period
        self.on_trigger = on_trigger
        self.next_trigger_time: datetime = datetime.now() + offset

        self.single_shot: bool = single_shot

    def request_early_trigger(self):
        self.next_trigger_time = datetime.min

    async def try_trigger(self, dt) -> bool:
        if dt >= self.next_trigger_time:
            self.next_trigger_time = dt + self.delta
            await self.on_trigger()
            return True

        return False
