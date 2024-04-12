import httpx
from snaptron_query.app import global_strings as gs

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
        alert_message = gs.bad_url
    elif e == EmptyResponse:
        alert_message = gs.empty_response
    elif e == MissingUserInputs:
        alert_message =gs.missing_user_input
    elif e == BadCoordinates:
        alert_message = gs.bad_coordinates
    elif e == EmptyJunction:
        alert_message = gs.empty_junction
    elif e == QueryGeneNotFound:
        alert_message = gs.query_gene_not_found
    elif e == NormalizationGeneNotFound:
        alert_message = gs.normalization_gene_not_found
    elif e == httpx.RemoteProtocolError:
        alert_message = gs.httpx_remote_protocol_error
    elif e == httpx.ConnectError or httpx.ConnectTimeout:
        alert_message = gs.httpx_connect_error
    else:
        alert_message = f'Exception Occurred: {e}'

    return alert_message
