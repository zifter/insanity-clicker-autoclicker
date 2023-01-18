import logging
import signal
from logging.config import fileConfig
from pathlib import Path

from pynput import keyboard

fileConfig(Path(__file__).parent / 'logging.ini')

import asyncio
from autoclicker import Runner
from insanity_clicker import InsanityClickerApp


logger = logging.getLogger('main')



async def main():
    clicker = Runner(InsanityClickerApp.create())

    def exit_gracefully(_signum, _frame):
        logger.warning("[!] got exit signal")

        clicker.stop()

    def on_press(key):
        if key == keyboard.Key.esc:
            logger.warning("[!] Esc pressed")

            clicker.stop()

        elif key == keyboard.Key.f2:
            logger.warning("F3 pressed")

            clicker.print_stats()

        elif key == keyboard.Key.f3:
            logger.warning("F3 pressed")

            clicker.amnesia()


    signal.signal(signal.SIGINT, exit_gracefully)
    signal.signal(signal.SIGTERM, exit_gracefully)

    with keyboard.Listener(on_press=on_press) as listener:
        await clicker.run()
        listener.stop()

    logger.info('finished!')


if __name__ == '__main__':
    asyncio.run(main())
