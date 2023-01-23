from enum import Enum

from autoclicker.logger import logger


class StateData:
    def __init__(self, state, **kwargs):
        self.state = state
        self.meta = Meta(**kwargs)

    def __str__(self):
        return f'{self.state}[{self.meta}]'

    def __repr__(self):
        return f'{self.state}[{self.meta}]'


class Meta(dict):
    @property
    def next_state_data(self) -> StateData:
        return self['next_state_data']


class StateDescr:
    def __init__(self, func, meta: Meta):
        self.func = func
        self.meta = meta


class StateMachine:
    class State(Enum):
        WAIT = 0

    def __init__(self, initial_state):
        self.deque= []
        self.actual_state = initial_state
        self.states = {}
        self.next_state: StateData | None = None

        self.add_state(StateMachine.State.WAIT, self.state_wait)

    def add_state(self, state, func):
        self.states[state] = StateDescr(func, Meta())

    async def process(self):
        data = self.states[self.actual_state]

        logger.debug('Process %s[%s]', self.actual_state, data.meta)
        new_state_data = await data.func(data.meta)
        if self.next_state:
            new_state_data = self.next_state
            self.next_state = None
        else:
            new_state_data = new_state_data

        if new_state_data is None:
            return

        if self.actual_state != new_state_data.state:
            logger.debug('switch %s -> %s', self.actual_state, new_state_data.state)

        self.switch_to_new_state(new_state_data)

    def switch_to_new_state(self, data: StateData):
        self.actual_state = data.state
        self.states[self.actual_state].meta = data.meta

    def request_next_state(self, state_data: StateData):
        self.next_state = state_data

    def wait_and_move_to(self, seconds, next_state_data: StateData):
        return StateData(
            state=StateMachine.State.WAIT,
            wait_seconds=seconds, next_state_data=next_state_data)

    async def state_wait(self, meta: Meta):
        if meta['wait_seconds'] <= 1:
            return meta.next_state_data

        meta['wait_seconds'] -= 1
