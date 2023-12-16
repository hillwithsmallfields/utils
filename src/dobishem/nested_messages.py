"""Output begin and end messages."""

class NestedMessages:

    """Run some code with nested begin and end/abandoned messages."""

    depth = 0

    def __init__(self, about, margin="    ", verbose=True):
        self.verbose = verbose
        self.about = about
        self.prefix = ""

    def __enter__(self):
        self.depth += 1
        self.prefix = self.margin * self.depth
        if self.verbose:
            print(self.prefix, "Beginning", self.about)
        return self

    def print(self, text):
        print(self.prefix, text)

    def __exit__(self, exc_type, _exc_val, _exc_tb):
        if self.verbose:
            print(self.prefix, ("Abandoned" if exc_type else "Finished"), self.about)
        self.depth -= 1
