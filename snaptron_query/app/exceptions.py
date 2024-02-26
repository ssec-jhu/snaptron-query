class BadURL(Exception):
    """Raised when the url is invalid"""
    pass


class EmptyResponse(Exception):
    """Raised when the response returned is invalid"""
    pass


class BadCoordinates(Exception):
    """Raised when the user has entered incorrect coordinates"""
    pass


class MissingUserInputs(Exception):
    """Raised when the user has missing inputs"""
    pass
