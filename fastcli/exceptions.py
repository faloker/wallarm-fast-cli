class FASTError(Exception):
    """Generic exception for FAST CLI."""

    def __init__(self, message, extra=None):
        super(FASTError, self).__init__(message)
        self.extra = extra
