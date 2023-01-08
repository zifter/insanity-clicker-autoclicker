from datetime import datetime

from croniter import croniter


class CronTask:
    def __init__(self, cron, on_trigger):
        self.cron = cron
        self.on_trigger = on_trigger
        self.next_trigger_time: datetime | None = None

    def _get_next_trigger_time(self, dt) -> datetime:
        return croniter(self.cron, dt).get_next(ret_type=datetime)

    def schedule(self, dt):
        self.next_trigger_time = self._get_next_trigger_time(dt)
        pass

    async def try_trigger(self, dt) -> bool:
        if dt > self.next_trigger_time:
            self.next_trigger_time = self._get_next_trigger_time(dt)
            await self.on_trigger()
            return True

        return False
