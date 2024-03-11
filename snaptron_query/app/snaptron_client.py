import httpx
import pandas as pd
from io import BytesIO
from snaptron_query.app import exceptions
import re


def split_genome_coordinates(*args):
    # split values such as 'chrX:Y-Z'
    return [(str(ch), int(start), int(end)) for ch, interval in [x.split(':') for x in args] for start, end in
            [interval.split('-')]]


def verify_coordinates(coordinates):
    # pattern used from snaptron code:
    # https://github.com/ChristopherWilks/snaptron/blob/75903c30d54708b19d91772142013687c74d88d8/snapconfshared.py#L196C31
    pattern = r'^(chr[12]?[0-9XYM]):(\d+)-(\d+)$'
    if not re.match(pattern, (str(coordinates))):
        raise exceptions.BadCoordinates


def split_and_verify_coordinates(*args):
    # verify the regex first
    for x in args:
        verify_coordinates(x)

    # split the intervals into chromosome numbers and interval starts and ends
    (exc_chr, exc_start, exc_end), (inc_chr, inc_start, inc_end) = split_genome_coordinates(*args)

    # add sanity checks here
    if inc_chr != exc_chr or inc_start > inc_end or exc_start > exc_end:
        raise exceptions.BadCoordinates

    return (exc_chr, exc_start, exc_end), (inc_chr, inc_start, inc_end)


def get_snaptron_query_results_df(compilation, junction_coordinates, query_mode):
    """Will run the url and return the response
    :param compilation: from the list box selection
    :param junction_coordinates: the interval of the query
    :param query_mode:  'snaptron' or 'genes'
    :return: the result of the snaptron web interface converted into a dataframe
    """
    # TODO: move this to a config file when it's made
    host = 'https://snaptron.cs.jhu.edu'
    url = f'{host}/{str(compilation)}/{query_mode}?regions={str(junction_coordinates)}'
    # url = 'https://snaptro.cs.jhu.edu/srav3h/snaptron?regions=chr19:4491836-4493702'
    # temp_url = 'https://snaptron.cs.jhu.edu/srav3h/genes?regions=chr1:11013716-11024183'

    if url:
        try:
            resp = httpx.get(url.lower())
            resp.raise_for_status()
            data_bytes = resp.read()
            if data_bytes:
                df = pd.read_csv(BytesIO(data_bytes), sep='\t')
                return df
            else:
                raise exceptions.EmptyResponse
        except Exception as e:
            print(f"HTTP Exception: {e}")
            raise exceptions.BadURL
