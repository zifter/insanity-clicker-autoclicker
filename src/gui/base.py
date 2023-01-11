import abc
from pathlib import Path


class GUIBase:
    def __init__(self):
        pass

    @abc.abstractmethod
    async def press_key(self, key_name: str):
        pass

    @abc.abstractmethod
    async def locate_on_screen(self, image_path: Path):
        pass

    @abc.abstractmethod
    async def click(self, x: int, y: int):
        pass

    @abc.abstractmethod
    async def move(self, x: int, y: int):
        pass

    @abc.abstractmethod
    def debug(self):
        pass
