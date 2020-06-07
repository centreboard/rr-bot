from unittest.case import TestCase


class TestLogger:
    def __init__(self, test_case: TestCase):
        self.test_case = test_case
        self.messages = []

    def log(self, message: str):
        self.messages.append(message)

    def assert_contains(self, message: str, count=1):
        filtered = [m for m in self.messages if m == message]
        self.test_case.assertEqual(len(filtered), count, f"{message} appears {len(filtered)} in {self.messages}")

    def print(self):
        for message in self.messages:
            print(message)
