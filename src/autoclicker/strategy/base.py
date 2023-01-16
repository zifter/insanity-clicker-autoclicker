import asyncio
from datetime import datetime
from typing import List

from autoclicker.scheduledtask import ScheduledTask
from autoclicker.logger import logger
from insanity_clicker import InsanityClickerApp


class StrategyBase:
    def __init__(self, app: InsanityClickerApp):
        self.app: InsanityClickerApp = app
        self.tasks: List[ScheduledTask] = []
        self._stop_requested: bool = False

    def add_task(self, task: ScheduledTask):
        self.tasks.append(task)

    async def on_start(self):
        pass

    async def run_impl(self):
        pass

    async def on_stop(self):
        pass

    async def beat(self):
        pass

    def request_stop(self):
        logger.info('Stop requested for %s', self)

        self._stop_requested = True

        self.on_stop_requested()

    def on_stop_requested(self):
        pass

    async def run(self):
        now = datetime.now()
        for task in self.tasks:
            task.schedule(now)

        await self.on_start()
        await asyncio.gather(
            self._beat_loop(),
            self._cron_loop(),
            self.run_impl(),
        )
        await self.on_stop()

    async def _beat_loop(self):
        while not self._stop_requested:
            await self.beat()
            await asyncio.sleep(1)

    async def _cron_loop(self):
        while not self._stop_requested:
            now = datetime.now()
            for task in self.tasks[:]:
                if await task.try_trigger(now):
                    if task.single_shot:
                        self.tasks.remove(task)

            await asyncio.sleep(1)

    def __str__(self):
        return type(self).__name__
