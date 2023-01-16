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
        SWITCH_TO_ENHANCEMENT = 1
        ENHANCEMENT = 2
        AMNESIA = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        delta = timedelta(hours=4, seconds=0)
        self.tasks: List[ScheduledTask] = [
            ScheduledTask(delta, self.trigger_amnesia, initial_offset=delta),
        ]

        self.active_strategy: StrategyBase | None = None

        self.state_machine = StateMachine(StrategyWalkthrough.State.SWITCH_TO_ENHANCEMENT)
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

    async def beat(self):
        await self.state_machine.process()

    def on_stop_requested(self):
        if self.active_strategy:
            self.active_strategy.request_stop()

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
