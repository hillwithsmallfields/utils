"""Output begin and end messages."""

import datetime

prefixes = list()

class BeginAndEndMessages:

    """Run some code with nested begin and end/abandoned messages."""

    def __init__(self, about,
                 margin="    ",
                 verbose=True):
        self.verbose = verbose
        self.about = about
        self.margin = margin
        self.started = None
        self.prefix = "".join(prefixes)

    def __enter__(self):
        if self.verbose:
            print(self.prefix + "Beginning", self.about)
        prefixes.append(self.margin)
        self.prefix = "".join(prefixes)
        self.started = datetime.datetime.now()
        return self

    def print(self, text):
        print(self.prefix + text)

    def __exit__(self, exc_type, _exc_val, _exc_tb):
        time_taken = datetime.datetime.now() - self.started
        prefixes.pop()
        self.prefix = "".join(prefixes)
        if self.verbose:
            print(self.prefix + ("Abandoned" if exc_type else "Finished"), self.about, "in", time_taken)

# if __name__ == "__main__":
#     with BeginAndEndMessages("outer one"):
#         with BeginAndEndMessages("middle one") as mid:
#             mid.print("inside mid one")
#             with BeginAndEndMessages("inner") as inner:
#                 inner.print("inner")
#         with BeginAndEndMessages("middle two") as mid:
#             mid.print("inside mid two")
#         with BeginAndEndMessages("middle three") as mid:
#             mid.print("inside mid three")
