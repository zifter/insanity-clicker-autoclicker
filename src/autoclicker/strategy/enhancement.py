import datetime
import random
from enum import Enum

from autoclicker.logger import logger
from autoclicker.scheduledtask import SchedulePeriod
from autoclicker.state_machine import StateData, Meta, StateMachine
from gui.base import Point
from insanity_clicker.window.window_main import MainWindow


class Enhancement:
    class State(Enum):
        WAIT = 0
        ENHANCE = 1
        LEVEL_UP = 2
        BUY_PERK = 2
        SCROLL_UP = 3
        SCROLL_DOWN = 4
        LEVEL_UP_OLD = 6

    def __init__(self, main_window: MainWindow):
        super().__init__()

        self.main_window: MainWindow = main_window

        self.state_machine = StateMachine(Enhancement.State.ENHANCE)
        self.state_machine.add_state(Enhancement.State.WAIT, self.state_wait)
        self.state_machine.add_state(Enhancement.State.ENHANCE, self.state_enhance)
        self.state_machine.add_state(Enhancement.State.BUY_PERK, self.state_buy_perk)
        self.state_machine.add_state(Enhancement.State.SCROLL_UP, self.state_scroll_up)
        self.state_machine.add_state(Enhancement.State.SCROLL_DOWN, self.state_scroll_down)
        self.state_machine.add_state(Enhancement.State.LEVEL_UP_OLD, self.state_level_up_old)

        self.buy_perk_task: SchedulePeriod = SchedulePeriod(datetime.timedelta(minutes=4),
                                                            offset=datetime.timedelta(seconds=35))
        self.level_up_old_task: SchedulePeriod = SchedulePeriod(datetime.timedelta(minutes=1),
                                                                offset=datetime.timedelta(seconds=60))

    def wait_and_move_to(self, seconds, next_state_data: StateData):
        return StateData(
            state=Enhancement.State.WAIT,
            wait_seconds=seconds, next_state_data=next_state_data)

    async def state_wait(self, meta: Meta):
        if meta['wait_seconds'] <= 1:
            return meta.next_state_data

        meta['wait_seconds'] -= 1

    async def state_scroll_up(self, meta: Meta):
        clicks = meta.setdefault('clicks', 1)
        for _ in range(clicks):
            await self.main_window.monster_scroll_up()

        return self.wait_and_move_to(2, meta.next_state_data)

    async def state_scroll_down(self, meta: Meta):
        clicks = meta.setdefault('clicks', 1)
        for _ in range(clicks):
            await self.main_window.monster_scroll_down()

        return self.wait_and_move_to(2, meta.next_state_data)

    async def state_buy_perk(self, meta: Meta):
        logger.debug('buy perk')

        screenshot = await self.main_window.gui.screenshot(None)
        monster_lvl_img = await self.main_window.load_image('part_monster_lvl.png')
        perk_amnesia_img = await self.main_window.load_image('part_perk_amnesia.png')

        perk_amnesia_pos = await self.main_window.gui.locate_all(perk_amnesia_img, screenshot)
        ignore_pos = None
        if perk_amnesia_pos:
            ignore_pos = perk_amnesia_pos[0]

        lvl_pos = await self.main_window.gui.locate_all(monster_lvl_img, screenshot)
        for pos in lvl_pos:
            first_perk_pos = Point(int(pos.x) - 100, int(pos.y) + 28)
            for i in range(7):
                p = Point(first_perk_pos.x + i*38, first_perk_pos.y)
                if ignore_pos and p.is_near(ignore_pos):
                    logger.warning('Ignore amnesia perk')
                    break

                await self.main_window.click(p)

        return self.wait_and_move_to(2, meta.next_state_data)

    async def state_enhance(self, meta: Meta):
        logger.info('try click level up or hire')
        screenshot = await self.main_window.gui.screenshot(None)

        hire_img = await self.main_window.load_image('btn_hire.png')
        level_up_img = await self.main_window.load_image('btn_level_up.png')

        level_up_pos = await self.main_window.gui.locate_all(level_up_img, screenshot, confidence=0.95)
        level_up_pos = sorted(level_up_pos, key=lambda v: v.y, reverse=True)

        hire_pos = await self.main_window.gui.locate_all(hire_img, screenshot, confidence=0.95)
        hire_pos = sorted(hire_pos, key=lambda v: v.y, reverse=True)

        wait_seconds = min(meta.setdefault('enhance_wait', 1)*2, 16)
        if hire_pos:
            wait_seconds = 1
            for p in hire_pos:
                logger.info('Click on hire')
                await self.main_window.click(p)
                self.main_window.stats.hired += 1

            self.buy_perk_task.reset()
            self.level_up_old_task.reset()

        if level_up_pos:
            wait_seconds = 2

            logger.info('Click on level up with ctrl')
            await self.main_window.q_down()

            for p in level_up_pos:
                await self.main_window.click(p)
                self.main_window.stats.level_ups += 1

            await self.main_window.q_up()

        dt = datetime.datetime.now()
        if await self.buy_perk_task.try_trigger(dt):
            return self.wait_and_move_to(5, StateData(
                Enhancement.State.BUY_PERK,
                next_state_data=StateData(
                    Enhancement.State.SCROLL_DOWN,
                    next_state_data=StateData(
                        Enhancement.State.ENHANCE,
                    ))))

        if await self.level_up_old_task.try_trigger(dt):
            clicks = random.randint(1, 5)
            return StateData(
                        Enhancement.State.SCROLL_UP,
                        clicks=clicks,
                        next_state_data=StateData(
                            Enhancement.State.LEVEL_UP_OLD,
                            next_state_data=StateData(
                                Enhancement.State.SCROLL_DOWN,
                                clicks=clicks,
                                next_state_data=StateData(Enhancement.State.ENHANCE)
                            )
                        )
                    )

        return self.wait_and_move_to(wait_seconds, StateData(Enhancement.State.ENHANCE, enhance_wait=wait_seconds))

    async def state_level_up_old(self, meta: Meta):
        logger.info('level up old')

        screenshot = await self.main_window.gui.screenshot(None)
        level_up_img = await self.main_window.load_image('btn_level_up.png')
        level_up_pos = await self.main_window.gui.locate_all(level_up_img, screenshot, confidence=0.95)

        if level_up_pos:
            logger.info('Click on level up with ctrl')
            await self.main_window.q_down()

            for p in level_up_pos:
                await self.main_window.click(p)
                self.main_window.stats.level_ups += 1

            await self.main_window.q_up()

        return meta.next_state_data

    async def beat(self):
        await self.state_machine.process()
