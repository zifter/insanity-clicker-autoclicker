import logging
from datetime import datetime

from autoclicker.crontask import CronTask
from autoclicker.stats import Stats
from insanity_clicker import InstanityClickerApp


logger = logging.getLogger('autocliker')


class Autoclicker:
    def __init__(self, app: InstanityClickerApp):
        self.app: InstanityClickerApp = app
        self.tasks = [
            CronTask('*/1 * * * *', self.trigger_perks_in_order),
            # CronTask('*/1 * * * *', self.try_find_and_open_chest),
        ]
        self.stats = Stats()

    async def start(self):
        logging.info('Start insanity clicker auto clicker!')

        now = datetime.now()
        for task in self.tasks:
            task.schedule(now)

    async def beat(self) -> bool:
        now = datetime.now()
        for task in self.tasks:
            await task.try_trigger(now)

        return True

    async def trigger_perks_in_order(self):
        logger.debug('Trigger buttons')

        for i in [1, 2, 3, 'h', 'e', 'l', 'l', '0']:
            await self.app.use_perk(i)

    async def try_find_and_open_chest(self):
        logger.debug('find chest')

        chest = await self.app.find_chest()
        if chest is None:
            return

        self.stats.opened_chest += 1
