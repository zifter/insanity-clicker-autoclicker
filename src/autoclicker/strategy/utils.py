from gui.base import Point


class ClickTarget:
    def __init__(self):
        self.default_target: Point | None = None
        self.stack = []

    def pop(self):
        if self.stack:
            return self.stack.pop()

        return self.default_target

    def push(self, p):
        self.stack.append(p)
