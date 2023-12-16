"""Output begin and end messages."""

import datetime

class BeginAndEndMessages:

    """Run some code with nested begin and end/abandoned messages."""

    prefixes = []

    def __init__(self, about,
                 margin="    ",
                 verbose=True):
        self.verbose = verbose
        self.about = about
        self.margin = margin
        self.started = None

    def __enter__(self):
        if self.verbose:
            print(self.prefix, "Beginning", self.about)
        self.prefixes.append(self.margin)
        self.prefix = "".join(self.prefixes)
        self.started = datetime.datetime.now()
        return self

    def print(self, text):
        print(self.prefix, text)

    def __exit__(self, exc_type, _exc_val, _exc_tb):
        time_taken = datetime.datetime.now() - self.started
        self.prefixes.pop()
        self.prefix = "".join(self.prefixes)
        if self.verbose:
            print(self.prefix, ("Abandoned" if exc_type else "Finished"), self.about, "in", time_taken)
