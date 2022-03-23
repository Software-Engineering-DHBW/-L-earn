"""
Defines all used exceptions
"""


class Error(Exception):
    pass


# Exception if an empty variable, especially for arrays, is given to a function
class EmptyValueError(Error):
    pass


# Exception if a searched value doesn't exist
class NotFoundError(Error):
    pass
