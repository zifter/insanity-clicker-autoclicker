from datetime import timedelta
from typing import List

from autoclicker.crontask import CronTask
from autoclicker.logger import logger
from .base import StrategyBase
from .strategy_enhancement import StrategyEnhancement


class StrategyWalkthrough(StrategyBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        delta = timedelta(hours=4, seconds=0)
        self.tasks: List[CronTask] = [
            CronTask(delta, self.trigger_amnesia, initial_offset=delta),
        ]

        self.active_strategy: StrategyBase | None = None

    async def on_start(self):
        logger.info('start walkthrough')

        main_window = self.app.switch_to_main_window()
        self.active_strategy = StrategyEnhancement(main_window, self.app)

    async def run_impl(self, shutdown):
        await self.active_strategy.run(shutdown)

    async def trigger_amnesia(self):
        main_window = self.app.switch_to_main_window()
        await main_window.amnesia()
