import logging
from pathlib import Path
from typing import List

import pyautogui

from .base import GUIBase, Point, Image

logger = logging.getLogger('pyautogui-impl')


class PyAutoGUIImpl(GUIBase):
    def __init__(self):
        super().__init__()

        pyautogui.FAILSAFE = False

    async def press_key(self, key_name: str):
        logger.info('Press key %s', key_name)
        pyautogui.press(key_name)

    async def key_down(self, key_name: str):
        pyautogui.keyDown(key_name)

    async def key_up(self, key_name: str):
        pyautogui.keyUp(key_name)

    async def screenshot(self, image_path: Path | None) -> Image:
        p = None
        if image_path:
            p = str(image_path)
        return pyautogui.screenshot(p)

    async def locate_all(self, image_to_find: Image.Image, screenshot: Image.Image, **kwargs) -> List[Point]:
        return [pyautogui.center(p) for p in pyautogui.locateAll(image_to_find, screenshot, **kwargs)]

    async def click(self, p: Point):
        pyautogui.click(p.x, p.y)

    async def position(self) -> Point:
        return pyautogui.position()

    async def move_to(self, p: Point):
        pyautogui.moveTo(p.x, p.y)

    def debug(self):
        logger.info('List of KEYBOARD')
        logger.info(pyautogui.KEYBOARD_KEYS)
