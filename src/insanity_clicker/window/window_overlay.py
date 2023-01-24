from insanity_clicker.logger import logger
from .window_base import WindowBase


class OverlayWindow(WindowBase):
    async def is_alert_activated(self) -> bool:
        logger.info('Try to find ALERT')

        return await self._try_find_and_click_on_button('part_alert.png')
