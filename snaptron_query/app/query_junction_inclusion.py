import collections
from enum import StrEnum
import pandas

from snaptron_query.app import exceptions, global_strings as gs, utils


class JunctionType(StrEnum):
    EXCLUSION = 'exc'
    INCLUSION = 'inc'


class JiqReturnType(StrEnum):
    LIST = 'list_of_dictionaries_for_ag_grid'
    RAW = 'raw_rail_id_dictionary'
    INDEXED_PD = 'pandas_data_frame'


# note the fields in this named tuple must match the table column names of the JIQ
JiqCalculations = collections.namedtuple('JiqCalculations',
                                         [gs.table_jiq_col_psi, gs.table_jiq_col_inc,
                                          gs.table_jiq_col_exc, gs.table_jiq_col_total, gs.table_jiq_col_log_2])


def split_and_cast(sample):
    (rail_id, count) = sample.split(':')
    return int(rail_id), int(count)


def default_junctions_dict():
    # Note: this acts like a "default constructor" for every value of a key not found
    return {"meta": {}, "junctions": [], "psi_sum": 0}


def insert_junction_calculations(list_of_junctions, junction_index, dict_items_to_add):
    # Extend the list if the index is larger than the current size
    if junction_index >= len(list_of_junctions):
        # Note: I purposefully did not fill the junction with JiqCalculations default.
        # All the other calculations are based upon these two values and are derived IF they exist for a junction
        list_of_junctions.extend([{'inc': 0, 'exc': 0} for _ in range(junction_index - len(list_of_junctions) + 1)])

    # Update the dictionary in the first list at the given index
    list_of_junctions[junction_index].update(dict_items_to_add)


class JunctionInclusionQueryManager:
    """Module that processes the junction inclusion query given the dataframe output from snaptron"""

    def __init__(self) -> None:
        self.rail_id_dictionary = collections.defaultdict(default_junctions_dict)

    def get_rail_id_dictionary(self):
        return self.rail_id_dictionary

    def _gather_samples_rail_id_and_counts(self, samples, junction_type, junction_index):
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
                    dict_value = {junction_type: count}
                    insert_junction_calculations(list_of_junctions=self.rail_id_dictionary[rail_id]['junctions'],
                                                 junction_index=junction_index,
                                                 dict_items_to_add=dict_value)

    def _calculate_percent_spliced_in(self, rail_id, junction_index):
        # calculate Percent Spliced In
        try:
            # get the inclusion and exclusion counts for this junction index
            # if this sample does not show up at this junction index, it will be populated with default
            # values in the IndexError exception below
            inclusion_count = (self.rail_id_dictionary[rail_id]['junctions'][junction_index]).get('inc', 0)
            exclusion_count = (self.rail_id_dictionary[rail_id]['junctions'][junction_index]).get('exc', 0)

        except IndexError:
            # if rail id has no sample in the junction, populate with default values
            insert_junction_calculations(list_of_junctions=self.rail_id_dictionary[rail_id]['junctions'],
                                         junction_index=junction_index,
                                         dict_items_to_add=JiqCalculations(0, 0, 0, 0, 0)._asdict())
            return

        # count totals
        total_count = inclusion_count + exclusion_count

        # TODO: PSI calculation tolerance of 15, PI must verify?
        psi = 0.0
        if total_count > 0:
            # calculate the percent spliced in
            psi = round(((100 * inclusion_count) / float(total_count)), 2)

        log2 = round(utils.log_2_plus(psi), 4)

        # insert the information for this junction
        insert_junction_calculations(
            list_of_junctions=self.rail_id_dictionary[rail_id]['junctions'],
            junction_index=junction_index,
            dict_items_to_add=JiqCalculations(psi, inclusion_count, exclusion_count, total_count, log2)._asdict())

        # accumulate the psi sum values
        self.rail_id_dictionary[rail_id]["psi_sum"] += psi

    def _gather_rail_id_meta_data(self, rail_id, meta_data_dict, junction_index):
        """Given the metadata for the compilation and the rail ids,function extracts the related metadata for
        rail ids
        """
        # look up the rail id and extract the information
        try:
            # gather the metadata associated with this rail id note: loc will return a data series not a frame
            # Performance note: using data frame as (meta_data_df.loc[rail_id]).to_dict() had a bad performance as
            # this was called for all rail_ids. Replaced the code to use dictionaries and made a significant
            # difference.
            # do lookup only if metadata does not exist
            if not self.rail_id_dictionary[rail_id]['meta']:
                self.rail_id_dictionary[rail_id]['meta'] = meta_data_dict[rail_id]

            # append the calculated results such as PSI and other counts
            self._calculate_percent_spliced_in(rail_id, junction_index)

        except (KeyError, IndexError):
            # TODO: look into the rail ids that are not found in the meta data file.
            # print(f"{rail_id} not in meta data file.  Moving on to the next iteration.")
            # code must continue and not stop
            pass

    def _convert_results_to_dictionary_list_single_jiq(self):
        """rail_id_dictionary contains information for all the samples an is independent of the UI.
        Use this helper function to convert to extract what we want to show for the SINGLE junction query table.
        """
        single_junction = []
        for rail_id, rail_data in self.rail_id_dictionary.items():
            if rail_data['meta'] and len(rail_data['junctions']) == 1:
                data = {'rail_id': rail_id}
                data.update(rail_data['meta'])
                data.update(rail_data['junctions'][0])
                single_junction.append(data)

        return single_junction

    def _convert_results_to_dictionary_list_multi_jiq(self):
        """rail_id_dictionary contains information for all the samples an is independent of the UI.
        Use this helper function to convert to extract what we want to show for the MULTI junction query table.
        """
        multi_junction = []
        for rail_id, rail_data in self.rail_id_dictionary.items():
            if rail_data['meta']:
                data = {gs.snpt_col_rail_id: rail_id}
                data.update(rail_data['meta'])

                # add the average psi
                num_junctions = len(rail_data['junctions'])
                data[gs.table_jiq_col_avg_psi] = rail_data['psi_sum'] / num_junctions

                for junction_index in range(0, num_junctions):
                    info = rail_data['junctions'][junction_index]
                    # NOTE: the output junction indices starts with 1 not 0
                    modified_dict = {f"{key}_{junction_index + 1}": value for key, value in info.items()}
                    data.update(modified_dict)

                multi_junction.append(data)

        return multi_junction

    @staticmethod
    def _find_junction(df, start, end):
        return df.loc[(df['start'] == start) & (df['end'] == end)]

    def run_junction_inclusion_query(self, meta_data_dict, df_snpt_results_dict, junctions_list,
                                     return_type: JiqReturnType):
        """Given the snaptron interface results in a map, this function calculates the Percent Spliced In (PSI)
        given the inclusion junction and the exclusion junctions. If multiple junctions are provided,
        each will be calculated separately.
        """
        # find the exclusion and inclusion junction rows
        for junction_index in range(0, len(junctions_list)):

            splice_junction_pair = junctions_list[junction_index]
            exc_junction_coordinates = splice_junction_pair[0]
            inc_junction_coordinates = splice_junction_pair[1]

            # exc_junction_coordinates must be in the map since it was created based on the coordinates before
            df_snpt_results = df_snpt_results_dict[exc_junction_coordinates]

            exc_junctions_df = self._find_junction(df_snpt_results,
                                                   exc_junction_coordinates.start, exc_junction_coordinates.end)
            inc_junctions_df = self._find_junction(df_snpt_results,
                                                   inc_junction_coordinates.start, inc_junction_coordinates.end)

            # if either one is empty the user has inputted wrong coordinates
            if exc_junctions_df.empty or inc_junctions_df.empty:
                raise exceptions.EmptyJunction

            # extract the 'sample' column form the row this is where all the samples and their count is
            exclusion_junction_samples = (exc_junctions_df[gs.snpt_col_samples]).tolist()
            inclusion_junction_samples = (inc_junctions_df[gs.snpt_col_samples]).tolist()

            # Gather results in a dictionary
            self._gather_samples_rail_id_and_counts(exclusion_junction_samples, 'exc', junction_index)
            self._gather_samples_rail_id_and_counts(inclusion_junction_samples, 'inc', junction_index)

        # For each rail id found, gather its metadata and calculate PSI values
        # this will populate self.gathered_rail_id_meta_data_and_psi
        for junction_index in range(0, len(junctions_list)):
            for rail_id in self.rail_id_dictionary:
                self._gather_rail_id_meta_data(rail_id, meta_data_dict, junction_index)

        query_results = {}
        if return_type == JiqReturnType.RAW:
            query_results = self.rail_id_dictionary
        elif return_type == JiqReturnType.LIST or return_type == JiqReturnType.INDEXED_PD:
            # returning a list of dictionaries not a dataframe for better coexistence with the front-end UI
            dict_list = self._convert_results_to_dictionary_list_single_jiq() if len(junctions_list) == 1 \
                else self._convert_results_to_dictionary_list_multi_jiq()

            # convert to dataframe if needed
            query_results = dict_list if return_type == JiqReturnType.LIST \
                else pandas.DataFrame(dict_list).set_index(gs.snpt_col_rail_id)

        return query_results
