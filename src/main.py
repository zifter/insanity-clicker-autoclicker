import logging
from logging.config import fileConfig
fileConfig('logging.ini')


import asyncio

from gracefull_shutdown import ExitSignalHandler

from autoclicker import Autoclicker
from insanity_clicker import InstanityClickerApp


async def main():
    app = InstanityClickerApp.create()
    clicker = Autoclicker(app)

    await clicker.start()

    shutdown = ExitSignalHandler()
    while not shutdown.triggered and await clicker.beat():
        await asyncio.sleep(1)

    logging.info('Finished clicker')

    return True


if __name__ == '__main__':
    asyncio.run(main())