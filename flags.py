import enum


class Flags(enum.IntEnum):
    """
    Process creation flags.
    """
    CREATE_BREAKAWAY_FROM_JOB = 0x01000000
    CREATE_DEFAULT_ERROR_MODE = 0x04000000
    CREATE_NEW_CONSOLE = 0x00000010
    CREATE_NEW_PROCESS_GROUP = 0x00000200
    CREATE_NO_WINDOW = 0x08000000
    CREATE_PROTECTED_PROCESS = 0x00040000
    CREATE_PRESERVE_CODE_AUTHZ_LEVEL = 0x02000000
    CREATE_SEPARATE_WOW_VDM = 0x00000800
    CREATE_SHARED_WOW_VDM = 0x00001000
    CREATE_SUSPENDED = 0x00000004
    CREATE_UNICODE_ENVIRONMENT = 0x00000400
    DEBUG_ONLY_THIS_PROCESS = 0x00000002
    DEBUG_PROCESS = 0x00000001
    DETACHED_PROCESS = 0x00000008
    EXTENDED_STARTUPINFO_PRESENT = 0x00080000
    INHERIT_PARENT_AFFINITY = 0x00010000

    @classmethod
    def get(cls, value_or_name):
        """
        Finds a flag with the given value or loosely matched name.
        """
        try:
            return cls(int(value_or_name))
        except ValueError:
            name = str(value_or_name).upper()
            try:
                return cls[name]
            except KeyError:
                return cls['CREATE_' + name]
