from datetime import timedelta, datetime

from insanity_clicker.main_window import MainWindow
from .crontask import CronTask
from .logger import logger
from insanity_clicker import InsanityClickerApp


class BaseStrategy:
    def __init__(self, app: InsanityClickerApp):
        self.app: InsanityClickerApp = app

    async def start(self):
        pass

    async def stop(self):
        pass

    async def beat(self) -> bool:
        return False


class MainStrategy(BaseStrategy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.tasks = [
            CronTask(timedelta(minutes=2, seconds=35), self.trigger_perks_in_order),
            CronTask(timedelta(seconds=30), self.try_find_and_open_chest),
            CronTask(timedelta(seconds=5), self.try_level_up),
        ]

        self.main_window: MainWindow | None = None

    async def start(self):
        logger.info('Start insanity clicker auto clicker!')

        self.main_window = self.app.switch_to_main_window()

        await self.main_window.turn_on_automatic_progress()

        now = datetime.now()
        for task in self.tasks:
            task.schedule(now)

    async def stop(self):
        pass

    async def beat(self) -> bool:
        now = datetime.now()
        for task in self.tasks:
            await task.try_trigger(now)

        return True

    async def trigger_perks_in_order(self):
        logger.debug('trigger perks')

        # https://steamcommunity.com/sharedfiles/filedetails/?id=705525781
        for i in [
            InsanityClickerApp.PERK.FLURRY_OF_BLOWS_1,
            InsanityClickerApp.PERK.TITAN_STRENGTH_2,
            InsanityClickerApp.PERK.WEAK_SPOT_3,
            InsanityClickerApp.PERK.TEETH_KNOCKER_5,
            InsanityClickerApp.PERK.BROKEN_JAWS_5,
            InsanityClickerApp.PERK.MAD_HATTERS_CLOCKS_9,
            InsanityClickerApp.PERK.LENS_OF_DARKNESS_8,
            InsanityClickerApp.PERK.INSANE_RAGE_7,
            # InstanityClickerApp.Perk.BROKEN_JAWS_5,  # again, after 30 seconds
        ]:
            await self.main_window.use_perk(i)

    async def try_find_and_open_chest(self):
        logger.debug('try_find_and_open_chest')

        await self.main_window.try_find_chest_and_click()

    async def try_level_up(self):
        logger.debug('try click level up')

        await self.main_window.click_level_up()
