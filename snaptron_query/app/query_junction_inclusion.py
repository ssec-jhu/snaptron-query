import decimal
import pandas as pd
from snaptron_query.app import exceptions


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
        self.rail_id_dictionary = dict()
        self.gathered_rail_id_meta_data_and_psi = []
        return

    def get_rail_id_dictionary(self):
        return self.rail_id_dictionary

    def _gather_samples_rail_id_and_counts(self, samples, mark_in_or_ex):
        """Given the samples extracted for the junction,extract the rail id and count info from the data.If the
        sample is from an inclusion junction, mark it.
        """
        # samples usually has 1 row, but just in case
        # I am putting it in a for loop
        for junction_samples in samples:
            # samples are separated by commas then each sample is separated with a colon from its count
            js = junction_samples.split(',')
            for eachSample in js:
                # each sample in snaptron is set as railID:count
                if eachSample:
                    (rail_id, count) = eachSample.split(':')

                    # cast the strings
                    rail_id = int(rail_id)
                    count = int(count)
                    dict_value = {'count': int(count), 'inc': mark_in_or_ex}

                    # keep the item in a dictionary
                    if rail_id in self.rail_id_dictionary:
                        self.rail_id_dictionary[rail_id].append(dict_value)
                    else:
                        self.rail_id_dictionary[rail_id] = [dict_value]

    def _calculate_percent_spliced_in(self, rail_id):
        # calculate Percent Spliced In
        sample_counts = self.rail_id_dictionary[rail_id]
        # make sure all values are 0
        inclusion_count = exclusion_count = 0
        psi = 0.0
        for s in sample_counts:
            inclusion_junction_type = s.get('inc')
            if inclusion_junction_type == 'True':
                inclusion_count = int(s.get('count'))
            if inclusion_junction_type == 'False':
                exclusion_count = int(s.get('count'))
        total_count = inclusion_count + exclusion_count

        # TODO: PSI calculation tolerance of 15, PI must verify?
        if total_count > 0:
            # calculate the percent spliced in
            psi = round(((100 * decimal.Decimal(inclusion_count)) / decimal.Decimal(total_count)), 2)

        return psi, inclusion_count, exclusion_count, total_count

    def _gather_rail_id_meta_data(self, rail_id, df_meta_data):
        """Given the metadata for the compilation and the rail ids,function extracts the related metadata for
        rail ids
        """
        # look up the rail id and extract the information
        try:
            # look up the rail id, make sure it is an int
            # note: loc will return a data series not a frame
            meta_data = (df_meta_data.loc[int(rail_id)]).to_dict()

            # calculate psi related values
            (psi, inclusion_count, exclusion_count, total_count) = self._calculate_percent_spliced_in(rail_id)

            # combine calculated values with the meta data
            # TODO: for multi junction query the behavior may be different here
            meta_data['rail_id'] = int(rail_id)
            meta_data['inc'] = int(inclusion_count)
            meta_data['exc'] = int(exclusion_count)
            meta_data['total'] = int(total_count)
            meta_data['psi'] = float(psi)

            # append to the rest of the data
            self.gathered_rail_id_meta_data_and_psi.append(meta_data)

        except (KeyError, IndexError):
            # TODO: look into the rail ids that are not found in the meta data file.
            # IT MUST BE IN THE META FILE
            print(f"{rail_id} not in meta data file.  Moving on to the next iteration.")

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
        if not exc_junctions_df.shape[0] or not inc_junctions_df.shape[0]:
            raise exceptions.BadCoordinates

        # extract the 'sample' column form the row this is where all the samples and their count is
        exclusion_junction_samples = (exc_junctions_df['samples']).tolist()
        inclusion_junction_samples = (inc_junctions_df['samples']).tolist()

        # Gather results in a dictionary. Samples that were extracted
        # as part of an inclusion junction are marked as 'true' and 'false' otherwise
        self._gather_samples_rail_id_and_counts(exclusion_junction_samples, 'False')
        self._gather_samples_rail_id_and_counts(inclusion_junction_samples, 'True')

        # For each rail id found, gather its metadata and calculate PSI values
        # this will populate self.gathered_rail_id_meta_data_and_psi
        for rail_id in self.rail_id_dictionary:
            self._gather_rail_id_meta_data(rail_id, df_meta_data)

        df_final = pd.DataFrame(self.gathered_rail_id_meta_data_and_psi)

        return df_final
