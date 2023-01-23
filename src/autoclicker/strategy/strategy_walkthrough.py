import asyncio
import datetime
from datetime import timedelta
from enum import Enum
from typing import List

from autoclicker.scheduledtask import ScheduledTask
from autoclicker.logger import logger
from .base import StrategyBase
from .strategy_enhancement import StrategyEnhancement
from ..state_machine import StateMachine, Meta, StateData


class StrategyWalkthrough(StrategyBase):
    class State(Enum):
        LAUNCH_APP = 1
        SWITCH_TO_ENHANCEMENT = 2
        ENHANCEMENT = 3
        AMNESIA = 4

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        delta = timedelta(hours=1)
        self.tasks: List[ScheduledTask] = [
            ScheduledTask(delta, self.trigger_amnesia, offset=delta),
            ScheduledTask(timedelta(seconds=10), self.trigger_check_if_app_is_launched),
        ]

        self.active_strategy: StrategyBase | None = None

        self.state_machine = StateMachine(StrategyWalkthrough.State.LAUNCH_APP)
        self.state_machine.add_state(StrategyWalkthrough.State.LAUNCH_APP, self.state_launch_app)
        self.state_machine.add_state(StrategyWalkthrough.State.SWITCH_TO_ENHANCEMENT, self.state_switch_to_enhancement)
        self.state_machine.add_state(StrategyWalkthrough.State.ENHANCEMENT, self.state_enhancement)
        self.state_machine.add_state(StrategyWalkthrough.State.AMNESIA, self.state_amnesia)

    def request_amnesia(self):
        logger.warning('Request amnesia')
        self.tasks[0].request_early_trigger()

    async def trigger_amnesia(self):
        if self.state_machine.actual_state != StrategyWalkthrough.State.ENHANCEMENT:
            logger.warning('Amnesia failed - do not know how to switch from other state')

        self.active_strategy.request_stop()
        self.state_machine.request_next_state(StateData(StrategyWalkthrough.State.AMNESIA))

    async def trigger_check_if_app_is_launched(self):
        if not self.app.is_launched():
            logger.warning('Application is not running')
            self.state_machine.request_next_state(StateData(StrategyWalkthrough.State.LAUNCH_APP))

    async def beat(self):
        await self.state_machine.process()

    def on_stop_requested(self):
        if self.active_strategy:
            self.active_strategy.request_stop()

    def debug_string(self) -> str:
        debug = super().debug_string()
        debug += f'Active strategy - {self.active_strategy}\n'
        debug += self.active_strategy.debug_string()

        return debug

    async def state_launch_app(self, meta: Meta):
        if self.app.is_launched():
            return StateData(StrategyWalkthrough.State.SWITCH_TO_ENHANCEMENT)
        else:
            self.app.launch()
            return self.state_machine.wait_and_move_to(15, StateData(StrategyWalkthrough.State.SWITCH_TO_ENHANCEMENT))

    async def state_switch_to_enhancement(self, meta: Meta):
        main_window = self.app.switch_to_main_window()
        self.active_strategy = StrategyEnhancement(main_window, self.app)

        return StateData(StrategyWalkthrough.State.ENHANCEMENT)

    async def state_enhancement(self, meta: Meta):
        await self.active_strategy.run()

        return None

    async def state_amnesia(self, meta: Meta):
        main_window = self.app.switch_to_main_window()
        await main_window.amnesia()
        return StateData(StrategyWalkthrough.State.SWITCH_TO_ENHANCEMENT)
