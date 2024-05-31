import numpy as np
import pandas as pd

from snaptron_query.app import exceptions, global_strings as gs


def read_srav3h(file_path):
    # read the file and make sure index is set to the rail id for fast lookup
    return pd.read_csv(file_path, sep='\t',
                       usecols=gs.srav3h_meta_data_required_list,
                       dtype={'sample_description': 'string'}).set_index(gs.snpt_col_rail_id).to_dict(orient='index')


def read_srav1m(file_path):
    # read the file and make sure index is set to the rail id for fast lookup
    return pd.read_csv(file_path, sep='\t',
                       usecols=gs.srav1m_meta_data_required_list,
                       dtype={'sample_description': 'string'}).set_index(gs.snpt_col_rail_id).to_dict(orient='index')


def read_gtexv2(file_path):
    # read the file and make sure index is set to the rail id for fast lookup
    col_types = {item: 'string' for item in gs.gtexv2_meta_data_required_list[1:len(gs.gtexv2_meta_data_required_list)]}

    return pd.read_csv(file_path, sep='\t',
                       usecols=gs.gtexv2_meta_data_required_list,
                       dtype=col_types).set_index(gs.snpt_col_rail_id).to_dict(orient='index')


def read_tcgav2(file_path):
    # read the file and make sure index is set to the rail id for fast lookup
    col_types = {item: 'string' for item in gs.tcgav2_meta_data_required_list[1:len(gs.tcgav2_meta_data_required_list)]}
    return pd.read_csv(file_path, sep='\t',
                       usecols=gs.tcgav2_meta_data_required_list,
                       dtype=col_types).set_index(gs.snpt_col_rail_id).to_dict(orient='index')


def log_2_plus(x):
    return np.log2(x + gs.log_epsilon)


def get_component(input_id, list_of_children, component_index, junctions):
    element = list_of_children[component_index].get('props', {}).get('children', {}).get('props', {})
    input_id_ret = element.get('id', None)
    if input_id_ret == input_id:
        value = element.get('value', '')
        if value:
            junctions.append(value)
        else:
            raise exceptions.MissingUserInputs


def get_element_id_and_value(children, count):
    inc_junctions = []
    exc_junctions = []
    for i in range(count + 1):
        # Get the value of each input textbox
        # list_of_children = children[i].get('props', {}).get('children', [])
        list_of_children = children[i]['props']['children']

        # Get the first component which is the inclusion junction coordinated
        get_component(f'id-input-jiq-inc-junc-{i}', list_of_children, 1, inc_junctions)

        # Get the second component which is the exclusion junction coordinates
        get_component(f'id-input-jiq-exc-junc-{i}', list_of_children, 2, exc_junctions)

        # if one item was missing, stop the loop and don't iterate
        if len(inc_junctions) != len(exc_junctions):
            raise exceptions.MissingUserInputs

    return inc_junctions, exc_junctions


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
