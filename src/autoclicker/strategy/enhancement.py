import asyncio
from enum import Enum

from autoclicker.logger import logger
from gui.base import Point
from insanity_clicker.window.window_main import MainWindow


class StateDescr:
    def __init__(self, func, meta):
        self.func = func
        self.meta = meta


class StateData:
    def __init__(self, state, **kwargs):
        self.state = state
        self.meta = Meta(**kwargs)

    def __str__(self):
        return f'{self.state}[{self.meta}]'

    def __repr__(self):
        return f'{self.state}[{self.meta}]'


class StateMachine:
    def __init__(self, initial_state):
        self.actual_state = initial_state
        self.states = {}

    def add_state(self, state, func):
        self.states[state] = StateDescr(func, {})

    async def process(self):
        data = self.states[self.actual_state]

        logger.debug('Process state: %s %s', self.actual_state, data.meta)
        new_state_data = await data.func(data.meta)
        if new_state_data is None:
            return

        if self.actual_state != new_state_data.state:
            logger.debug('switch state %s -> %s', self.actual_state, new_state_data.state)

        self.switch_to_new_state(new_state_data)

    def switch_to_new_state(self, data: StateData):
        self.actual_state = data.state
        self.states[self.actual_state].meta = data.meta


class Meta(dict):
    @property
    def next_state_data(self) -> StateData:
        return self['next_state_data']


class EnhancementStateMachine:
    class State(Enum):
        WAIT = 0
        ENHANCE = 1
        LEVEL_UP = 2
        BUY_PERK = 2
        SCROLL_UP = 3
        SCROLL_DOWN = 4

    def __init__(self, main_window: MainWindow):
        super().__init__()

        self.main_window: MainWindow = main_window

        self.state_machine = StateMachine(EnhancementStateMachine.State.ENHANCE)
        self.state_machine.add_state(EnhancementStateMachine.State.WAIT, self.state_wait)
        self.state_machine.add_state(EnhancementStateMachine.State.ENHANCE, self.state_enhance)
        self.state_machine.add_state(EnhancementStateMachine.State.BUY_PERK, self.state_buy_perk)
        self.state_machine.add_state(EnhancementStateMachine.State.SCROLL_UP, self.state_scroll_up)
        self.state_machine.add_state(EnhancementStateMachine.State.SCROLL_DOWN, self.state_scroll_down)

    async def wait_and_move_to(self, seconds, next_state_data: StateData):
        return StateData(
            state=EnhancementStateMachine.State.WAIT,
            wait_seconds=seconds, next_state_data=next_state_data)

    async def state_wait(self, meta: Meta):
        if meta['wait_seconds'] == 0:
            return meta.next_state_data

        meta['wait_seconds'] -= 1

    async def state_scroll_up(self, meta: Meta):
        await self.main_window.monster_scroll_up()

        return await self.wait_and_move_to(2, meta.next_state_data)

    async def state_scroll_down(self, meta: Meta):
        await self.main_window.monster_scroll_down()

        return await self.wait_and_move_to(2, meta.next_state_data)

    async def state_buy_perk(self, meta: Meta):
        logger.debug('buy perk')

        screenshot = await self.main_window.gui.screenshot(None)
        monster_lvl_img = await self.main_window.load_image('part_monster_lvl.png')

        lvl_pos = await self.main_window.gui.locate_all(monster_lvl_img, screenshot)
        for pos in lvl_pos:
            first_perk_pos = Point(int(pos.x) - 100, int(pos.y) + 28)
            for i in range(7):
                # TODO Ignore amensia
                p = Point(first_perk_pos.x + i*38, first_perk_pos.y)
                await self.main_window.click(p)

        return await self.wait_and_move_to(2, meta.next_state_data)
        # return await self.wait_and_move_to(2, StateData(EnhancementStateMachine.State.BUY_PERK))

    async def state_enhance(self, meta: Meta):
        logger.debug('try click level up or hire')
        screenshot = await self.main_window.gui.screenshot(None)

        hire_img = await self.main_window.load_image('btn_hire.png')
        level_up_img = await self.main_window.load_image('btn_level_up.png')

        level_up_pos = await self.main_window.gui.locate_all(level_up_img, screenshot, confidence=0.95)
        level_up_pos = sorted(level_up_pos, key=lambda v: v.y, reverse=True)

        hire_pos = await self.main_window.gui.locate_all(hire_img, screenshot, confidence=0.9)
        hire_pos = sorted(hire_pos, key=lambda v: v.y, reverse=True)

        next_state_data = StateData(EnhancementStateMachine.State.ENHANCE, **meta)

        wait_seconds = 10
        if hire_pos:
            wait_seconds = 1
            for p in hire_pos:
                logger.info('Click on hire')
                await self.main_window.click(p)
                self.main_window.stats.hired += 1
            next_state_data.meta['hired'] = True
        else:
            if 'hired' in meta:
                next_state_data.meta['switch_to_buy_perk_counter'] = 10

        if level_up_pos:
            wait_seconds = 1

            logger.info('Click on level up with ctrl')
            await self.main_window.ctrl_down()

            for p in level_up_pos:
                await self.main_window.click(p)
                self.main_window.stats.level_ups += 1

            await self.main_window.ctrl_up()

        if 'switch_to_buy_perk_counter' in meta:
            counter = meta['switch_to_buy_perk_counter']
            if counter == 0:
                del next_state_data.meta['switch_to_buy_perk_counter']
                next_state_data = StateData(
                    EnhancementStateMachine.State.BUY_PERK,
                    next_state_data=StateData(EnhancementStateMachine.State.SCROLL_DOWN, next_state_data=next_state_data)
                )
            else:
                next_state_data.meta['switch_to_buy_perk_counter'] = counter-1

        return await self.wait_and_move_to(wait_seconds, next_state_data)

    async def beat(self):
        await self.state_machine.process()
