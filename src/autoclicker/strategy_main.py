import asyncio
from datetime import timedelta, datetime

from gui.base import Point
from insanity_clicker.window_main import MainWindow
from .crontask import CronTask
from .logger import logger
from insanity_clicker import InsanityClickerApp
from .strategy_base import StrategyBase


class ClickTarget:
    def __init__(self):
        self.default_target: Point | None = None
        self.stack = []

    def pop(self):
        if self.stack:
            return self.stack.pop()

        return self.default_target

    def push(self, p):
        self.stack.append(p)


class StrategyMain(StrategyBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.tasks = [
            CronTask(timedelta(minutes=2, seconds=35), self.trigger_perks_in_order),
            CronTask(timedelta(seconds=30), self.try_find_and_open_chest),
            CronTask(timedelta(seconds=5), self.try_level_up),
        ]

        self.main_window: MainWindow | None = None

        self.click_target = ClickTarget()

    async def start(self):
        logger.info('Start insanity clicker auto clicker!')

        self.main_window = self.app.switch_to_main_window()

        await self.main_window.turn_on_automatic_progress()
        self.main_window.click_impl = self.click_impl_override
        self.click_target.default_target = await self.main_window.center_of_monster()

        now = datetime.now()
        for task in self.tasks:
            task.schedule(now)

    async def on_stop(self):
        pass

    async def run(self, shutdown) -> bool:
        await asyncio.gather(
            self._tick_cron_tasks(shutdown),
            self._run_fixed_click_rate(shutdown),
        )
        return True

    async def click_impl_override(self, p: Point):
        self.click_target.push(p)

    async def _tick_cron_tasks(self, shutdown):
        while not shutdown.triggered:
            now = datetime.now()
            for task in self.tasks:
                await task.try_trigger(now)

            await asyncio.sleep(1)

    async def _run_fixed_click_rate(self, shutdown):
        while not shutdown.triggered:
            p = self.click_target.pop()
            if p:
                await self.app.gui.click(p)
            await asyncio.sleep(0.02)

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
