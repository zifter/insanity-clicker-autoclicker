import pytest

from gui import GUIBase
from unittest.mock import AsyncMock, call

from gui.base import Point
from insanity_clicker.window.window_main import MainWindow
from insanity_clicker.stats import AppStats


@pytest.mark.asyncio
async def test_turn_on_auto_progress():
    stats = AppStats()

    pos = [
        Point(25, 25)
    ]
    gui = GUIBase()
    gui.click = AsyncMock()
    gui.locate_all = AsyncMock(return_value=pos)

    mw = MainWindow(gui, stats)
    await mw.turn_on_automatic_progress()

    calls = [
        call(pos[0]),
    ]
    gui.click.assert_has_calls(calls, any_order=True)
