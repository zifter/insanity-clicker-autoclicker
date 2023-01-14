import asyncio

from autoclicker.logger import logger
from insanity_clicker.window.window_main import MainWindow


class EnhancementStateMachine:
    def __init__(self, main_window: MainWindow):
        self.main_window: MainWindow = main_window

    async def enhance(self):
        logger.debug('try click level up or hire')
        screenshot = await self.main_window.gui.screenshot(None)
        level_up_img = await self.main_window.load_image('btn_level_up.png')
        hire_img = await self.main_window.load_image('btn_hire.png')
        level_up_pos = await self.main_window.gui.locate_all(level_up_img, screenshot)
        level_up_pos = sorted(level_up_pos, key=lambda v: v.y, reverse=True)

        hire_pos = await self.main_window.gui.locate_all(hire_img, screenshot)
        hire_pos = sorted(hire_pos, key=lambda v: v.y, reverse=True)

        for p in hire_pos:
            logger.info('Click on hire')
            await self.main_window.click(p)
            self.main_window.stats.hired += 1
            await self.main_window.monster_scroll_down()

        if level_up_pos:
            logger.info('Click on level up with ctrl')
            await self.main_window.gui.key_down('ctrl')
            await asyncio.sleep(0.2)
            for p in level_up_pos:
                await asyncio.sleep(0.02)
                await self.main_window.click(p)
                self.main_window.stats.level_ups += 1

            await self.main_window.gui.key_up('ctrl')
