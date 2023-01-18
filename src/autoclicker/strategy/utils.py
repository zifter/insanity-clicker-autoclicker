from collections import deque
from typing import List

from gui.base import Point


class KeyboardActionStack:
    def __init__(self, click_impl, key_action_impl):
        self.single_click_stack = deque()
        self.default_click_target_stack: List[Point] = []

        self.click_impl = click_impl
        self.key_action_impl = key_action_impl

    def pop(self):
        if self.single_click_stack:
            return self.single_click_stack.popleft()

        return None

    @property
    def default_click_target(self) -> Point:
        return self.default_click_target_stack[-1]

    def push_default_target(self, p: Point):
        self.default_click_target_stack.append(p)

    def pop_default_target(self) -> Point:
        return self.default_click_target_stack.pop()

    def push_click(self, *args):
        self.single_click_stack.append((self.click_impl, args))

    def push_key_action(self, *args):
        self.single_click_stack.append((self.key_action_impl, args))
