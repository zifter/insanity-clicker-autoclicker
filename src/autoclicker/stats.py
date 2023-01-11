class Stats:

    def __init__(self):
        self.opened_chest = 0
        self.level_ups = 0
        self.triggered_perks = 0

    def __str__(self):
        return f"Chests: {self.opened_chest}\n" \
               f"Level ups: {self.level_ups}\n" \
               f"Perks: {self.triggered_perks}\n"
