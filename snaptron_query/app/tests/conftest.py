from pathlib import Path

import pandas as pd
import pytest

from snaptron_query.app import global_strings as gs, utils
from snaptron_query.app import query_gene_expression as gex
from snaptron_query.app import query_junction_inclusion as jiq
from snaptron_query.app import snaptron_client as sc

path_srav3h_meta = Path(__file__).parent / "data/test_srav3h_samples.tsv"
path_gtexv2_meta = Path(__file__).parent / "data/test_gtexv2_samples.tsv"
path_tcgav2_meta = Path(__file__).parent / "data/test_tcgav2_samples.tsv"
path_srav1m_meta = Path(__file__).parent / "data/test_srav1m_samples.tsv"
path_encode_meta = Path(__file__).parent / "data/test_encode_samples.tsv"

path_sample_junction_data_srav3h = Path(__file__).parent / "data/test_chr19_4491836_4493702_srav3h.tsv"

path_ground_truth_data = Path(__file__).parent / "data/test_shinyapp_chr19_4491836_4492014_chr19_4491836_4493702.csv"

path_gex_srav3h_meta = Path(__file__).parent / "data/test_samples_SRAv3h_GEX.csv"


class JunctionQuery:
    def __init__(self, compilation, junction_list, meta_data_dict, df_from_snaptron_map):
        # find the exclusion and inclusion junction rows
        self.query_mgr = jiq.JunctionInclusionQueryManager()
        self.df_jiq_results = self.query_mgr.run_junction_inclusion_query(
            compilation=compilation,
            meta_data_dict=meta_data_dict,
            df_snpt_results_dict=df_from_snaptron_map,
            junctions_list=junction_list,
            return_type=jiq.JiqReturnType.INDEXED_PD,
        )

    def get_rail_id_dict(self):
        return self.query_mgr.get_rail_id_dictionary()

    def get_results(self):
        return self.df_jiq_results


class MultiJunctionQuery:
    def __init__(
        self,
        compilation,
        junction_list,
        meta_data_dict,
        df_from_snaptron_map,
        data_return_type=jiq.JiqReturnType.INDEXED_PD,
    ):
        # find the exclusion and inclusion junction rows
        self.query_mgr = jiq.JunctionInclusionQueryManager()
        self.jiq_results = self.query_mgr.run_junction_inclusion_query(
            compilation=compilation,
            meta_data_dict=meta_data_dict,
            df_snpt_results_dict=df_from_snaptron_map,
            junctions_list=junction_list,
            return_type=data_return_type,
        )

    def get_rail_id_dict(self):
        return self.query_mgr.get_rail_id_dictionary()

    def get_results(self):
        return self.jiq_results


class GEXQuery:
    def __init__(
        self,
        compilation,
        query_gene_id,
        query_gene_snaptron_data,
        query_gene_meta_data_dict,
        norm_gene_id=None,
        norm_gene_snaptron_data=None,
        norm_gene_meta_data_dict=None,
    ):
        self.gex_mgr = gex.GeneExpressionQueryManager()

        # calculate factors
        if norm_gene_id:
            self.gex_mgr.setup_normalization_data_method(
                norm_gene_id, norm_gene_snaptron_data, norm_gene_meta_data_dict
            )

        self.results_list_of_dict = self.gex_mgr.run_gene_expression_query(
            gene_id_query=query_gene_id,
            df_snaptron_results_query=query_gene_snaptron_data,
            meta_data_dict=query_gene_meta_data_dict,
            compilation=compilation,
        )

    def get_factor_table(self):
        return self.gex_mgr.normalization_factor_table

    def get_results(self):
        return pd.DataFrame(self.results_list_of_dict).set_index(gs.snpt_col_rail_id)


@pytest.fixture
def monkeypatch_meta_data(monkeypatch):
    """ "
    path to the metadata files has been mocked here to read the sample metadata file
    """
    meta_dir = Path(__file__).parent / "data/"
    from snaptron_query.app import paths

    monkeypatch.setattr(paths, "meta_data_directory", meta_dir)
    monkeypatch.setattr(paths, "srav3h_meta", path_srav3h_meta)
    monkeypatch.setattr(paths, "gtexv2_meta", path_gtexv2_meta)
    monkeypatch.setattr(paths, "tcgav2_meta", path_tcgav2_meta)
    monkeypatch.setattr(paths, "srav1m_meta", path_srav1m_meta)
    monkeypatch.setattr(paths, "encode_meta", path_encode_meta)


@pytest.fixture(scope="session")
def junction_pair_human_1():
    return sc.SpliceJunctionPair(
        exc_coordinates=sc.JunctionCoordinates(chr="chr19", start=4491836, end=4493702),
        inc_coordinates=sc.JunctionCoordinates(chr="chr19", start=4491836, end=4492014),
    )


@pytest.fixture(scope="session")
def junction_pair_human_2():
    return sc.SpliceJunctionPair(
        exc_coordinates=sc.JunctionCoordinates(chr="chr19", start=4491836, end=4493702),
        inc_coordinates=sc.JunctionCoordinates(chr="chr19", start=4492153, end=4493702),
    )


@pytest.fixture(scope="session")
def junction_pair_human_3():
    return sc.SpliceJunctionPair(
        exc_coordinates=sc.JunctionCoordinates(chr="chr7", start=98881251, end=98881974),
        inc_coordinates=sc.JunctionCoordinates(chr="chr19", start=98881251, end=98881694),
    )


@pytest.fixture(scope="session")
def junction_pair_human_4():
    return sc.SpliceJunctionPair(
        exc_coordinates=sc.JunctionCoordinates(chr="chr7", start=98881251, end=98881974),
        inc_coordinates=sc.JunctionCoordinates(chr="chr19", start=98881737, end=98881974),
    )


@pytest.fixture(scope="session")
def junction_pair_mouse_1():
    return sc.SpliceJunctionPair(
        exc_coordinates=sc.JunctionCoordinates(chr="chr8", start=71666671, end=71671625),
        inc_coordinates=sc.JunctionCoordinates(chr="chr19", start=71666671, end=71667328),
    )


@pytest.fixture(scope="session")
def junction_pair_mouse_2():
    return sc.SpliceJunctionPair(
        exc_coordinates=sc.JunctionCoordinates(chr="chr8", start=71666671, end=71671625),
        inc_coordinates=sc.JunctionCoordinates(chr="chr19", start=71667373, end=71671625),
    )


@pytest.fixture(scope="session")
def df_sample_junctions_from_srav3h():
    return pd.read_csv(path_sample_junction_data_srav3h, sep="\t")


@pytest.fixture(scope="session")
def meta_data_dict_srav3h():
    return utils.read_srav3h(path_srav3h_meta)


@pytest.fixture(scope="session")
def meta_data_dict_srav1m():
    return utils.read_srav1m(path_srav1m_meta)


@pytest.fixture(scope="session")
def gex_data_srav3h_TARDBP():
    path = Path(__file__).parent / "data/test_srav3h_gene_query_TARDBP.csv"
    return pd.read_csv(path)


@pytest.fixture(scope="session")
def gex_data_srav3h_EDF1():
    path = Path(__file__).parent / "data/test_srav3h_gene_norm_EDF1.csv"
    return pd.read_csv(path)


@pytest.fixture(scope="session")
def gex_data_srav1m_ADNP2():
    path = Path(__file__).parent / "data/test_srav1m_gene_query_ADNP2.csv"
    return pd.read_csv(path)


@pytest.fixture(scope="session")
def junction_srav3h(df_sample_junctions_from_srav3h, meta_data_dict_srav3h, junction_pair_human_1):
    df_sample_junctions_from_snaptron_map = {junction_pair_human_1.exc_coordinates: df_sample_junctions_from_srav3h}
    jq = JunctionQuery(
        compilation=gs.compilation_srav3h,
        junction_list=[junction_pair_human_1],
        meta_data_dict=meta_data_dict_srav3h,
        df_from_snaptron_map=df_sample_junctions_from_snaptron_map,
    )
    return jq


@pytest.fixture(scope="session")
def junction_gtexv2(junction_pair_human_1):
    # this is extracted from the GTEXv2 compilation
    meta_data_dict = utils.read_gtexv2(path_gtexv2_meta)
    path = Path(__file__).parent / "data/test_chr19_4491836_4493702_gtexv2.tsv"
    df_sample_junctions_from_snaptron = pd.read_csv(path, sep="\t")

    df_sample_junctions_from_snaptron_map = {junction_pair_human_1.exc_coordinates: df_sample_junctions_from_snaptron}

    return JunctionQuery(
        compilation=gs.compilation_gtexv2,
        junction_list=[junction_pair_human_1],
        meta_data_dict=meta_data_dict,
        df_from_snaptron_map=df_sample_junctions_from_snaptron_map,
    )


@pytest.fixture(scope="session")
def junction_tcgav2(junction_pair_human_1):
    # this is extracted from the TCGAv2 compilation
    meta_data_dict = utils.read_tcgav2(path_tcgav2_meta)
    path = Path(__file__).parent / "data/test_chr19_4491836_4493702_tcgav2.tsv"
    df_sample_junctions_from_snaptron = pd.read_csv(path, sep="\t")

    df_sample_junctions_from_snaptron_map = {junction_pair_human_1.exc_coordinates: df_sample_junctions_from_snaptron}

    return JunctionQuery(
        compilation=gs.compilation_tcgav2,
        junction_list=[junction_pair_human_1],
        meta_data_dict=meta_data_dict,
        df_from_snaptron_map=df_sample_junctions_from_snaptron_map,
    )


@pytest.fixture(scope="session")
def junction_srav1m(meta_data_dict_srav1m, junction_pair_mouse_1):
    # this is extracted from the SRAv1m compilation
    path = Path(__file__).parent / "data/test_chr8_71666671_71671625_srav1m.tsv"
    df_sample_junctions_from_snaptron = pd.read_csv(path, sep="\t")

    df_sample_junctions_from_snaptron_map = {junction_pair_mouse_1.exc_coordinates: df_sample_junctions_from_snaptron}

    return JunctionQuery(
        compilation=gs.compilation_srav1m,
        junction_list=[junction_pair_mouse_1],
        meta_data_dict=meta_data_dict_srav1m,
        df_from_snaptron_map=df_sample_junctions_from_snaptron_map,
    )


@pytest.fixture(scope="session")
def junction_encode(junction_pair_human_1):
    # this is extracted from the encode compilation
    meta_data_dict = utils.read_encode(path_encode_meta)
    path = Path(__file__).parent / "data/test_chr19_4491836_4493702_encode.tsv"
    df_sample_junctions_from_snaptron = pd.read_csv(path, sep="\t")

    df_sample_junctions_from_snaptron_map = {junction_pair_human_1.exc_coordinates: df_sample_junctions_from_snaptron}

    return JunctionQuery(
        compilation=gs.compilation_encode,
        junction_list=[junction_pair_human_1],
        meta_data_dict=meta_data_dict,
        df_from_snaptron_map=df_sample_junctions_from_snaptron_map,
    )


@pytest.fixture(scope="session")
def multi_junction_srav3h(
    df_sample_junctions_from_srav3h, meta_data_dict_srav3h, junction_pair_human_1, junction_pair_human_2
):
    # same exclusion junction in this example
    return MultiJunctionQuery(
        compilation=gs.compilation_srav3h,
        junction_list=[junction_pair_human_1, junction_pair_human_2],
        meta_data_dict=meta_data_dict_srav3h,
        df_from_snaptron_map={junction_pair_human_1.exc_coordinates: df_sample_junctions_from_srav3h},
    )


@pytest.fixture(scope="session")
def multi_junction_srav3h_raw_results(
    df_sample_junctions_from_srav3h, meta_data_dict_srav3h, junction_pair_human_1, junction_pair_human_2
):
    # this test fixture is similar to multi_junction_srav3h fixture but the fixture
    # requests a different return type from the query
    return MultiJunctionQuery(
        compilation=gs.compilation_srav3h,
        junction_list=[junction_pair_human_1, junction_pair_human_2],
        meta_data_dict=meta_data_dict_srav3h,
        df_from_snaptron_map={junction_pair_human_1.exc_coordinates: df_sample_junctions_from_srav3h},
        data_return_type=jiq.JiqReturnType.RAW,
    )


@pytest.fixture(scope="session")
def multi_junction_srav3h_2(
    df_sample_junctions_from_srav3h, meta_data_dict_srav3h, junction_pair_human_1, junction_pair_human_2
):
    # this test fixture is similar to multi_junction_srav3h fixture but the fixture
    # reverses the junction pairs orders to ensure results are the same regardless of the ordering of the pairs.
    # this will also test junction indexing in the rail id dictionary

    # reverse the junctions
    return MultiJunctionQuery(
        compilation=gs.compilation_srav3h,
        junction_list=[junction_pair_human_2, junction_pair_human_1],
        meta_data_dict=meta_data_dict_srav3h,
        df_from_snaptron_map={junction_pair_human_1.exc_coordinates: df_sample_junctions_from_srav3h},
    )


@pytest.fixture(scope="session")
def multi_junction_srav3h_3(meta_data_dict_srav3h, junction_pair_human_3, junction_pair_human_4):
    # this specific pair of junctions should have the psi_2 all 0
    df_sample_junctions_from_snaptron = pd.read_csv(
        Path(__file__).parent / "data/test_chr7_98881251_98881974_srav3h.tsv", sep="\t"
    )

    return MultiJunctionQuery(
        compilation=gs.compilation_srav3h,
        junction_list=[junction_pair_human_3, junction_pair_human_4],
        meta_data_dict=meta_data_dict_srav3h,
        df_from_snaptron_map={junction_pair_human_3.exc_coordinates: df_sample_junctions_from_snaptron},
    )


@pytest.fixture(scope="session")
def multi_junction_srav3h_one_empty_inclusion(
    df_sample_junctions_from_srav3h, meta_data_dict_srav3h, junction_pair_human_1, junction_pair_human_2
):
    # the third inclusion junction does not exist and should throw an error with the index specified
    junction_3 = sc.SpliceJunctionPair(
        exc_coordinates=sc.JunctionCoordinates("chr19", 4491836, 4493702),
        inc_coordinates=sc.JunctionCoordinates("chr19", 4056797, 4643209),
    )
    j_list = [junction_pair_human_1, junction_pair_human_2, junction_3]
    df_from_snaptron_map = {junction_pair_human_1.exc_coordinates: df_sample_junctions_from_srav3h}
    return j_list, df_from_snaptron_map


@pytest.fixture(scope="session")
def multi_junction_srav1m_1(meta_data_dict_srav1m, junction_pair_mouse_1, junction_pair_mouse_2):
    # this specific pair of junctions should have the psi_2 all 0
    df_sample_junctions_from_snaptron = pd.read_csv(
        Path(__file__).parent / "data/test_chr8_71666671_71671625_srav1m.tsv", sep="\t"
    )
    return MultiJunctionQuery(
        compilation=gs.compilation_srav1m,
        junction_list=[junction_pair_mouse_1, junction_pair_mouse_2],
        meta_data_dict=meta_data_dict_srav1m,
        df_from_snaptron_map={junction_pair_mouse_1.exc_coordinates: df_sample_junctions_from_snaptron},
    )


@pytest.fixture(scope="session")
def ground_truth_df():
    # sample data provided has been pruned to include samples with significant PSI>0
    # note when changing this data: rail_id is saved as sample_id from the PI website
    df_test_results = pd.read_csv(path_ground_truth_data).set_index("sample_id")
    return df_test_results


@pytest.fixture(scope="session")
def compilations():
    return [gs.compilation_srav3h, gs.compilation_gtexv2, gs.compilation_tcgav2]


@pytest.fixture(scope="session")
def gene_query_srav3h_tardbp_with_edf1(meta_data_dict_srav3h, gex_data_srav3h_TARDBP, gex_data_srav3h_EDF1):
    return GEXQuery(
        compilation=gs.compilation_srav3h,
        query_gene_id="TARDBP",
        query_gene_snaptron_data=gex_data_srav3h_TARDBP,
        query_gene_meta_data_dict=meta_data_dict_srav3h,
        norm_gene_id="EDF1",
        norm_gene_snaptron_data=gex_data_srav3h_EDF1,
        norm_gene_meta_data_dict=meta_data_dict_srav3h,
    )


@pytest.fixture(scope="session")
def gene_query_case_sensitive_srav3h_tardbp_with_edf1(
    meta_data_dict_srav3h, gex_data_srav3h_TARDBP, gex_data_srav3h_EDF1
):
    return GEXQuery(
        compilation=gs.compilation_srav3h,
        query_gene_id="taRdBp",
        query_gene_snaptron_data=gex_data_srav3h_TARDBP,
        query_gene_meta_data_dict=meta_data_dict_srav3h,
        norm_gene_id="eDf1",
        norm_gene_snaptron_data=gex_data_srav3h_EDF1,
        norm_gene_meta_data_dict=meta_data_dict_srav3h,
    )


@pytest.fixture(scope="session")
def gene_query_case_sensitive_srav1m_ADNP2_not_normalized(meta_data_dict_srav1m, gex_data_srav1m_ADNP2):
    # mouse datasets have the ensembles in lowercase
    return GEXQuery(
        compilation=gs.compilation_srav1m,
        query_gene_id="aDnp2",
        query_gene_snaptron_data=gex_data_srav1m_ADNP2,
        query_gene_meta_data_dict=meta_data_dict_srav1m,
    )


@pytest.fixture(scope="session")
def gene_query_case_sensitive_srav1m_adnp2_with_edf1(
    meta_data_dict_srav1m, gex_data_srav1m_ADNP2, meta_data_dict_srav3h, gex_data_srav3h_EDF1
):
    # mouse datasets have the ensembles in lowercase
    return GEXQuery(
        compilation=gs.compilation_srav1m,
        query_gene_id="aDnp2",
        query_gene_snaptron_data=gex_data_srav1m_ADNP2,
        query_gene_meta_data_dict=meta_data_dict_srav1m,
        norm_gene_id="eDf1",
        norm_gene_snaptron_data=gex_data_srav3h_EDF1,
        norm_gene_meta_data_dict=meta_data_dict_srav3h,
    )


@pytest.fixture(scope="session")
def sample_ui_children():
    return [
        {
            "props": {
                "children": [
                    {
                        "props": {
                            "children": {
                                "props": {"children": "Junction 1", "size": "sm", "weight": 500},
                                "type": "Text",
                            }
                        }
                    },
                    {
                        "props": {
                            "children": {
                                "props": {"id": "id-input-jiq-inc-junc-0", "value": "chr19:4491836-4492014"},
                                "type": "Input",
                            }
                        }
                    },
                    {
                        "props": {
                            "children": {
                                "props": {"id": "id-input-jiq-exc-junc-0", "value": "chr19:4491836-4493702"},
                                "type": "Input",
                            }
                        }
                    },
                    {
                        "props": {
                            "children": [
                                {
                                    "props": {
                                        "children": [
                                            {
                                                "props": {
                                                    "children": {
                                                        "props": {"height": 16, "icon": "mdi:add-box", "width": 16}
                                                    }
                                                },
                                                "type": "I",
                                            },
                                            " Add Junction",
                                        ],
                                        "id": "id-button-jiq-add-more-junctions",
                                    },
                                    "type": "Button",
                                    "namespace": "dash_bootstrap_components",
                                },
                                {
                                    "props": {
                                        "children": "Add more inclusion or exclusion junctions (up to 5) to the PSI "
                                        "query",
                                        "target": "id-button-jiq-add-more-junctions",
                                    },
                                    "type": "Tooltip",
                                },
                            ]
                        }
                    },
                ]
            },
            "type": "Row",
        },
    ]


@pytest.fixture(scope="session")
def sample_ui_children_with_error():
    return [
        {
            "props": {
                "children": [
                    {
                        "props": {
                            "children": {
                                "props": {"children": "Junction 1", "size": "sm", "weight": 500},
                                "type": "Text",
                            }
                        }
                    },
                    {
                        "props": {
                            "children": {
                                "props": {
                                    "id": "id-input-jiq-inc-junc-0",
                                },
                                "type": "Input",
                            }
                        }
                    },
                    {
                        "props": {
                            "children": {
                                "props": {"id": "id-input-jiq-exc-junc-0", "value": "chr19:4491836-4493702"},
                                "type": "Input",
                            }
                        }
                    },
                    {
                        "props": {
                            "children": [
                                {
                                    "props": {
                                        "children": [
                                            {
                                                "props": {
                                                    "children": {
                                                        "props": {"height": 16, "icon": "mdi:add-box", "width": 16}
                                                    }
                                                },
                                                "type": "I",
                                            },
                                            " Add Junction",
                                        ],
                                        "id": "id-button-jiq-add-more-junctions",
                                    },
                                    "type": "Button",
                                    "namespace": "dash_bootstrap_components",
                                },
                                {
                                    "props": {
                                        "children": "Add more inclusion or exclusion junctions (up to 5) to the PSI "
                                        "query",
                                        "target": "id-button-jiq-add-more-junctions",
                                    },
                                    "type": "Tooltip",
                                },
                            ]
                        }
                    },
                ]
            },
            "type": "Row",
        },
    ]
