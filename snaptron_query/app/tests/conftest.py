from pathlib import Path

import pandas as pd
import pytest

from snaptron_query.app import global_strings as gs, utils
from snaptron_query.app import query_gene_expression as gex
from snaptron_query.app import query_junction_inclusion as jiq
from snaptron_query.app import snaptron_client as sc

path_srav3h_meta = Path(__file__).parent / 'data/test_srav3h_samples.tsv'
path_gtexv2_meta = Path(__file__).parent / 'data/test_gtexv2_samples.tsv'
path_tcgav2_meta = Path(__file__).parent / 'data/test_tcgav2_samples.tsv'
path_srav1m_meta = Path(__file__).parent / 'data/test_srav1m_samples.tsv'

path_sample_junction_data = Path(__file__).parent / 'data/test_chr19_4491836_4493702_srav3h.tsv'

path_ground_truth_data = Path(__file__).parent / 'data/test_shinyapp_chr19_4491836_4492014_chr19_4491836_4493702.csv'

path_gex_srav3h_meta = Path(__file__).parent / 'data/test_samples_SRAv3h_GEX.csv'
path_sample_gex_norm_data = Path(__file__).parent / 'data/test_srav3h_gene_norm_EDF1.csv'
path_sample_gex_query_data = Path(__file__).parent / 'data/test_srav3h_gene_query_TARDBP.csv'


class JunctionQuery:
    def __init__(self, junction_list, meta_data_dict, df_from_snaptron_map):
        # find the exclusion and inclusion junction rows
        self.query_mgr = jiq.JunctionInclusionQueryManager()
        df = pd.DataFrame(jiq.convert_to_single_junction
                          (self.query_mgr.run_junction_inclusion_query(meta_data_dict=meta_data_dict,
                                                                       df_snpt_results_dict=df_from_snaptron_map,
                                                                       junctions_list=junction_list)))
        self.df_jiq_results = df.set_index(gs.snpt_col_rail_id)

    def get_rail_id_dict(self):
        return self.query_mgr.get_rail_id_dictionary()

    def get_results(self):
        return self.df_jiq_results


class MultiJunctionQuery:
    def __init__(self, junction_list, meta_data_dict, df_from_snaptron_map):
        # find the exclusion and inclusion junction rows
        self.query_mgr = jiq.JunctionInclusionQueryManager()
        df = pd.DataFrame(utils.convert_to_multi_junction
                          (self.query_mgr.run_junction_inclusion_query(meta_data_dict=meta_data_dict,
                                                                       df_snpt_results_dict=df_from_snaptron_map,
                                                                       junctions_list=junction_list)))
        self.df_jiq_results = df.set_index(gs.snpt_col_rail_id)

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
        meta_data_dict = df_srav3h_meta_data.to_dict(orient='index')

        self.gex_mgr = gex.GeneExpressionQueryManager()

        # calculate factors
        self.gex_mgr.setup_normalization_data_method(norm_gene_id, df_snaptron_norm, meta_data_dict)

        self.results_list_of_dict = self.gex_mgr.run_gene_expression_query(query_gene_id,
                                                                           df_snaptron_query, meta_data_dict)

    def get_factor_table(self):
        return self.gex_mgr.normalization_factor_table

    def get_results(self):
        return pd.DataFrame(self.results_list_of_dict).set_index('rail_id')


@pytest.fixture(scope='session')
def junction_srav3h():
    meta_data_dict = utils.read_srav3h(path_srav3h_meta)
    df_sample_junctions_from_snaptron = pd.read_csv(path_sample_junction_data, sep='\t')

    splice_pair = sc.SpliceJunctionPair(exc_coordinates=sc.JunctionCoordinates(19, 4491836, 4493702),
                                        inc_coordinates=sc.JunctionCoordinates(19, 4491836, 4492014))
    df_sample_junctions_from_snaptron_map = {splice_pair.exc_coordinates: df_sample_junctions_from_snaptron}
    jq = JunctionQuery(junction_list=[splice_pair],
                       meta_data_dict=meta_data_dict,
                       df_from_snaptron_map=df_sample_junctions_from_snaptron_map)
    return jq


@pytest.fixture(scope='session')
def junction_gtexv2():
    # this is extracted from the GTEXv2 compilation
    meta_data_dict = utils.read_gtexv2(path_gtexv2_meta)
    path = Path(__file__).parent / 'data/test_chr19_4491836_4493702_gtexv2.tsv'
    df_sample_junctions_from_snaptron = pd.read_csv(path, sep='\t')

    splice_pair = sc.SpliceJunctionPair(exc_coordinates=sc.JunctionCoordinates(19, 4491836, 4493702),
                                        inc_coordinates=sc.JunctionCoordinates(19, 4491836, 4492014))
    df_sample_junctions_from_snaptron_map = {splice_pair.exc_coordinates: df_sample_junctions_from_snaptron}

    return JunctionQuery(junction_list=[splice_pair],
                         meta_data_dict=meta_data_dict,
                         df_from_snaptron_map=df_sample_junctions_from_snaptron_map)


@pytest.fixture(scope='session')
def junction_tcgav2():
    # this is extracted from the TCGAv2 compilation
    meta_data_dict = utils.read_tcgav2(path_tcgav2_meta)
    path = Path(__file__).parent / 'data/test_chr19_4491836_4493702_tcgav2.tsv'
    df_sample_junctions_from_snaptron = pd.read_csv(path, sep='\t')
    splice_pair = sc.SpliceJunctionPair(exc_coordinates=sc.JunctionCoordinates(19, 4491836, 4493702),
                                        inc_coordinates=sc.JunctionCoordinates(19, 4491836, 4492014))
    df_sample_junctions_from_snaptron_map = {splice_pair.exc_coordinates: df_sample_junctions_from_snaptron}

    return JunctionQuery(junction_list=[splice_pair],
                         meta_data_dict=meta_data_dict,
                         df_from_snaptron_map=df_sample_junctions_from_snaptron_map)


@pytest.fixture(scope='session')
def junction_srav1m():
    # this is extracted from the SRAv1m compilation
    meta_data_dict = utils.read_srav1m(path_srav1m_meta)
    path = Path(__file__).parent / 'data/test_chr8_71666671_71671625_srav1m.tsv'
    df_sample_junctions_from_snaptron = pd.read_csv(path, sep='\t')

    splice_pair = sc.SpliceJunctionPair(exc_coordinates=sc.JunctionCoordinates(8, 71666671, 71671625),
                                        inc_coordinates=sc.JunctionCoordinates(8, 71666671, 71667328))
    df_sample_junctions_from_snaptron_map = {splice_pair.exc_coordinates: df_sample_junctions_from_snaptron}

    return JunctionQuery(junction_list=[splice_pair],
                              meta_data_dict=meta_data_dict,
                              df_from_snaptron_map=df_sample_junctions_from_snaptron_map)


@pytest.fixture(scope='session')
def multi_junction_srav3h():
    meta_data_dict = utils.read_srav3h(path_srav3h_meta)
    df_sample_junctions_from_snaptron = pd.read_csv(path_sample_junction_data, sep='\t')

    # same exclusion junction in this example
    exc_junction = sc.JunctionCoordinates(19, 4491836, 4493702)
    junction_0 = sc.SpliceJunctionPair(exc_coordinates=exc_junction,
                                       inc_coordinates=sc.JunctionCoordinates(19, 4491836, 4492014))
    junction_1 = sc.SpliceJunctionPair(exc_coordinates=exc_junction,
                                       inc_coordinates=sc.JunctionCoordinates(19, 4492153, 4493702))

    return MultiJunctionQuery(junction_list=[junction_0, junction_1],
                              meta_data_dict=meta_data_dict,
                              df_from_snaptron_map={junction_0.exc_coordinates: df_sample_junctions_from_snaptron})


@pytest.fixture(scope='session')
def multi_junction_srav3h_2():
    meta_data_dict = utils.read_srav3h(path_srav3h_meta)
    df_sample_junctions_from_snaptron = pd.read_csv(path_sample_junction_data, sep='\t')

    exc_junction = sc.JunctionCoordinates(19, 4491836, 4493702)
    junction_0 = sc.SpliceJunctionPair(exc_coordinates=exc_junction,
                                       inc_coordinates=sc.JunctionCoordinates(19, 4491836, 4492014))
    junction_1 = sc.SpliceJunctionPair(exc_coordinates=exc_junction,
                                       inc_coordinates=sc.JunctionCoordinates(19, 4492153, 4493702))
    # reverse the junctions
    return MultiJunctionQuery(junction_list=[junction_1, junction_0],
                              meta_data_dict=meta_data_dict,
                              df_from_snaptron_map={junction_0.exc_coordinates: df_sample_junctions_from_snaptron})


@pytest.fixture(scope='session')
def multi_junction_srav3h_3():
    # this specific pair of junctions should have the psi_2 all 0
    meta_data_dict = utils.read_srav3h(path_srav3h_meta)
    df_sample_junctions_from_snaptron = pd.read_csv(
        Path(__file__).parent / 'data/test_chr7_98881251_98881974_srav3h.tsv', sep='\t')

    exc_junction = sc.JunctionCoordinates(7, 98881251, 98881974)
    junction_0 = sc.SpliceJunctionPair(exc_coordinates=exc_junction,
                                       inc_coordinates=sc.JunctionCoordinates(19, 98881251, 98881694))
    junction_1 = sc.SpliceJunctionPair(exc_coordinates=exc_junction,
                                       inc_coordinates=sc.JunctionCoordinates(19, 98881737, 98881974))

    mjq = MultiJunctionQuery(junction_list=[junction_0, junction_1],
                             meta_data_dict=meta_data_dict,
                             df_from_snaptron_map={junction_0.exc_coordinates: df_sample_junctions_from_snaptron})
    return mjq


@pytest.fixture(scope='session')
def multi_junction_srav1m_1():
    # this specific pair of junctions should have the psi_2 all 0
    meta_data_dict = utils.read_srav1m(path_srav1m_meta)
    df_sample_junctions_from_snaptron = pd.read_csv(
        Path(__file__).parent / 'data/test_chr8_71666671_71671625_srav1m.tsv', sep='\t')

    exc_junction = sc.JunctionCoordinates(8, 71666671, 71671625)
    junction_0 = sc.SpliceJunctionPair(exc_coordinates=exc_junction,
                                       inc_coordinates=sc.JunctionCoordinates(19, 71666671, 71667328))
    junction_1 = sc.SpliceJunctionPair(exc_coordinates=exc_junction,
                                       inc_coordinates=sc.JunctionCoordinates(19, 71667373, 71671625))

    return MultiJunctionQuery(junction_list=[junction_0, junction_1],
                              meta_data_dict=meta_data_dict,
                              df_from_snaptron_map={exc_junction: df_sample_junctions_from_snaptron})


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


@pytest.fixture(scope='session')
def compilations():
    return [gs.compilation_srav3h, gs.compilation_gtexv2, gs.compilation_tcgav2]


@pytest.fixture(scope='session')
def sample_ui_children():
    return [
        {'props': {'children': [
            {'props': {'children': {'props': {'children': 'Junction 1', 'size': 'sm', 'weight': 500}, 'type': 'Text'}}},
            {'props': {'children': {'props': {'id': 'id-input-jiq-inc-junc-0',
                                              'value': 'chr19:4491836-4492014'}, 'type': 'Input'}}},
            {'props': {'children': {'props': {'id': 'id-input-jiq-exc-junc-0',
                                              'value': 'chr19:4491836-4493702'}, 'type': 'Input'}}},
            {'props': {'children': [{'props': {'children': [
                {'props': {'children': {
                    'props': {'height': 16, 'icon': 'mdi:add-box', 'width': 16}}}, 'type': 'I'}, ' Add Junction'],
                'id': 'id-button-jiq-add-more-junctions'},
                'type': 'Button', 'namespace': 'dash_bootstrap_components'},
                {'props': {'children': 'Add more inclusion or exclusion junctions (up to 5) to the PSI query',
                           'target': 'id-button-jiq-add-more-junctions'}, 'type': 'Tooltip'}]}}
        ]}, 'type': 'Row'},
    ]


@pytest.fixture(scope='session')
def sample_ui_children_with_error():
    return [
        {'props': {'children': [
            {'props': {'children': {'props': {'children': 'Junction 1', 'size': 'sm', 'weight': 500}, 'type': 'Text'}}},
            {'props': {'children': {'props': {'id': 'id-input-jiq-inc-junc-0',
                                              }, 'type': 'Input'}}},
            {'props': {'children': {'props': {'id': 'id-input-jiq-exc-junc-0',
                                              'value': 'chr19:4491836-4493702'}, 'type': 'Input'}}},
            {'props': {'children': [{'props': {'children': [
                {'props': {'children': {
                    'props': {'height': 16, 'icon': 'mdi:add-box', 'width': 16}}}, 'type': 'I'}, ' Add Junction'],
                'id': 'id-button-jiq-add-more-junctions'},
                'type': 'Button', 'namespace': 'dash_bootstrap_components'},
                {'props': {'children': 'Add more inclusion or exclusion junctions (up to 5) to the PSI query',
                           'target': 'id-button-jiq-add-more-junctions'}, 'type': 'Tooltip'}]}}
        ]}, 'type': 'Row'},
    ]
