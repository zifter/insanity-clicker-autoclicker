import logging

import pyautogui

from .base import GUIBase


logger = logging.getLogger('pyautogui-impl')


class PyAutoGUIImpl(GUIBase):
    async def press_key(self, key_name: str):
        pyautogui.press(key_name)

    async def locate_on_screen(self, image: str):  # -> PIL.Image.Image:
        return pyautogui.locateOnScreen(image)

    def debug(self):
        logger.info('List of KEYBOARD')
        logger.info(pyautogui.KEYBOARD_KEYS)
