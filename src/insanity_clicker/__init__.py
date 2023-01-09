import logging
from enum import Enum

import gui
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
        screenshot = await self.gui.locate_on_screen('chest.png')
        return None

    async def turn_on_automatic_progress(self) -> bool:
        logger.info('Try to turn on automatic progress')
        return False
