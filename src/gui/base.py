import abc
from collections import namedtuple
from pathlib import Path
from typing import List

from PIL import Image

Point = namedtuple('Point', ['x', 'y'])


class GUIBase:
    def __init__(self):
        pass

    @abc.abstractmethod
    async def press_key(self, key_name: str):
        pass

    @abc.abstractmethod
    async def key_down(self, key_name: str):
        pass

    @abc.abstractmethod
    async def key_up(self, key_name: str):
        pass

    @abc.abstractmethod
    async def screenshot(self, image_path: Path | None) -> Image.Image:
        pass

    @abc.abstractmethod
    async def locate_all(self, image_to_find: Image, screenshot: Image.Image, **kwargs) -> List[Point]:
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
