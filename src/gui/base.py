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
    def press_key(self, key_name: str):
        pass

    @abc.abstractmethod
    def screenshot(self, image_path: Path | None) -> Image.Image:
        pass

    @abc.abstractmethod
    def locate_all(self, image_to_find: Image, screenshot: Image.Image, **kwargs) -> List[Point]:
        pass

    @abc.abstractmethod
    def click(self, p: Point):
        pass

    @abc.abstractmethod
    def move_to(self, p: Point):
        pass

    @abc.abstractmethod
    def position(self) -> Point:
        pass

    @abc.abstractmethod
    def debug(self):
        pass
