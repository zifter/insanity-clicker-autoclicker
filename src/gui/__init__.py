from gui.base import GUIBase


def create_gui_impl() -> GUIBase:
    from gui.pyautogui_impl import PyAutoGUIImpl
    return PyAutoGUIImpl()
