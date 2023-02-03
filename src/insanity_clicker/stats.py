class AppStats:
    def __init__(self):
        self.restarts = 0
        self.alerts = 0
        self.amnesias = 0
        self.runs = [RunStats()]

    def restart(self):
        self.restarts += 1

    def alert(self):
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

    def total_run_stats(self):
        return sum(self.runs)

    def __str__(self):
        runs_str = ''.join(f'> Run {i}:\n{str(self.runs[i])}' for i in range(len(self.runs)))
        return "==== STATS ====\n" \
               f"Amnesia: {self.amnesias}\n" \
               f"Alerts: {self.alerts}\n" \
               f"Restarts: {self.restarts}\n" \
               f"Run count: {len(self.runs)}\n" \
               f"Total:\n{self.total_run_stats()}\n" + runs_str + \
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

    def __str__(self):
        return ''.join(f'  {k}: {v}\n' for k, v in self.__dict__.items())

    def __radd__(self, other):
        if other == 0:
            tmp = RunStats()
            return tmp.__add__(self)
        else:
            return self.__add__(other)

    def __add__(self, other):
        for k, v in other.__dict__.items():
            setattr(self, k, getattr(self, k) + v)

        return self
