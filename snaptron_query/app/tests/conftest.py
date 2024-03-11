from pathlib import Path
import pandas as pd
import pytest
from snaptron_query.app import global_strings as gs
from snaptron_query.app import query_junction_inclusion as jiq

# path_srav3h_meta = os.path.join(os.path.dirname(__file__), 'data/test_samples_SRAv3h.csv')
path_srav3h_meta = Path(__file__).parent / 'data/test_samples_SRAv3h.csv'
path_ground_truth_data = Path(__file__).parent / 'data/test_shinyapp_chr19_4491836_4492014_chr19_4491836_4493702.csv'
path_sample_junction_data = Path(__file__).parent / 'data/test_srav3h_chr19_4491836_4493702.tsv'


class JunctionQuery:
    def __init__(self, exclusion_start, exclusion_end, inclusion_start, inclusion_end, file):
        df_srav3h_meta_data = pd.read_csv(path_srav3h_meta, usecols=gs.srav3h_meta_data_required_list).set_index(
            gs.snaptron_col_rail_id)

        df_from_snaptron = pd.read_csv(file, sep='\t')

        # find the exclusion and inclusion junction rows
        self.query_mgr = jiq.JunctionInclusionQueryManager(exclusion_start, exclusion_end,
                                                           inclusion_start, inclusion_end)

        df = pd.DataFrame(self.query_mgr.run_junction_inclusion_query(df_from_snaptron, df_srav3h_meta_data))
        self.df_jiq_results = df.set_index(gs.snaptron_col_rail_id)

    def get_query_mgr(self):
        return self.query_mgr

    def get_rail_id_dict(self):
        return self.query_mgr.get_rail_id_dictionary()

    def get_results(self):
        return self.df_jiq_results


@pytest.fixture(scope='session')
def junction():
    jq = JunctionQuery(4491836, 4493702, 4491836, 4492014, path_sample_junction_data)
    return jq


@pytest.fixture(scope='session')
def ground_truth_df():
    # sample data provided has been pruned to include samples with significant PSI>0
    # note when changing this data: rail_id is saved as sample_id from the PI website
    df_test_results = pd.read_csv(path_ground_truth_data).set_index('sample_id')
    return df_test_results
