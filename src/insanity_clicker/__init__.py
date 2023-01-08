import logging

import gui
from gui.base import GUIBase
from insanity_clicker.chest import Chest

logger = logging.getLogger('insanity-clicker')


class InstanityClickerApp:
    @staticmethod
    def create():
        return InstanityClickerApp(gui.create_gui_impl())

    def __init__(self, gui):
        self.gui: GUIBase = gui

    async def use_perk(self, index):
        logger.info('Use perk %s', index)

        await self.gui.press_key(str(index))

    async def find_chest(self) -> Chest | None:
        screenshot = await self.gui.locate_on_screen('chest.png')
        return None
