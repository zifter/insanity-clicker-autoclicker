import abc


class GUIBase:
    def __init__(self):
        pass

    @abc.abstractmethod
    async def press_key(self, key_name: str):
        pass

    @abc.abstractmethod
    async def locate_on_screen(self, image):
        pass

    @abc.abstractmethod
    def debug(self):
        pass
