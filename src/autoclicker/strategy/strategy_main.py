import asyncio
from datetime import timedelta, datetime

from gui.base import Point
from insanity_clicker.window.window_main import MainWindow
from autoclicker.crontask import CronTask
from autoclicker.logger import logger
from insanity_clicker import InsanityClickerApp
from .base import StrategyBase
from .enhancement import EnhancementStateMachine
from .utils import KeyboardActionStack


class StrategyMain(StrategyBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.tasks = [
            CronTask(timedelta(minutes=2, seconds=35), self.trigger_perks_in_order),
            CronTask(timedelta(seconds=30), self.try_find_and_open_chest),
            CronTask(timedelta(seconds=1), self.enhance_monster),
        ]

        self.main_window: MainWindow | None = None
        self.enhancement: EnhancementStateMachine | None = None

        self.click_target: KeyboardActionStack | None = None
        self.default_click_target: Point | None = None

    async def start(self):
        logger.info('Start insanity clicker auto clicker!')

        self.main_window = self.app.switch_to_main_window()
        self.enhancement = EnhancementStateMachine(self.main_window)
        self.click_target = KeyboardActionStack(self.main_window.click, self.main_window.key_action)
        self.default_click_target = await self.main_window.center_of_monster()

        await self.main_window.turn_on_automatic_progress()

        self.main_window.click = self.click_override
        self.main_window.key_action = self.key_action_override

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

    async def click_override(self, *args):
        self.click_target.push_click(*args)

    async def key_action_override(self, *args):
        self.click_target.push_key_action(*args)

    async def _tick_cron_tasks(self, shutdown):
        while not shutdown.triggered:
            now = datetime.now()
            for task in self.tasks:
                await task.try_trigger(now)

            await asyncio.sleep(1)

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

    async def try_find_and_open_chest(self):
        logger.debug('try_find_and_open_chest')

        await self.main_window.try_find_chest_and_click()
