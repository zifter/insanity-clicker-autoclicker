import logging
from pathlib import Path

import pyautogui

from .base import GUIBase


logger = logging.getLogger('pyautogui-impl')


class PyAutoGUIImpl(GUIBase):
    async def press_key(self, key_name: str):
        logger.info('Press key %s', key_name)
        pyautogui.press(key_name)

    async def locate_on_screen(self, image_path: Path):  # -> PIL.Image.Image:
        return pyautogui.locateCenterOnScreen(str(image_path), step=5, confidence=0.9)

    async def click(self, x: int, y: int):
        pyautogui.click(x, y)

    def debug(self):
        logger.info('List of KEYBOARD')
        logger.info(pyautogui.KEYBOARD_KEYS)
