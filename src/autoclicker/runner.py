import logging

from autoclicker.logger import logger
from autoclicker.strategy.strategy_enhancement import StrategyEnhancement, StrategyBase
from autoclicker.strategy.strategy_walkthrough import StrategyWalkthrough
from insanity_clicker import InsanityClickerApp


class Runner:
    def __init__(self, app: InsanityClickerApp):
        self.app: InsanityClickerApp = app
        self.strategy: StrategyWalkthrough = StrategyWalkthrough(self.app)

    async def run(self, shutdown):
        logging.info('Start insanity clicker auto clicker!')

        await self.strategy.run(shutdown)

        logger.info('Finished clicker')

        logger.info('Stats:\n%s', self.app.stats)
