"""Output begin and end messages."""

class BeginAndEndMessages:

    """Run some code with begin and end/abandoned messages."""

    def __init__(self, about, verbose=True):
        self.verbose = verbose
        self.about = about

    def __enter__(self):
        if self.verbose:
            print("Beginning", self.about)

    def __exit__(self, exc_type, _exc_val, _exc_tb):
        if self.verbose:
            print(("Abandoned" if exc_type else "Finished"), self.about)
