import asyncio
from datetime import timedelta, datetime
from typing import List

from gui.base import Point
from insanity_clicker.window.window_main import MainWindow
from autoclicker.crontask import CronTask
from autoclicker.logger import logger
from insanity_clicker import InsanityClickerApp
from .base import StrategyBase
from .enhancement import Enhancement
from .utils import KeyboardActionStack


class StrategyMain(StrategyBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.tasks: List[CronTask] = [
            CronTask(timedelta(minutes=2, seconds=35), self.trigger_perks_in_order),
            CronTask(timedelta(seconds=30), self.try_to_find_and_open_chest),
            CronTask(timedelta(seconds=1), self.enhance_monster),
        ]

        self.main_window: MainWindow | None = None
        self.enhancement: Enhancement | None = None

        self.click_target: KeyboardActionStack | None = None
        self.default_click_target: Point | None = None

    async def on_start(self):
        logger.info('Start insanity clicker auto clicker!')

        self.main_window = self.app.switch_to_main_window()
        self.enhancement = Enhancement(self.main_window)
        self.click_target = KeyboardActionStack(self.main_window.click, self.main_window.key_action)
        self.default_click_target = await self.main_window.center_of_monster()

        await self.main_window.turn_on_automatic_progress()

        self.main_window.click = self.click_override
        self.main_window.key_action = self.key_action_override

    async def run_impl(self, shutdown):
        await self._run_fixed_click_rate(shutdown)

    async def click_override(self, *args):
        self.click_target.push_click(*args)

    async def key_action_override(self, *args):
        self.click_target.push_key_action(*args)

    async def _run_fixed_click_rate(self, shutdown):
        while not shutdown.triggered:
            data = self.click_target.pop()
            if data is None:
                await self.main_window.gui.click(self.default_click_target)
                await asyncio.sleep(0.02)
            else:
                action, args = data
                await action(*args)
                await asyncio.sleep(0.1)

    async def enhance_monster(self):
        await self.enhancement.beat()

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

    async def try_to_find_and_open_chest(self):
        logger.debug('Try to find chest and open')

        await self.main_window.try_find_chest_and_click()
