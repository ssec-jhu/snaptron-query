import collections
from enum import StrEnum
from snaptron_query.app import exceptions, global_strings as gs, utils


class JunctionType(StrEnum):
    EXCLUSION = 'exc'
    INCLUSION = 'inc'


# note the fields in this named tuple must match the table column names of the JIQ
JIQ_CALCULATIONS = collections.namedtuple('JIQ_CALCULATIONS',
                                          [gs.table_jiq_col_psi, gs.table_jiq_col_inc,
                                           gs.table_jiq_col_exc, gs.table_jiq_col_total, gs.table_jiq_col_log_2])


def split_and_cast(sample):
    (rail_id, count) = sample.split(':')
    return int(rail_id), int(count)


def default_junctions_dict():
    # Note: this acts like a "default constructor" for every value of a key not found
    return {"meta": {}, "junctions": []}


def insert_value(list_of_junctions, junction_index, dict_items_to_add):
    # Extend the list if the index is larger than the current size
    if junction_index >= len(list_of_junctions):
        # fill it with default values list_of_junctions.extend([JIQ_CALCULATIONS(-1, 0, 0, 0, -1)._asdict() for _ in
        # range(junction_index - len(list_of_junctions) + 1)])
        list_of_junctions.extend([{'inc': 0, 'exc': 0} for _ in range(junction_index - len(list_of_junctions) + 1)])

    # Update the dictionary in the first list at the given index
    existing_dict = list_of_junctions[junction_index]
    existing_dict.update(dict_items_to_add)


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
                    insert_value(list_of_junctions=self.rail_id_dictionary[rail_id]['junctions'],
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

            # count totals
            total_count = inclusion_count + exclusion_count

            # TODO: PSI calculation tolerance of 15, PI must verify?
            psi = 0.0
            if total_count > 0:
                # calculate the percent spliced in
                psi = round(((100 * inclusion_count) / float(total_count)), 2)

            log2 = round(utils.log_2_plus(psi), 4)

            insert_value(list_of_junctions=self.rail_id_dictionary[rail_id]['junctions'],
                         junction_index=junction_index,
                         dict_items_to_add=JIQ_CALCULATIONS(psi, inclusion_count, exclusion_count, total_count,
                                                            log2)._asdict())

        except IndexError:
            # the rail id has no sample in the junction so populate with default values
            insert_value(list_of_junctions=self.rail_id_dictionary[rail_id]['junctions'],
                         junction_index=junction_index,
                         dict_items_to_add=JIQ_CALCULATIONS(0, 0, 0, 0, 0)._asdict())

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

    @staticmethod
    def _find_junction(df, start, end):
        return df.loc[(df['start'] == start) & (df['end'] == end)]

    def run_junction_inclusion_query(self, df, meta_data_dict, junctions_list):
        """Given the snaptron interface results, this function calculates the Percent Spliced In (PSI)
        given the inclusion junction and the exclusion junction
        """
        # find the exclusion and inclusion junction rows
        for junction_index in range(0, len(junctions_list)):
            (exclusion_start, exclusion_end, inclusion_start, inclusion_end) = junctions_list[junction_index]

            exc_junctions_df = self._find_junction(df, exclusion_start, exclusion_end)
            inc_junctions_df = self._find_junction(df, inclusion_start, inclusion_end)

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
            for rail_id in self.rail_id_dictionary:
                self._gather_rail_id_meta_data(rail_id, meta_data_dict, junction_index)

            # returning a list of dictionaries not a dataframe for better coexistence with the front-end UI
        return self.rail_id_dictionary


def convert_to_single_junction(rail_id_dictionary):
    """rail_id_dictionary contains information for all the samples an is independent of the UI.
    Use this helper function to convert to extract what we want to show for the SINGLE junction query table.
    """
    single_junction = []
    for rail_id in rail_id_dictionary:
        if rail_id_dictionary[rail_id]['meta'] and len(rail_id_dictionary[rail_id]['junctions']) == 1:
            data = {'rail_id': rail_id}
            data.update(rail_id_dictionary[rail_id]['meta'])
            data.update(rail_id_dictionary[rail_id]['junctions'][0])
            single_junction.append(data)

    return single_junction


def convert_to_multi_junction(rail_id_dictionary):
    """rail_id_dictionary contains information for all the samples an is independent of the UI.
        Use this helper function to convert to extract what we want to show for the MULTI junction query table.
        """
    multi_junction = []
    for rail_id in rail_id_dictionary:
        if rail_id_dictionary[rail_id]['meta']:
            data = {'rail_id': rail_id}
            data.update(rail_id_dictionary[rail_id]['meta'])
            for junction_index in range(0, len(rail_id_dictionary[rail_id]['junctions'])):
                info = rail_id_dictionary[rail_id]['junctions'][junction_index]
                modified_dict = {f"{key}_{junction_index}": value for key, value in info.items()}
                data.update(modified_dict)

            multi_junction.append(data)

    return multi_junction
