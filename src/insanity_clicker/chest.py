class Chest:
    def __init__(self, point):
        self.pos = point

    @property
    def x(self) -> int:
        return self.pos.x

    @property
    def y(self) -> int:
        return self.pos.y
