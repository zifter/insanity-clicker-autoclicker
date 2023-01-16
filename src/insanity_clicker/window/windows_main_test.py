import pytest

from gui import GUIBase
from unittest.mock import AsyncMock, call

from gui.base import Point
from insanity_clicker.window.window_main import MainWindow
from insanity_clicker.stats import Stats


# @pytest.mark.asyncio
# async def test_level_up_points_are_sorted():
#     stats = Stats()
#
#     pos = [
#         Point(1, 1), Point(25, 25), Point(5, 5),
#     ]
#     gui = GUIBase()
#     gui.click = AsyncMock()
#     gui.locate_on_screen = AsyncMock(return_value=pos)
#
#     mw = MainWindow(gui, stats)
#     await mw.()
#
#     calls = [
#         call(pos[1]), call(pos[2]), call(pos[0])
#     ]
#     gui.click.assert_has_calls(calls, any_order=True)


@pytest.mark.asyncio
async def test_turn_on_auto_progress():
    stats = Stats()

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
