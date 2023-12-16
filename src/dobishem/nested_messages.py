"""Output begin and end messages."""

import datetime

message_prefixes_as_list = list()

class BeginAndEndMessages:

    """Run some code with nested begin and end/abandoned messages."""

    def __init__(self, about,
                 margin="    ",
                 verbose=True):
        self.verbose = verbose
        self.about = about
        self.margin = margin
        self.started = None
        self._set_prefix("0")

    def _set_prefix(self, label):
        print(label, "setting prefix from", message_prefixes_as_list)
        self.prefix = "".join(message_prefixes_as_list)

    def __enter__(self):
        if self.verbose:
            print(self.prefix + "Beginning", self.about)
        message_prefixes_as_list.append(self.margin)
        self._set_prefix("+")
        self.started = datetime.datetime.now()
        return self

    def print(self, text):
        print(self.prefix + text)

    def __exit__(self, exc_type, _exc_val, _exc_tb):
        time_taken = datetime.datetime.now() - self.started
        message_prefixes_as_list.pop()
        self._set_prefix("-")
        if self.verbose:
            print(self.prefix + ("Abandoned" if exc_type else "Finished"), self.about, "in", time_taken)

if __name__ == "__main__":
    with BeginAndEndMessages("outer one"):
        with BeginAndEndMessages("middle one") as mid:
            mid.print("inside mid one")
            with BeginAndEndMessages("inner") as inner:
                inner.print("inner")
        with BeginAndEndMessages("middle two") as mid:
            mid.print("inside mid two")
        with BeginAndEndMessages("middle three") as mid:
            mid.print("inside mid three")
