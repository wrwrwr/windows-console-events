import enum


class Signals(enum.IntEnum):
    """
    Signal numbers, with few additions to signal.Signals.
    """
    SIGINT = 2
    SIGILL = 4
    SIGFPE = 8
    SIGSEGV = 11
    SIGTERM = 15
    SIGBREAK = 21
    SIGABRT = 22
    CTRL_C_EVENT = 0
    CTRL_BREAK_EVENT = 1
    CTRL_CLOSE_EVENT = 2
    CTRL_LOGOFF_EVENT = 5
    CTRL_SHUTDOWN_EVENT = 6

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
                try:
                    return cls[name + '_EVENT']
                except KeyError:
                    return cls['SIG' + name]
