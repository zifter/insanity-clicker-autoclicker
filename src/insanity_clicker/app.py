from enum import Enum

from gui import create_gui_impl
from gui.base import GUIBase
from insanity_clicker.window.window_main import MainWindow
from .stats import Stats


class InsanityClickerApp:
    class PERK(Enum):
        FLURRY_OF_BLOWS_1 = 1
        TITAN_STRENGTH_2 = 2
        WEAK_SPOT_3 = 3
        TEETH_KNOCKER_4 = 4
        BROKEN_JAWS_5 = 5
        HELLISH_RITUAL_6 = 6
        INSANE_RAGE_7 = 7
        LENS_OF_DARKNESS_8 = 8
        MAD_HATTERS_CLOCKS_9 = 9

    @staticmethod
    def create():
        return InsanityClickerApp(create_gui_impl())

    def __init__(self, gui: GUIBase):
        self.gui: GUIBase = gui
        self.stats: Stats = Stats()

    def switch_to_main_window(self) -> MainWindow:
        return MainWindow(self.gui, self.stats)
