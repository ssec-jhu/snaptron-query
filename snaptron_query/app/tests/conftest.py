import os
import pandas as pd
import pytest
from snaptron_query.app import query_junction_inclusion as jiq
from snaptron_query.app import global_strings as gs


path_srav3h_meta = os.path.join(os.path.dirname(__file__), 'data/test_samples_SRAv3h.csv')


def read_meta_srav3h():
    df = pd.read_csv(path_srav3h_meta, usecols=gs.srav3h_meta_data_required_list)
    # make sure you set the index
    return df.set_index(gs.snaptron_col_rail_id)


class JunctionQuery:
    def __init__(self, exclusion_start, exclusion_end, inclusion_start, inclusion_end, file):
        df_srav3h_meta_data = read_meta_srav3h()
        df_from_snaptron = pd.read_csv(file, sep='\t')

        # find the exclusion and inclusion junction rows
        self.query_mgr = jiq.JunctionInclusionQueryManager(exclusion_start, exclusion_end,
                                                           inclusion_start, inclusion_end)
        self.df_jiq_results = (
            self.query_mgr.run_junction_inclusion_query(df_from_snaptron, df_srav3h_meta_data).set_index
            (gs.snaptron_col_rail_id))

    def get_query_mgr(self):
        return self.query_mgr

    def get_rail_id_dict(self):
        return self.query_mgr.get_rail_id_dictionary()

    def get_results(self):
        return self.df_jiq_results


@pytest.fixture(scope='session', autouse=True)
def junction():
    data_path = os.path.join(os.path.dirname(__file__), 'data/test_srav3h_chr19_4491836_4493702.tsv')
    jq = JunctionQuery(4491836, 4493702, 4491836, 4492014, data_path)
    return jq
