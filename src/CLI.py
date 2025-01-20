import argparse

class CLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Command processing CLI")
        self.parser.add_argument('--command', type=str, required=True, help="The command to execute")
        self.parser.add_argument('--language', type=str, choices=['python', 'matlab'], required=True, help="Language of the source code")

    def parse_input(self):
        return self.parser.parse_args()
