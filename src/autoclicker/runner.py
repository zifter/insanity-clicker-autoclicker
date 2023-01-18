import logging

from autoclicker.logger import logger
from autoclicker.strategy.strategy_walkthrough import StrategyWalkthrough
from insanity_clicker import InsanityClickerApp


class Runner:
    def __init__(self, app: InsanityClickerApp):
        self.app: InsanityClickerApp = app
        self.strategy: StrategyWalkthrough = StrategyWalkthrough(self.app)

    def stop(self):
        logger.warning("Stop autoclicker requested")

        self.strategy.request_stop()

    async def run(self):
        logging.info('Start insanity clicker auto clicker!')

        await self.strategy.run()

        logger.info('Autoclicker finished')

        self.print_stats()

    def amnesia(self):
        self.strategy.request_amnesia()

    def print_stats(self):
        logger.info('Stats:\n%s', self.app.stats)

    def debug(self):
        logger.info(f"\n{self.strategy.debug_string()}")
