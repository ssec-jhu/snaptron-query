from pathlib import Path
import pandas as pd
import pytest
from snaptron_query.app import global_strings as gs
from snaptron_query.app import query_junction_inclusion as jiq
from snaptron_query.app import query_gene_expression as gex

# path_srav3h_meta = os.path.join(os.path.dirname(__file__), 'data/test_samples_SRAv3h.csv')
path_srav3h_meta = Path(__file__).parent / 'data/test_samples_SRAv3h.csv'
path_ground_truth_data = Path(__file__).parent / 'data/test_shinyapp_chr19_4491836_4492014_chr19_4491836_4493702.csv'
path_sample_junction_data = Path(__file__).parent / 'data/test_srav3h_chr19_4491836_4493702.tsv'

path_gex_srav3h_meta = Path(__file__).parent / 'data/test_samples_SRAv3h_GEX.csv'
path_sample_gex_norm_data = Path(__file__).parent / 'data/test_srav3h_gene_norm_EDF1.csv'
path_sample_gex_query_data = Path(__file__).parent / 'data/test_srav3h_gene_query_TARDBP.csv'


class JunctionQuery:
    def __init__(self, exclusion_start, exclusion_end, inclusion_start, inclusion_end, file):
        df_srav3h_meta_data = pd.read_csv(path_srav3h_meta, usecols=gs.srav3h_meta_data_required_list).set_index(
            gs.snpt_col_rail_id)

        df_from_snaptron = pd.read_csv(file, sep='\t')

        # find the exclusion and inclusion junction rows
        self.query_mgr = jiq.JunctionInclusionQueryManager(exclusion_start, exclusion_end,
                                                           inclusion_start, inclusion_end)

        df = pd.DataFrame(self.query_mgr.run_junction_inclusion_query(df_from_snaptron, df_srav3h_meta_data))
        self.df_jiq_results = df.set_index(gs.snpt_col_rail_id)

    def get_query_mgr(self):
        return self.query_mgr

    def get_rail_id_dict(self):
        return self.query_mgr.get_rail_id_dictionary()

    def get_results(self):
        return self.df_jiq_results


class GEXQuery:
    def __init__(self, query_gene_id, norm_gene_id):
        df_snaptron_norm = pd.read_csv(path_sample_gex_norm_data)  # Note: query_gene_coord = 'chr1:11012654-11025492'
        df_snaptron_query = pd.read_csv(path_sample_gex_query_data)  # Note: query_gene_coord = 'chr1:11012654-11025492'
        df_srav3h_meta_data = pd.read_csv(path_gex_srav3h_meta, usecols=gs.srav3h_meta_data_required_list).set_index(
            gs.snpt_col_rail_id)

        self.gex_mgr = gex.GeneExpressionQueryManager()
        self.gex_mgr.setup_normalization_data_method_2_opt(norm_gene_id, df_snaptron_norm, df_srav3h_meta_data)
        self.results_list_of_dict = self.gex_mgr.run_gene_expression_query(query_gene_id, df_snaptron_query,
                                                                           df_srav3h_meta_data)

    def get_factor_table(self):
        return self.gex_mgr.normalization_factor_table

    def get_results(self):
        return pd.DataFrame(self.results_list_of_dict).set_index('rail_id')


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


@pytest.fixture(scope='session')
def gene_query():
    # return GEXQuery('ENSG00000120948', 'ENSG00000107223')
    return GEXQuery('TARDBP', 'EDF1')
