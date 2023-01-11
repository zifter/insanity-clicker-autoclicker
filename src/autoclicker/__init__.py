import logging
from datetime import datetime, timedelta

from autoclicker.crontask import CronTask
from autoclicker.stats import Stats
from insanity_clicker import InstanityClickerApp


logger = logging.getLogger('autocliker')


class Autoclicker:
    def __init__(self, app: InstanityClickerApp):
        self.app: InstanityClickerApp = app
        self.tasks = [
            CronTask(timedelta(minutes=2, seconds=35), self.trigger_perks_in_order),
            CronTask(timedelta(seconds=30), self.try_find_and_open_chest),
            CronTask(timedelta(seconds=5), self.try_level_up),
        ]
        self.stats = Stats()

    async def start(self):
        logging.info('Start insanity clicker auto clicker!')

        await self.app.turn_on_automatic_progress()

        now = datetime.now()
        for task in self.tasks:
            task.schedule(now)

    async def stop(self):
        logger.info('Finished clicker')

        logger.info('Stats:\n%s', self.stats)

    async def beat(self) -> bool:
        now = datetime.now()
        for task in self.tasks:
            await task.try_trigger(now)

        return True

    async def trigger_perks_in_order(self):
        logger.debug('Trigger perks')
        self.stats.triggered_perks += 1
        # https://steamcommunity.com/sharedfiles/filedetails/?id=705525781
        for i in [
            InstanityClickerApp.PERK.FLURRY_OF_BLOWS_1,
            InstanityClickerApp.PERK.TITAN_STRENGTH_2,
            InstanityClickerApp.PERK.WEAK_SPOT_3,
            InstanityClickerApp.PERK.TEETH_KNOCKER_5,
            InstanityClickerApp.PERK.BROKEN_JAWS_5,
            InstanityClickerApp.PERK.MAD_HATTERS_CLOCKS_9,
            InstanityClickerApp.PERK.LENS_OF_DARKNESS_8,
            InstanityClickerApp.PERK.INSANE_RAGE_7,
            # InstanityClickerApp.Perk.BROKEN_JAWS_5,  # again, after 30 seconds
        ]:
            await self.app.use_perk(i)

    async def try_find_and_open_chest(self):
        logger.debug('try_find_and_open_chest')

        chest = await self.app.find_chest()
        if chest is None:
            return

        await self.app.click(chest.x, chest.y)

        self.stats.opened_chest += 1

    async def try_level_up(self):
        self.stats.level_ups += await self.app.click_level_up()
