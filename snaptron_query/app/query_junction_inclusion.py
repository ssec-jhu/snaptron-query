import decimal
import pandas as pd
from snaptron_query.app import global_strings, exceptions


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
            # samples are separated by commas
            # then each sample is separated with a colon from its count
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

    def _gather_rail_id_meta_data(self, df_meta_data, rail_id_meta_data_list, rail_id):
        """Given the metadata for the compilation and the rail ids,function extracts the related metadata for
        rail ids
        """
        # look up the rail id and extract the information
        try:
            meta_data_series = df_meta_data.loc[int(rail_id)]  # make sure it is an int for lookup

            # TODO: move forward only if the rail id was found, throw exception otherwise,

            # TODO: this data will be different for different compilations
            # external_id, study, study_title = lookup_meta_data(meta_data_series)
            external_id = meta_data_series['external_id']
            study = meta_data_series['study']
            study_title = meta_data_series['study_title']

            counts = self.rail_id_dictionary[rail_id]
            inclusion_count = 0
            exclusion_count = 0
            psi = 0.0
            for c in counts:
                if c['inc'] == 'True':
                    inclusion_count = int(c['count'])
                if c['inc'] == 'False':
                    exclusion_count = int(c['count'])
            total_count = inclusion_count + exclusion_count

            # TODO: PSI calculation tolerance of 15? original code had this, ut now with ag grid it can be removed
            if total_count > 0:
                # calculate the percent spliced in
                psi = (100 * decimal.Decimal(inclusion_count)) / decimal.Decimal(total_count)
                psi = round(psi, 2)

                # TODO: append study_title as well, some bug here
                data = f'{rail_id},{external_id},{study},{inclusion_count},{exclusion_count},{total_count},{psi}'
                rail_id_meta_data_list.append(data)

        except (KeyError, IndexError):
            # TODO: look into the rail ids that are not found in the meta data file.
            print(f"{rail_id} not in meta data file.  Moving on to the next iteration.")

        return rail_id_meta_data_list

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

        # TODO: GLOBAL: this function should be called in global space
        #  and its data frame passed in based on compilation. String should also be global
        # df_meta_data = read_meta_data_file('srav3h')

        # this list will gather all the rail ids and their meta data
        rail_id_data_list = []
        for rail_id in self.rail_id_dictionary:
            rail_id_data_list = self._gather_rail_id_meta_data(df_meta_data, rail_id_data_list, rail_id)

        # create a dataframe form the list
        # TODO: column here will be different based on compilation -> maybe make that  function,
        # also used in gathering meta data
        try:
            split_data = [item.split(',') for item in rail_id_data_list]
            df_final = pd.DataFrame(split_data,
                                    columns=[global_strings.snaptron_col_rail_id,
                                             global_strings.snaptron_col_external_id,
                                             global_strings.snaptron_col_study,
                                             'inc', 'exc', 'total', 'psi'])

            # TODO: column names will change based on compilation here too
            # convert the datatypes here so it's easy later
            df_final[global_strings.snaptron_col_rail_id] = df_final[global_strings.snaptron_col_rail_id].astype('int')
            df_final['inc'] = df_final['inc'].astype('int')
            df_final['exc'] = df_final['exc'].astype('int')
            df_final['total'] = df_final['total'].astype('int')
            df_final['psi'] = df_final['psi'].astype('float')

        except ValueError:
            stop = 1
            # TODO: do something if this is thrown

        return df_final
