import collections
import re
from io import BytesIO

import httpx
import pandas as pd

from snaptron_query.app import exceptions

COORDINATES = collections.namedtuple("COORDINATES", ["chr", "start", "end"])

JIQ_COORDINATES = collections.namedtuple(
    "JIQ_COORDINATES",
    [
        "exc_coordinates",  # type COORDINATES
        "inc_coordinates",
    ],
)  # type COORDINATES


def coordinates_to_formatted_string(coordinates: COORDINATES):
    return f"{coordinates.chr}:{coordinates.start}-{coordinates.end}"


def verify_coordinates(coordinates):
    # Another format used is: Chromosome 19: 4,472,297-4,502,208
    # We want to handle this case as well and remove all commas and spaces
    translation_table = str.maketrans("", "", ", ")
    coordinates = coordinates.translate(translation_table).replace("Chromosome", "chr")

    # pattern used from snaptron code:
    # https://github.com/ChristopherWilks/snaptron/blob/75903c30d54708b19d91772142013687c74d88d8/snapconfshared.py#L196C31
    # https://docs.python.org/3/library/re.html#re.Match
    pattern = r"^(chr[12]?[0-9XYM]):(\d+)-(\d+)$"
    m = re.match(pattern, coordinates)
    if m:  # group(0) is the entire match, will be None if there is no match
        # group(1) will be the chromosome
        # group(2) will be the start of the interval
        # group(3) will be the end of the interval
        return COORDINATES(m.group(1), int(m.group(2)), int(m.group(3)))
    else:  # if not re.match(pattern, (str(coordinates))):
        raise exceptions.BadCoordinates


def jiq_verify_coordinate_pairs(exclusion_coordinates, inclusion_coordinates):
    exc_coordinates = verify_coordinates(exclusion_coordinates)
    inc_coordinates = verify_coordinates(inclusion_coordinates)

    # add sanity checks here for the pairs
    if (
        inc_coordinates.chr != exc_coordinates.chr
        or inc_coordinates.start > inc_coordinates.end
        or exc_coordinates.start > exc_coordinates.end
    ):
        raise exceptions.BadCoordinates

    return JIQ_COORDINATES(exc_coordinates, inc_coordinates)


def geq_verify_coordinate(gene_coordinate):
    coordinates = verify_coordinates(gene_coordinate)

    # add sanity checks here for the pairs
    if coordinates.start > coordinates.end:
        raise exceptions.BadCoordinates

    return coordinates


def get_snpt_query_results_df(compilation, region, query_mode):
    """Will run the url and return the response
    :param compilation: from the list box selection
    :param region: the interval of the query
    :param query_mode:  'snaptron' or 'genes'
    :return: the result of the snaptron web interface converted into a dataframe
    """
    # TODO: move this to a config file when it's made
    host = "https://snaptron.cs.jhu.edu"
    url = f"{host}/{str(compilation).lower()}/{query_mode}?regions={str(region)}"
    # url = 'https://snaptro.cs.jhu.edu/srav3h/snaptron?regions=chr19:4491836-4493702'
    # temp_url = 'https://snaptron.cs.jhu.edu/srav3h/genes?regions=chr1:11013716-11024183'

    resp = httpx.get(url)
    # this will raise an HTTPError, if the response was a http error.
    # any exceptions thrown here will be captured by the client: Dash UI in this case
    resp.raise_for_status()
    data_bytes = resp.read()
    if data_bytes:
        df = pd.read_csv(BytesIO(data_bytes), sep="\t")
        return df
    else:
        raise exceptions.EmptyResponse
