class Stats:

    def __init__(self):
        self.opened_chest = 0
        self.level_ups = 0
        self.used_perks = 0
        self.clicks = 0

    def __str__(self):
        return f"Chests: {self.opened_chest}\n" \
               f"Level ups: {self.level_ups}\n" \
               f"Perks: {self.used_perks}\n" \
               f"Clicks: {self.clicks}\n"