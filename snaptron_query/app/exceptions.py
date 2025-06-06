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


class EmptyIncJunction(Exception):
    """Raised when one of the inclusion junctions is empty"""

    def __init__(self, index):
        self.index = index

    def get_message(self):
        return f"Inclusion Junction {self.index} returned no results!"


class EmptyExcJunction(Exception):
    """Raised when one of the junctions is empty"""

    def __init__(self, index):
        self.index = index

    def get_message(self):
        return f"Exclusion Junction {self.index} returned no results!"


class QueryGeneNotFound(Exception):
    """Raised when the gene is not found in the results"""

    pass


class NormalizationGeneNotFound(Exception):
    """Raised when the gene is not found in the results"""

    pass


class MatchingQueryAndNormGene(Exception):
    """Raised when the gene names or coordinates match"""

    pass


class EncodeNormAttempt(Exception):
    """Raised when the data compilation is ENCODE for GEQ and trying to normalize"""

    pass


def alert_message_from_exception(exception):
    e = type(exception)
    if e == BadURL:
        alert_message = gs.bad_url
    elif e == EmptyResponse:
        alert_message = gs.empty_response
    elif e == MissingUserInputs:
        alert_message = gs.missing_user_input
    elif e == BadCoordinates:
        alert_message = gs.bad_coordinates
    elif e == EmptyIncJunction:
        alert_message = exception.get_message()
    elif e == EmptyExcJunction:
        alert_message = exception.get_message()
    elif e == QueryGeneNotFound:
        alert_message = gs.query_gene_not_found
    elif e == NormalizationGeneNotFound:
        alert_message = gs.normalization_gene_not_found
    elif e == MatchingQueryAndNormGene:
        alert_message = gs.matching_query_and_norm_gen
    elif e == httpx.RemoteProtocolError:
        alert_message = gs.httpx_remote_protocol_error
    elif e == httpx.ConnectError or e == httpx.ConnectTimeout:
        alert_message = gs.httpx_connect_error
    elif e == EncodeNormAttempt:
        alert_message = gs.geq_encode_norm_error
    else:
        alert_message = f"Exception Occurred: {exception}"

    return alert_message
