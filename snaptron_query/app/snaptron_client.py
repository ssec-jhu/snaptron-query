import httpx
import pandas as pd
from io import BytesIO
from snaptron_query.app import exceptions
import re


def verify_coordinates(coordinates):
    # pattern used from snaptron code:
    # https://github.com/ChristopherWilks/snaptron/blob/75903c30d54708b19d91772142013687c74d88d8/snapconfshared.py#L196C31
    # https://docs.python.org/3/library/re.html#re.Match
    pattern = r'^(chr[12]?[0-9XYM]):(\d+)-(\d+)$'
    m = re.match(pattern, str(coordinates))
    if m:  # group(0) is the entire match, will be None if there is no match
        # group(1) will be the chromosome
        # group(2) will be the start of the interval
        # group(3) will be the end of the interval
        return m.group(1), int(m.group(2)), int(m.group(3))
    else:  # if not re.match(pattern, (str(coordinates))):
        raise exceptions.BadCoordinates


def jiq_verify_coordinate_pairs(exclusion_coordinates, inclusion_coordinates):
    (exc_chr, exc_start, exc_end) = verify_coordinates(exclusion_coordinates)
    (inc_chr, inc_start, inc_end) = verify_coordinates(inclusion_coordinates)

    # add sanity checks here for the pairs
    if inc_chr != exc_chr or inc_start > inc_end or exc_start > exc_end:
        raise exceptions.BadCoordinates

    return (exc_chr, exc_start, exc_end), (inc_chr, inc_start, inc_end)


def geq_verify_coordinate(gene_coordinate):
    (coord_chr, coord_start, coord_end) = verify_coordinates(gene_coordinate)

    # add sanity checks here for the pairs
    if coord_start > coord_end:
        raise exceptions.BadCoordinates

    return coord_chr, coord_start, coord_end


def get_snpt_query_results_df(compilation, junction_coordinates, query_mode):
    """Will run the url and return the response
    :param compilation: from the list box selection
    :param junction_coordinates: the interval of the query
    :param query_mode:  'snaptron' or 'genes'
    :return: the result of the snaptron web interface converted into a dataframe
    """
    # TODO: move this to a config file when it's made
    host = 'https://snaptron.cs.jhu.edu'
    url = f'{host}/{str(compilation).lower()}/{query_mode}?regions={str(junction_coordinates)}'
    # url = 'https://snaptro.cs.jhu.edu/srav3h/snaptron?regions=chr19:4491836-4493702'
    # temp_url = 'https://snaptron.cs.jhu.edu/srav3h/genes?regions=chr1:11013716-11024183'

    try:
        resp = httpx.get(url)
        # this will raise an HTTPError, if the response was a http error.
        resp.raise_for_status()

        data_bytes = resp.read()
        if data_bytes:
            df = pd.read_csv(BytesIO(data_bytes), sep='\t')
            return df
        else:
            raise exceptions.EmptyResponse
    except Exception as e:
        # Any other exception happens I want it forwarded to the front end for handling
        print(f"HTTP Exception: {e}")
        raise exceptions.BadURL
