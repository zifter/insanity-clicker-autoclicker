from typing import List

from PIL import Image

from common import get_res_path, load_image
from gui.base import Point, GUIBase

from .logger import logger
from .stats import Stats


class WindowBase:
    def __init__(self, gui: GUIBase, stats: Stats):
        self.gui: GUIBase = gui
        self.stats: Stats = stats

    def click(self, p: Point):
        logger.info('click on %s', p)

        self.click_impl(p)

        self.stats.clicks += 1

    def click_impl(self, p: Point):
        self.gui.click(p)

    def load_image(self, image_path: str) -> Image.Image:
        return load_image(get_res_path()/image_path)

    def locate_on_screen(self, image_path: str, **kwargs) -> List[Point]:
        screenshot = self.gui.screenshot(None)
        img = self.load_image(image_path)
        return self.gui.locate_all(img, screenshot, **kwargs)

    async def _try_find_and_click_on_button(self, button_image_name: str, confidence=0.95) -> bool:
        positions = self.locate_on_screen(button_image_name, confidence=confidence)
        if positions:
            p = positions[0]
            self.gui.click(p)
            return True

        return False

    async def _find_and_click_on_all_buttons(self, button_image_name, confidence=0.95, sort=sorted) -> int:
        positions = self.locate_on_screen(button_image_name, confidence=confidence)
        positions = sort(positions)
        for p in positions:
            self.click(p)

        return len(positions)
