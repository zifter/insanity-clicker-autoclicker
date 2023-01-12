import asyncio
import logging

from autoclicker.logger import logger
from autoclicker.strategy import MainStrategy, BaseStrategy
from insanity_clicker import InsanityClickerApp


class Runner:
    def __init__(self, app: InsanityClickerApp):
        self.app: InsanityClickerApp = app
        self.active_strategy: BaseStrategy | None = None

    async def run(self, shutdown):
        logging.info('Start insanity clicker auto clicker!')

        self.active_strategy = MainStrategy(self.app)
        await self.active_strategy.start()
        while not shutdown.triggered and await self.active_strategy.beat():
            await asyncio.sleep(1)
        await self.active_strategy.stop()

        logger.info('Finished clicker')

        logger.info('Stats:\n%s', self.app.stats)
