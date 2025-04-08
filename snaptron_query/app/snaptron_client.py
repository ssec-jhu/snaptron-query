import collections
import httpx
import pandas as pd
from io import BytesIO
from snaptron_query.app import exceptions
import re

JunctionCoordinates = collections.namedtuple("JunctionCoordinates", ["chr", "start", "end"])

SpliceJunctionPair = collections.namedtuple(
    "SpliceJunctionPair",
    [
        "exc_coordinates",  # type JunctionCoordinates
        "inc_coordinates",
        "search_coordinates",
    ],
)  # type JunctionCoordinates


def coordinates_to_formatted_string(coordinates: JunctionCoordinates):
    return f"{coordinates.chr}:{coordinates.start}-{coordinates.end}"


def verify_coordinates(coordinates) -> JunctionCoordinates:
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
        return JunctionCoordinates(m.group(1), int(m.group(2)), int(m.group(3)))
    else:  # if not re.match(pattern, (str(coordinates))):
        raise exceptions.BadCoordinates


def jiq_verify_coordinate_pairs(
    exclusion_coordinates, inclusion_coordinates, expanded_coordinates
) -> SpliceJunctionPair:
    exc_coordinates = verify_coordinates(exclusion_coordinates)
    inc_coordinates = verify_coordinates(inclusion_coordinates)

    # add sanity checks here for the pairs
    if (
        inc_coordinates.chr != exc_coordinates.chr
        or inc_coordinates.start > inc_coordinates.end
        or exc_coordinates.start > exc_coordinates.end
    ):
        raise exceptions.BadCoordinates

    # add checks here for if any inclusion junction is outside exclusion junction
    # this should allow for mutually exclusive exons?
    if not expanded_coordinates:
        if (
            (inc_coordinates.start > exc_coordinates.end and inc_coordinates.end > exc_coordinates.end)
            or (exc_coordinates.start > inc_coordinates.start and exc_coordinates.start > inc_coordinates.end)
            or (inc_coordinates.start < exc_coordinates.start < inc_coordinates.end)
            or (inc_coordinates.start < exc_coordinates.end < inc_coordinates.end)
        ):
            raise exceptions.ExpandedJunctions
        else:
            search_coordinates = verify_coordinates(exclusion_coordinates)
    else:
        search_coordinates = JunctionCoordinates(
            exc_coordinates.chr,
            min(exc_coordinates.start, inc_coordinates.start),
            max(exc_coordinates.end, inc_coordinates.end),
        )

    return SpliceJunctionPair(
        exc_coordinates=exc_coordinates, inc_coordinates=inc_coordinates, search_coordinates=search_coordinates
    )


def geq_verify_coordinate(gene_coordinate) -> JunctionCoordinates:
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


def gather_snpt_query_results_into_dict(compilation, junction_lists: [SpliceJunctionPair]):
    df_snpt_results_dict = {}
    for j in range(len(junction_lists)):
        # gather the exclusion junctions snaptron results
        # only run if it wasn't calculated previously
        junction_exc_coordinates = junction_lists[j].exc_coordinates
        junction_search_coordinates = junction_lists[j].search_coordinates
        if junction_exc_coordinates not in df_snpt_results_dict:
            # RUN the URL and get results back from SNAPTRON
            # make sure you get results back
            if junction_lists[j].exc_coordinates != junction_lists[j].search_coordinates:
                # This occurs when we care about expanded coordinates. This is the same as the exclusion coordinates in
                # some cases. "exc_coordinates" hard-coded in query_junction_inclusion.py for the results dictionary -
                # will break if I change to search_coordinates
                df_snpt_results = get_snpt_query_results_df(
                    compilation=compilation,
                    region=coordinates_to_formatted_string(junction_search_coordinates),
                    query_mode="snaptron",
                )
            else:
                df_snpt_results = get_snpt_query_results_df(
                    compilation=compilation,
                    region=coordinates_to_formatted_string(junction_exc_coordinates),
                    query_mode="snaptron",
                )

            if df_snpt_results.empty:
                raise exceptions.EmptyResponse

            df_snpt_results_dict[junction_exc_coordinates] = df_snpt_results

    return df_snpt_results_dict
