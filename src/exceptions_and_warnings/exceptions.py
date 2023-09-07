from typing import Optional


class CannotPerformCalculations(Exception):
    """
    Defines the exception which is raise when a calculation cannot be made.
    """
    def __init__(self, msg: Optional[str] = None) -> None:
        """
        Constructor
        :param msg: details about the circumstance surrounding the raise.
        """
        if msg:
            super().__init__(msg)
