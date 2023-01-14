import logging

from autoclicker.logger import logger
from autoclicker.strategy.strategy_main import StrategyMain, StrategyBase
from insanity_clicker import InsanityClickerApp


class Runner:
    def __init__(self, app: InsanityClickerApp):
        self.app: InsanityClickerApp = app
        self.active_strategy: StrategyBase | None = None

    async def run(self, shutdown):
        logging.info('Start insanity clicker auto clicker!')

        self.active_strategy = StrategyMain(self.app)
        await self.active_strategy.start()
        await self.active_strategy.run(shutdown)
        await self.active_strategy.on_stop()

        logger.info('Finished clicker')

        logger.info('Stats:\n%s', self.app.stats)
