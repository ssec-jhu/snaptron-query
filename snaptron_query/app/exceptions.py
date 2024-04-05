import httpx


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


class QueryGeneNotFound(Exception):
    """Raised when the gene is not found in the results"""
    pass


class NormalizationGeneNotFound(Exception):
    """Raised when the gene is not found in the results"""
    pass


def handle_exception(exception):
    e = type(exception)
    if e == BadURL:
        alert_message = 'Sorry, something must have gone wrong...try again in a couple minutes!'
    elif e == EmptyResponse:
        alert_message = 'Snaptron Empty response!'
    elif e == MissingUserInputs:
        alert_message = 'You are missing one or more required inputs...try again!'
    elif e == BadCoordinates:
        alert_message = 'Input coordinates are invalid!'
    elif e == EmptyJunction:
        alert_message = 'Junctions entered have no results!'
    elif e == QueryGeneNotFound:
        alert_message = ('Query gene was not found. Try adding gene coordinates to your query or double check '
                         'coordinates if provided!')
    elif e == NormalizationGeneNotFound:
        alert_message = ('Normalization gene was not found. Try adding gene coordinates to your query or double check '
                         'coordinates if provided!')
    elif e == httpx.RemoteProtocolError:
        alert_message = f'Remote Protocol Error: {exception.args[0]}.'
    elif e == httpx.ConnectError or httpx.ConnectTimeout:
        alert_message = 'Failed to establish a connection with Snaptron Web API!'
    else:
        alert_message = f'Exception Occurred: {e}'

    return alert_message
