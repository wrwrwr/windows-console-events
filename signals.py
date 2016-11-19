import enum


class Signals(enum.IntEnum):
    """
    Signal numbers.
    """
    SIGINT = 2
    SIGILL = 4
    SIGFPE = 8
    SIGSEGV = 11
    SIGTERM = 15
    SIGBREAK = 21
    SIGABRT = 22

    @classmethod
    def get(cls, value_or_name):
        """
        Finds a signal with the given value or loosely matched name.
        """
        try:
            return cls(int(value_or_name))
        except ValueError:
            name = str(value_or_name).upper()
            try:
                return cls[name]
            except KeyError:
                return cls['SIG{}'.format(name)]
