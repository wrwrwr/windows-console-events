import enum


class Events(enum.IntEnum):
    """
    Console event numbers.
    """
    CTRL_C_EVENT = 0
    CTRL_BREAK_EVENT = 1
    CTRL_CLOSE_EVENT = 2
    CTRL_LOGOFF_EVENT = 5
    CTRL_SHUTDOWN_EVENT = 6

    @classmethod
    def get(cls, value_or_name):
        """
        Finds an event with the given value or loosely matched name.
        """
        try:
            return cls(int(value_or_name))
        except ValueError:
            name = str(value_or_name).upper()
            try:
                return cls[name]
            except KeyError:
                return cls['CTRL_{}_EVENT'.format(name)]
