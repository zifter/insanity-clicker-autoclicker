import logging
from logging.config import fileConfig
from pathlib import Path

fileConfig(Path(__file__).parent / 'logging.ini')

import asyncio
import keyboard
from gracefull_shutdown import ExitSignalHandler
from autoclicker import Runner
from insanity_clicker import InsanityClickerApp


logger = logging.getLogger('main')


async def main():
    app = InsanityClickerApp.create()
    clicker = Runner(app)

    shutdown = ExitSignalHandler()
    try:
        keyboard.on_press_key("esc", lambda _: shutdown.trigger())
    except:
        logger.error('failed to install esc hook')
    await clicker.run(shutdown)


if __name__ == '__main__':
    asyncio.run(main())
