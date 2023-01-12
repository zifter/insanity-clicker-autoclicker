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

    async def _click(self, p: Point):
        logger.info('click on %s', p)

        await self.gui.click(p)

        self.stats.clicks += 1

    async def _try_find_and_click_on_button(self, button_image_name: str) -> bool:
        async with restore_position(self.gui):
            positions = await self.gui.locate_on_screen(get_res_path() / button_image_name)
            if positions:
                p = positions[0]
                await self.gui.click(p)
                return True

        return False

    async def _find_and_click_on_all_buttons(self, button_image_name, sort=sorted) -> int:
        async with restore_position(self.gui):
            positions = await self.gui.locate_on_screen(get_res_path() / button_image_name)
            positions = sort(positions)
            for p in positions:
                await self._click(p)

        return len(positions)


class MainWindow(WindowBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def use_perk(self, perk):
        logger.info('Use perk %s', perk.name)

        self.stats.used_perks += 1

        await self.gui.press_key(str(perk.value))

    async def try_find_chest_and_click(self) -> bool:
        logger.debug('find chest')
        if await self._try_find_and_click_on_button('chest_part.png'):
            self.stats.opened_chest += 1
            logger.debug('chest found')
            return True

        return False

    async def turn_on_automatic_progress(self) -> bool:
        logger.info('Try to turn on automatic progress')

        if await self._try_find_and_click_on_button('btn_auto_progress.png'):
            logger.debug('turn on automatic progress')
            return True

        return False

    async def click_level_up(self):
        logger.info('click level up')
        sort = lambda l: sorted(l, key=lambda v: v.x)
        self.stats.level_ups += await self._find_and_click_on_all_buttons('btn_level_up.png', sort=sort)

    async def monster_scroll_up(self) -> bool:
        logger.info('scroll up level')

        return await self._try_find_and_click_on_button('btn_scroll_up.png')

    async def monster_scroll_down(self) -> bool:
        logger.info('scroll up level')

        return await self._try_find_and_click_on_button('btn_scroll_down.png')
