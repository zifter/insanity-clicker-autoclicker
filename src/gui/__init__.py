from gui.base import GUIBase


def create_gui() -> GUIBase:
    from gui.pyautogui_impl import PyAutoGUIImpl
    return PyAutoGUIImpl()
