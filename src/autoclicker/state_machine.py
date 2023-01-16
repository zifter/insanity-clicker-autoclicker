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
    def __init__(self, initial_state):
        self.actual_state = initial_state
        self.states = {}

    def add_state(self, state, func):
        self.states[state] = StateDescr(func, Meta())

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
