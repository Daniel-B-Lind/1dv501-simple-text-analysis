"""

1DV501 Final Project - SimpleTextAnalysis
stex_exceptions.py (or, if you will, stexceptions :D)

Author: Daniel Lind

This file provides custom defined exceptions for the project.

"""

class OperationCancelled(Exception):
    """
    Raised when a user explicitly chooses to abort or cancel an operation
    mid-execution.
    """
    def __init__(self, message="Operation was cancelled by the user."):
        self.message = message
        super().__init__(self.message)