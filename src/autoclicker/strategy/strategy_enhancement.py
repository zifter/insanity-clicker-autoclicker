import asyncio
import datetime
from datetime import timedelta
from typing import List

from insanity_clicker.window.window_main import MainWindow
from autoclicker.scheduledtask import ScheduledTask
from autoclicker.logger import logger
from insanity_clicker import InsanityClickerApp
from .base import StrategyBase
from .enhancement import Enhancement
from .utils import KeyboardActionStack, ElapsedTime


class StrategyEnhancement(StrategyBase):
    def __init__(self, main_window, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.tasks: List[ScheduledTask] = [
            ScheduledTask(timedelta(minutes=2, seconds=35), self.trigger_perks, offset=timedelta(seconds=5)),
            ScheduledTask(timedelta(minutes=10), self.trigger_hellish_ritual, offset=timedelta(seconds=5)),
            ScheduledTask(timedelta(seconds=30), self.trigger_try_to_find_bee_and_chest),
            ScheduledTask(timedelta(minutes=10), self.trigger_auto_progress),
        ]

        self.main_window: MainWindow = main_window
        self.enhancement: Enhancement = Enhancement(self.main_window)
        self.click_target: KeyboardActionStack = KeyboardActionStack(self.main_window.click, self.main_window.key_action)

    async def on_start(self):
        logger.info('Start insanity clicker auto clicker!')

        self.click_target.push_default_target(await self.main_window.center_of_monster())

        await self.main_window.turn_on_automatic_progress()
        for _ in range(6):
            await self.main_window.monster_scroll_down()

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
            elapsed = ElapsedTime()
            sleeptime = 0.1

            data = self.click_target.pop()
            if data:
                action, args = data
                await action(*args)
            else:
                target = self.click_target.default_click_target
                if target:
                    await self.main_window.gui.click(target)
                    sleeptime = 0.05

            sleeptime = min(sleeptime - elapsed.elapsed_seconds(), 0)
            await asyncio.sleep(sleeptime)

    async def beat(self):
        await self.enhancement.beat()

    async def trigger_auto_progress(self):
        await self.main_window.turn_on_automatic_progress()

    async def trigger_perks(self):
        logger.info('Trigger perks')

        # https://steamcommunity.com/sharedfiles/filedetails/?id=705525781
        for i in [
            InsanityClickerApp.PERK.FLURRY_OF_BLOWS_1,
            InsanityClickerApp.PERK.TITAN_STRENGTH_2,
            InsanityClickerApp.PERK.TEETH_KNOCKER_4,
            InsanityClickerApp.PERK.BROKEN_JAWS_5,
            InsanityClickerApp.PERK.MAD_HATTERS_CLOCKS_9,
            InsanityClickerApp.PERK.LENS_OF_DARKNESS_8,
            InsanityClickerApp.PERK.INSANE_RAGE_7,
            InsanityClickerApp.PERK.WEAK_SPOT_3,
            # InstanityClickerApp.Perk.BROKEN_JAWS_5,  # again, after 30 seconds
        ]:
            await self.main_window.use_perk(i)
            await asyncio.sleep(0.1)

        task = ScheduledTask(
            timedelta(seconds=30),
            self.trigger_broken_jaw,
            offset=timedelta(seconds=30),
            single_shot=True)
        self.add_task(task)

    async def trigger_broken_jaw(self):
        await self.main_window.use_perk(InsanityClickerApp.PERK.BROKEN_JAWS_5)

    async def trigger_hellish_ritual(self):
        logger.debug('trigger hellish ritual')
        await self.main_window.use_perk(InsanityClickerApp.PERK.HELLISH_RITUAL_6)

    async def trigger_try_to_find_bee_and_chest(self):
        logger.debug('Try to find chest and open')

        screenshot = await self.main_window.gui.screenshot(None)

        chest_img = await self.main_window.load_image('chest_part.png')
        bee_img = await self.main_window.load_image('part_bee.png')

        chest_pos = await self.main_window.gui.locate_all(chest_img, screenshot, confidence=0.95)
        if chest_pos:
            logger.info('chest found')
            self.main_window.stats.open_chest()
            await self.main_window.click(chest_pos[0])

        bee_pos = await self.main_window.gui.locate_all(bee_img, screenshot, confidence=0.90)
        if bee_pos:
            logger.info('bee found')
            self.main_window.stats.bee()
            self.click_target.push_default_target(bee_pos[0])

            task = ScheduledTask(
                timedelta(seconds=5),
                self.trigger_pop_default_click_target,
                offset=timedelta(seconds=5),
                single_shot=True)
            self.add_task(task)

    async def trigger_pop_default_click_target(self):
        self.click_target.pop_default_target()
