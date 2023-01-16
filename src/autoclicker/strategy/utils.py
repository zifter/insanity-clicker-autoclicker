from collections import deque


class KeyboardActionStack:
    def __init__(self, click_impl, key_action_impl):
        self.stack = deque()

        self.click_impl = click_impl
        self.key_action_impl = key_action_impl

    def pop(self):
        if self.stack:
            return self.stack.popleft()

        return None

    def push_click(self, *args):
        self.stack.append((self.click_impl, args))

    def push_key_action(self, *args):
        self.stack.append((self.key_action_impl, args))
