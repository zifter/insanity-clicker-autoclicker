import logging
from logging.config import fileConfig
from pathlib import Path

from pynput import keyboard

fileConfig(Path(__file__).parent / 'logging.ini')

import asyncio
from gracefull_shutdown import ExitSignalHandler
from autoclicker import Runner
from insanity_clicker import InsanityClickerApp


logger = logging.getLogger('main')

shutdown = ExitSignalHandler()


def on_press(key):
    if key == keyboard.Key.esc:
        shutdown.trigger()


async def main():
    app = InsanityClickerApp.create()
    clicker = Runner(app)

    with keyboard.Listener(on_press=on_press) as listener:
        await clicker.run(shutdown)
        listener.stop()

    logger.info('finished!')


if __name__ == '__main__':
    asyncio.run(main())
