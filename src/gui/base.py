import abc
from pathlib import Path
from typing import List


class Point:
    x: int
    y: int


class GUIBase:
    def __init__(self):
        pass

    @abc.abstractmethod
    async def press_key(self, key_name: str):
        pass

    @abc.abstractmethod
    async def locate_on_screen(self, image_path: Path) -> List[Point]:
        pass

    @abc.abstractmethod
    async def click(self, p: Point):
        pass

    @abc.abstractmethod
    async def move_to(self, p: Point):
        pass

    @abc.abstractmethod
    async def position(self) -> Point:
        pass

    @abc.abstractmethod
    def debug(self):
        pass
