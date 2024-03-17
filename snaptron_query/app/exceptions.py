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


class EmptyJunction(Exception):
    """Raised when one of the junctions is empty"""
    pass


class GeneNotFound(Exception):
    """Raised when the gene is not found in the results"""
    pass