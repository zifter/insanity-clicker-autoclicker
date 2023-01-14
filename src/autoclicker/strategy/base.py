from insanity_clicker import InsanityClickerApp


class StrategyBase:
    def __init__(self, app: InsanityClickerApp):
        self.app: InsanityClickerApp = app

    async def start(self):
        pass

    async def on_stop(self):
        pass

    async def run(self, shutdown) -> bool:
        return False
