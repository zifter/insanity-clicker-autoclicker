from datetime import datetime, timedelta


class SchedulePeriod:
    def __init__(self, period: timedelta, offset: timedelta = timedelta(), single_shot=False):
        self.period = period
        self.offset = offset
        self.single_shot: bool = single_shot
        self.next_trigger_time: datetime = datetime.now() + offset

    def reset(self):
        self.next_trigger_time: datetime = datetime.now() + self.offset

    def request_early_trigger(self):
        self.next_trigger_time = datetime.min

    async def try_trigger(self, dt) -> bool:
        if dt >= self.next_trigger_time:
            if self.single_shot:
                self.next_trigger_time = datetime.max
            else:
                self.next_trigger_time = dt + self.period

            return True

        return False

    def __str__(self):
        return f'SchedulePeriod {self.next_trigger_time}'


class ScheduledTask(SchedulePeriod):
    def __init__(self, period: timedelta, on_trigger, offset: timedelta = timedelta(), single_shot=False):
        super().__init__(period, offset, single_shot=single_shot)
        self.on_trigger = on_trigger

    async def try_trigger(self, dt) -> bool:
        if await super().try_trigger(dt):
            await self.on_trigger()
            return True

        return False

    def __str__(self):
        return f'{self.on_trigger.__name__} at {self.next_trigger_time}'
