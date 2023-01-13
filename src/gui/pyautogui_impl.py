import logging
from pathlib import Path
from typing import List

import pyautogui

from .base import GUIBase, Point

logger = logging.getLogger('pyautogui-impl')


class PyAutoGUIImpl(GUIBase):
    def __init__(self):
        super().__init__()

        # pyautogui.FAILSAFE = False

    async def press_key(self, key_name: str):
        logger.info('Press key %s', key_name)
        pyautogui.press(key_name)

    async def locate_on_screen(self, image_path: Path, confidence) -> List[Point]:
        img = str(image_path)
        return [pyautogui.center(p) for p in pyautogui.locateAllOnScreen(img, step=1, confidence=confidence)]

    async def click(self, p: Point):
        pyautogui.click(p.x, p.y)

    async def position(self) -> Point:
        return pyautogui.position()

    async def move_to(self, p: Point):
        pyautogui.moveTo(p.x, p.y)

    async def move(self, p: Point):
        pyautogui.move(p.x, p.y)

    def debug(self):
        logger.info('List of KEYBOARD')
        logger.info(pyautogui.KEYBOARD_KEYS)
