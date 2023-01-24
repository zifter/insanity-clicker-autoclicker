import asyncio
import datetime

from common.res import walkthrough_dir
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

        self.stats.use_perk()

        await self.gui.press_key(str(perk.value))

    async def try_find_chest_and_click(self) -> bool:
        logger.info('find chest')
        if await self._try_find_and_click_on_button('chest_part.png'):
            self.stats.open_chest()
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
        logger.warning('!!!!!!!!!!!!!!!')
        logger.warning('!!! Amnesia !!!')

        dt = format(datetime.datetime.now(), '%m%d%H%M')
        filename = f'amnesia_{dt}v.png'
        await self.gui.screenshot(walkthrough_dir() / filename)

        if await self._try_find_and_click_on_button('btn_amnesia.png'):
            logger.info('amnesia is invoked')

            for _ in range(5):
                await asyncio.sleep(1)
                if await self.press_dialog_button_yes():
                    self.stats.amnesia()
                    return True

        return False

    async def press_dialog_button_yes(self) -> bool:
        logger.info('Press YES on dialog button')

        return await self._try_find_and_click_on_button('btn_dialog_yes.png')

    async def press_take_teeth(self) -> bool:
        logger.info('Press take teeth button')

        return await self._try_find_and_click_on_button('btn_take_teeth.png')

    async def monster_scroll_up(self) -> bool:
        logger.info('scroll up monsters')

        return await self._try_find_and_click_on_button('btn_scroll_up.png')

    async def monster_scroll_down(self) -> bool:
        logger.info('scroll down monsters')

        return await self._try_find_and_click_on_button('btn_scroll_down.png')
