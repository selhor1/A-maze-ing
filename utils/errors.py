class InvalidDistinationFor42Path(Exception):
    """Raised when maze is too small for 42 pattern."""
    pass


class InvalidEntryExitPoint(Exception):
    """Raised when entry/exit are inside 42 pattern."""
    pass