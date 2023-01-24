from typing import List

from PIL import Image

from common.res import get_res_path, load_image
from gui.base import Point, GUIBase

from insanity_clicker.logger import logger
from insanity_clicker.stats import AppStats


class WindowBase:
    def __init__(self, gui: GUIBase, stats: AppStats):
        self.gui: GUIBase = gui
        self.stats: AppStats = stats

    async def click(self, p: Point):
        logger.debug('click on %s', p)

        await self.gui.click(p)

        self.stats.click()

    async def q_down(self):
        await self.key_action('q', 'down')

    async def q_up(self):
        await self.key_action('q', 'up')

    async def key_action(self, key_name: str, action: str):
        logger.debug('%s %s', key_name, action)

        if action == 'up':
            await self.gui.key_up(key_name)
        elif action == 'down':
            await self.gui.key_down(key_name)
        else:
            assert False, action

        self.stats.press_key()

    async def load_image(self, image_path: str) -> Image.Image:
        return load_image(get_res_path()/image_path)

    async def locate_on_screen(self, image_path: str, **kwargs) -> List[Point]:
        screenshot = await self.gui.screenshot(None)
        img = await self.load_image(image_path)
        return await self.gui.locate_all(img, screenshot, **kwargs)

    async def _try_find_and_click_on_button(self, button_image_name: str, confidence=0.95) -> bool:
        positions = await self.locate_on_screen(button_image_name, confidence=confidence)
        if positions:
            p = positions[0]
            await self.click(p)
            return True

        return False
