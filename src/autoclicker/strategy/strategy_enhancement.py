import asyncio
from datetime import timedelta
from typing import List

from gui.base import Point
from insanity_clicker.window.window_main import MainWindow
from autoclicker.crontask import CronTask
from autoclicker.logger import logger
from insanity_clicker import InsanityClickerApp
from .base import StrategyBase
from .enhancement import Enhancement
from .utils import KeyboardActionStack


class StrategyEnhancement(StrategyBase):
    def __init__(self, main_window, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.tasks: List[CronTask] = [
            CronTask(timedelta(minutes=2, seconds=35), self.trigger_perks, initial_offset=timedelta(seconds=5)),
            CronTask(timedelta(minutes=10), self.trigger_hellish_ritual, initial_offset=timedelta(seconds=5)),
            CronTask(timedelta(seconds=30), self.try_to_find_and_open_chest),
            CronTask(timedelta(seconds=30), self.try_to_find_bee),
        ]

        self.main_window: MainWindow = main_window
        self.enhancement: Enhancement = Enhancement(self.main_window)
        self.click_target: KeyboardActionStack = KeyboardActionStack(self.main_window.click, self.main_window.key_action)

        self.default_click_target: Point | None = None

    async def on_start(self):
        logger.info('Start insanity clicker auto clicker!')

        self.default_click_target = await self.main_window.center_of_monster()

        await self.main_window.turn_on_automatic_progress()

        self.main_window.click = self.click_override
        self.main_window.key_action = self.key_action_override

    async def run_impl(self):
        await self._run_fixed_click_rate()

    async def click_override(self, *args):
        self.click_target.push_click(*args)

    async def key_action_override(self, *args):
        self.click_target.push_key_action(*args)

    async def _run_fixed_click_rate(self):
        while not self._stop_requested:
            data = self.click_target.pop()
            if data is None:
                if self.default_click_target:
                    await self.main_window.gui.click(self.default_click_target)
                await asyncio.sleep(0.02)
            else:
                action, args = data
                await action(*args)
                await asyncio.sleep(0.1)

    async def beat(self):
        await self.enhancement.beat()

    async def try_to_find_bee(self):
        # TODO
        pass
        # await self.enhancement.beat()

    async def trigger_perks(self):
        logger.debug('trigger perks')

        # https://steamcommunity.com/sharedfiles/filedetails/?id=705525781
        for i in [
            InsanityClickerApp.PERK.FLURRY_OF_BLOWS_1,
            InsanityClickerApp.PERK.TITAN_STRENGTH_2,
            InsanityClickerApp.PERK.WEAK_SPOT_3,
            InsanityClickerApp.PERK.TEETH_KNOCKER_4,
            InsanityClickerApp.PERK.BROKEN_JAWS_5,
            InsanityClickerApp.PERK.MAD_HATTERS_CLOCKS_9,
            InsanityClickerApp.PERK.LENS_OF_DARKNESS_8,
            InsanityClickerApp.PERK.INSANE_RAGE_7,
            # InstanityClickerApp.Perk.BROKEN_JAWS_5,  # again, after 30 seconds
        ]:
            await self.main_window.use_perk(i)

    async def trigger_hellish_ritual(self):
        logger.debug('trigger hellish ritual')
        await self.main_window.use_perk(InsanityClickerApp.PERK.HELLISH_RITUAL_6)

    async def try_to_find_and_open_chest(self):
        logger.debug('Try to find chest and open')

        await self.main_window.try_find_chest_and_click()
