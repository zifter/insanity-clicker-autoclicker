class AppStats:
    def __init__(self):
        self.crashes = 0
        self.alerts = 0
        self.amnesias = 0
        self.runs = [RunStats()]

    def crash(self):
        self.crash += 1

    def alerts(self):
        self.alerts += 1

    def open_chest(self):
        self.runs[-1].opened_chest += 1

    def level_up(self):
        self.runs[-1].level_ups += 1

    def use_perk(self):
        self.runs[-1].used_perks += 1

    def click(self):
        self.runs[-1].clicks += 1

    def press_key(self):
        self.runs[-1].keys += 1

    def hire(self):
        self.runs[-1].hired += 1

    def bee(self):
        self.runs[-1].bee += 1

    def amnesia(self):
        self.amnesias += 1
        self.runs.append(RunStats())

    def __str__(self):
        runs_str = ''.join(f'> Run {i}:\n{str(self.runs[i])}' for i in range(len(self.runs)))
        return "==== STATS ====\n" \
               f"Amnesia: {self.amnesias}\n" \
               f"Alerts: {self.alerts}\n" \
               f"Crashes: {self.crashes}\n" \
               f"Run count: {len(self.runs)}\n" + runs_str + \
            "==== END ===="


class RunStats:
    def __init__(self):
        self.opened_chest = 0
        self.level_ups = 0
        self.used_perks = 0
        self.clicks = 0
        self.keys = 0
        self.hired = 0
        self.bee = 0
        self.crashes = 0

    def __str__(self):
        return ''.join(f'  {k}: {v}\n' for k, v in self.__dict__.items())
