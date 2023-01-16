from gui.base import Point

from insanity_clicker.logger import logger
from .window_base import WindowBase


class MainWindow(WindowBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def center_of_monster(self) -> Point | None:
        positions = await self.locate_on_screen('level_text.png', confidence=0.95)
        if positions:
            p = positions[0]
            return Point(int(p.x), int(p.y)+400)
        return None

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

    async def amnesia(self) -> bool:
        logger.info('!!! Amnesia !!!')

        if await self._try_find_and_click_on_button('btn_amnesia.png'):
            logger.debug('amnesia is pressed')

            return await self.press_dialog_button_yes()

        return False

    async def press_dialog_button_yes(self) -> bool:
        logger.info('Press dialog button YES')

        if await self._try_find_and_click_on_button('btn_dialog_yes.png'):
            return True

        return False

    async def monster_scroll_up(self) -> bool:
        logger.info('scroll up level')

        return await self._try_find_and_click_on_button('btn_scroll_up.png')

    async def monster_scroll_down(self) -> bool:
        logger.info('scroll up level')

        return await self._try_find_and_click_on_button('btn_scroll_down.png')