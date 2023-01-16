import asyncio
from datetime import datetime
from typing import List

from autoclicker.crontask import CronTask
from insanity_clicker import InsanityClickerApp


class StrategyBase:
    def __init__(self, app: InsanityClickerApp):
        self.app: InsanityClickerApp = app
        self.tasks: List[CronTask] = []

    async def on_start(self):
        pass

    async def run_impl(self, shutdown):
        pass

    async def on_stop(self):
        pass

    async def beat(self):
        pass

    async def run(self, shutdown):
        now = datetime.now()
        for task in self.tasks:
            task.schedule(now)

        await self.on_start()
        await asyncio.gather(
            self._beat_loop(shutdown),
            self.run_impl(shutdown),
        )
        await self.on_stop()

    async def _beat_loop(self, shutdown):
        while not shutdown.triggered:
            now = datetime.now()
            for task in self.tasks:
                await task.try_trigger(now)

            await self.beat()
            await asyncio.sleep(1)
