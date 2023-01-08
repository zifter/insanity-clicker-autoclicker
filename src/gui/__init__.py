from gui.base import GUIBase
from gui.pyautogui_impl import PyAutoGUIImpl


def create_gui_impl() -> GUIBase:
    return PyAutoGUIImpl()
