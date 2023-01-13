from contextlib import asynccontextmanager

from common import get_res_path
from gui.base import Point, GUIBase

from .logger import logger
from .stats import Stats


@asynccontextmanager
async def restore_position(gui):
    p = await gui.position()
    try:
        yield
    finally:
        await gui.move_to(p)


class WindowBase:
    def __init__(self, gui: GUIBase, stats: Stats):
        self.gui: GUIBase = gui
        self.stats: Stats = stats

    async def click(self, p: Point):
        logger.info('click on %s', p)

        await self.click_impl(p)

        self.stats.clicks += 1

    async def click_impl(self, p: Point):
        await self.gui.click(p)

    async def _try_find_and_click_on_button(self, button_image_name: str, confidence=0.95) -> bool:
        async with restore_position(self.gui):
            positions = await self.gui.locate_on_screen(get_res_path() / button_image_name, confidence)
            if positions:
                p = positions[0]
                await self.gui.click(p)
                return True

        return False

    async def _find_and_click_on_all_buttons(self, button_image_name, confidence=0.95, sort=sorted) -> int:
        async with restore_position(self.gui):
            positions = await self.gui.locate_on_screen(get_res_path() / button_image_name, confidence)
            positions = sort(positions)
            for p in positions:
                await self.click(p)

        return len(positions)
