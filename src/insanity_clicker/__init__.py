import logging
from enum import Enum

import gui
from common import get_res_path
from gui.base import GUIBase
from insanity_clicker.chest import Chest

logger = logging.getLogger('insanity-clicker')


class InstanityClickerApp:
    class PERK(Enum):
        FLURRY_OF_BLOWS_1 = 1
        TITAN_STRENGTH_2 = 2
        WEAK_SPOT_3 = 3
        TEETH_KNOCKER_5 = 4
        BROKEN_JAWS_5 = 5
        HELLISH_RITUAL_6 = 6
        INSANE_RAGE_7 = 7
        LENS_OF_DARKNESS_8 = 8
        MAD_HATTERS_CLOCKS_9 = 9

    @staticmethod
    def create():
        return InstanityClickerApp(gui.create_gui_impl())

    def __init__(self, gui):
        self.gui: GUIBase = gui

    async def use_perk(self, perk):
        logger.info('Use perk %s', perk.name)

        await self.gui.press_key(str(perk.value))

    async def find_chest(self) -> Chest | None:
        logger.debug('find chest')
        positions = await self.gui.locate_on_screen(get_res_path() / 'chest_part.png')
        if positions:
            pos = positions[0]
            logger.debug('chest is found')
            return Chest(pos)

        logger.debug('chest is not found')
        return None

    async def turn_on_automatic_progress(self) -> bool:
        logger.info('Try to turn on automatic progress')
        positions = await self.gui.locate_on_screen(get_res_path() / 'btn_auto_progress.png')
        if positions:
            pos = positions[0]
            logger.debug('turn on automatic progress')
            await self.gui.click(pos.x, pos.y)
            return True

        return False

    async def click(self, x, y):
        logger.info('click on %s, %s', x, y)

        await self.gui.click(x, y)

    async def click_level_up(self) -> int:
        logger.info('Click level up')
        positions = await self.gui.locate_on_screen(get_res_path() / 'btn_level_up.png')
        for pos in positions:
            await self.gui.click(pos.x, pos.y)

        return len(positions)
