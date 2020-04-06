class Error(Exception):
    """Base class."""
    pass


class PointGenerationError(Error):
    """Exception raised for point generation exceeding number of tries.

    Attributes:
        message -- explaination of the error.
    """

    def __init__(self, message):
        self.message = message
