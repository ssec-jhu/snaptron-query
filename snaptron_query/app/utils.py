import numpy as np
import pandas as pd

from snaptron_query.app import exceptions, global_strings as gs


def read_srav3h():
    # TODO: read the rest of the meta data files here as they become available
    # read the file and make sure index is set to the rail id for fast lookup
    df = pd.read_csv('data/samples_SRAv3h.tsv', sep='\t',
                     usecols=gs.srav3h_meta_data_required_list,
                     dtype={'sample_description': 'string'}).set_index(gs.snpt_col_rail_id)
    return df.to_dict(orient='index')


def log_2_function(df, y):
    # add th plus 1
    return np.log2(df[y] + 1)


def log_2_function_lists(array):
    # add th plus 1
    values_plus_one = np.array(array) + 1
    return np.log2(values_plus_one)


def log_2(x):
    return np.log2(x)


def get_element_id_and_value(children, count):
    inc_junctions = []
    exc_junctions = []
    for i in range(count + 1):
        # Get the value of each input textbox
        # list_of_children = children[i].get('props', {}).get('children', [])
        list_of_children = children[i]['props']['children']

        # Get the first component which is the inclusion junction coordinated
        inc_input_id = f'id-input-jiq-inc-junc-{i}'
        inc_element = list_of_children[1].get('props', {}).get('children', {}).get('props', {})
        inc_input_id_ret = inc_element.get('id', None)
        if inc_input_id_ret == inc_input_id:
            value = inc_element.get('value', '')
            if value:
                inc_junctions.append(value)
            else:
                raise exceptions.MissingUserInputs

        # Get the second component which is the exclusion junction coordinates
        exc_input_id = f'id-input-jiq-exc-junc-{i}'
        exc_element = list_of_children[2].get('props', {}).get('children', {}).get('props', {})
        exc_input_id_ret = exc_element.get('id', None)
        if exc_input_id_ret == exc_input_id:
            value = exc_element.get('value', '')
            if value:
                exc_junctions.append(value)
            else:
                raise exceptions.MissingUserInputs

        # if one item was missing, stop the loop and don't iterate
        if len(inc_junctions) != len(exc_junctions):
            raise exceptions.MissingUserInputs

    return inc_junctions, exc_junctions
