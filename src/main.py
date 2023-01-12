import logging
from logging.config import fileConfig

from autoclicker import Runner

fileConfig('logging.ini')


import asyncio

from gracefull_shutdown import ExitSignalHandler

from insanity_clicker import InsanityClickerApp


logger = logging.getLogger('main')


async def main():
    app = InsanityClickerApp.create()
    clicker = Runner(app)

    shutdown = ExitSignalHandler()
    await clicker.run(shutdown)


if __name__ == '__main__':
    asyncio.run(main())
