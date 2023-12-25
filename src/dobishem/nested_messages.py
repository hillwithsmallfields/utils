"""Output begin and end messages."""

import datetime

message_prefixes_as_list = list()

ONE_MINUTE = datetime.timedelta(seconds=60)
ONE_SECOND = datetime.timedelta(seconds=1)

class BeginAndEndMessages:

    """Run some code with nested begin and end/abandoned messages."""

    def __init__(self, about,
                 margin="    ",
                 verbose=True):
        self.verbose = verbose
        self.about = about
        self.margin = margin
        self.started = None
        self._set_prefix()

    def _set_prefix(self):
        self.prefix = "".join(message_prefixes_as_list)

    def __enter__(self):
        if self.verbose:
            print(self.prefix + "Beginning", self.about)
        message_prefixes_as_list.append(self.margin)
        self._set_prefix()
        self.started = datetime.datetime.now()
        return self

    def print(self, text):
        print(self.prefix + text)

    def __exit__(self, exc_type, _exc_val, _exc_tb):
        time_taken = datetime.datetime.now() - self.started
        message_prefixes_as_list.pop()
        self._set_prefix()
        if self.verbose:
            message = self.prefix + ("Abandoned " if exc_type else "Finished ") + self.about
            if time_taken >= ONE_MINUTE:
                message += " in %s" % time_taken
            elif time_taken >= ONE_SECOND:
                message += " in %.3g sec" % time_taken.total_seconds()
            print(message)
