import collections
from enum import Enum
from snaptron_query.app import exceptions, global_strings as gs


class JunctionType(Enum):
    EXCLUSION = 0
    INCLUSION = 1


def split_and_cast(sample):
    (rail_id, count) = sample.split(':')
    return int(rail_id), int(count)


class JunctionInclusionQueryManager:
    """Module that processes the junction inclusion query given the dataframe output from snaptron"""

    def __init__(self,
                 exclusion_start: int,
                 exclusion_end: int,
                 inclusion_start: int,
                 inclusion_end: int) -> None:

        self.exclusion_start = exclusion_start
        self.exclusion_end = exclusion_end
        self.inclusion_start = inclusion_start
        self.inclusion_end = inclusion_end
        self.rail_id_dictionary = collections.defaultdict(list)
        self.gathered_rail_id_meta_data_and_psi = []

    def get_rail_id_dictionary(self):
        return self.rail_id_dictionary

    def _gather_samples_rail_id_and_counts(self, samples, junction_type):
        """Given the samples extracted for the junction,extract the rail id and count info from the data.If the
        sample is from an inclusion junction, mark it as True
        """
        # samples usually has 1 row, but just in case
        # I am putting it in a for loop
        for junction_samples in samples:
            # samples are separated by commas then each sample is separated with a colon from its count as railID:count
            for each_sample in junction_samples.split(','):
                if each_sample:
                    (rail_id, count) = split_and_cast(each_sample)

                    # create dictionary item
                    dict_value = {'count': count, 'type': junction_type}

                    # keep the item in a defaultdict(list)
                    self.rail_id_dictionary[rail_id].append(dict_value)

    def _calculate_percent_spliced_in(self, rail_id):
        # calculate Percent Spliced In
        sample_counts = self.rail_id_dictionary[rail_id]
        # make sure all values are 0
        inclusion_count = exclusion_count = 0
        psi = 0.0
        for s in sample_counts:
            inclusion_junction_type = s.get('type')
            if inclusion_junction_type == JunctionType.INCLUSION:
                inclusion_count = s.get('count')
            if inclusion_junction_type == JunctionType.EXCLUSION:
                exclusion_count = s.get('count')

        # count totals
        total_count = inclusion_count + exclusion_count

        # TODO: PSI calculation tolerance of 15, PI must verify?
        if total_count > 0:
            # calculate the percent spliced in
            psi = round(((100 * inclusion_count) / float(total_count)), 2)

        return psi, inclusion_count, exclusion_count, total_count

    def _gather_rail_id_meta_data(self, rail_id, df_meta_data):
        """Given the metadata for the compilation and the rail ids,function extracts the related metadata for
        rail ids
        """
        # look up the rail id and extract the information
        try:
            # gather the metadata associated with this rail id
            # note: loc will return a data series not a frame
            meta_data = (df_meta_data.loc[rail_id]).to_dict()

            # TODO: for multi junction query the data may be different here
            # append the calculated results such as PSI and other counts
            (meta_data[gs.table_jiq_col_psi], meta_data[gs.table_jiq_col_inc], meta_data[gs.table_jiq_col_exc],
             meta_data[gs.table_jiq_col_total]) = self._calculate_percent_spliced_in(rail_id)

            # add the rail id information
            meta_data[gs.snaptron_col_rail_id] = rail_id

            # append to the rest of the data
            self.gathered_rail_id_meta_data_and_psi.append(meta_data)

        except (KeyError, IndexError):
            # TODO: look into the rail ids that are not found in the meta data file.
            # TODO: IT MUST BE IN THE META FILE, is this a snaptron error? discuss with PI
            # print(f"{rail_id} not in meta data file.  Moving on to the next iteration.")
            # code must continue and not stop
            pass

    @staticmethod
    def _find_junction(df, start, end):
        return df.loc[(df['start'] == start) & (df['end'] == end)]

    def run_junction_inclusion_query(self, df, df_meta_data):
        """Given the snaptron interface results, this function calculates the Percent Spliced In (PSI)
        given the inclusion junction and the exclusion junction
        """
        # find the exclusion and inclusion junction rows
        exc_junctions_df = self._find_junction(df, self.exclusion_start, self.exclusion_end)
        inc_junctions_df = self._find_junction(df, self.inclusion_start, self.inclusion_end)

        # if either one is empty the user has inputted wrong coordinates
        if exc_junctions_df.empty or inc_junctions_df.empty:
            raise exceptions.EmptyJunction

        # extract the 'sample' column form the row this is where all the samples and their count is
        exclusion_junction_samples = (exc_junctions_df['samples']).tolist()
        inclusion_junction_samples = (inc_junctions_df['samples']).tolist()

        # Gather results in a dictionary
        self._gather_samples_rail_id_and_counts(exclusion_junction_samples, JunctionType.EXCLUSION)
        self._gather_samples_rail_id_and_counts(inclusion_junction_samples, JunctionType.INCLUSION)

        # For each rail id found, gather its metadata and calculate PSI values
        # this will populate self.gathered_rail_id_meta_data_and_psi
        for rail_id in self.rail_id_dictionary:
            self._gather_rail_id_meta_data(rail_id, df_meta_data)

        # returning a list of dictionaries not a dataframe for better coexistence with the front-end UI
        return self.gathered_rail_id_meta_data_and_psi
