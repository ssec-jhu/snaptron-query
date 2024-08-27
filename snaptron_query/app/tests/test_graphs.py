import pandas as pd
import pytest

from snaptron_query.app import (
    graphs,
)


@pytest.mark.parametrize(
    "log_psi_values, violin_overlay, list_of_calculated_junctions",
    [
        (True, False, ["psi"]),
        (True, True, ["psi"]),
        (False, False, ["psi"]),
        (False, True, ["psi"]),
    ],
)
def test_box_plot_single_junction(junction_srav3h, log_psi_values, violin_overlay, list_of_calculated_junctions):
    # format returned is indexed so rail_id needs to be folded back for testing purposes
    df = junction_srav3h.get_results()
    df_with_index = df.reset_index()
    fig = graphs.get_box_plot_jiq(df_with_index, log_psi_values, violin_overlay, list_of_calculated_junctions)
    assert len(fig["data"]) == 1
    assert len(fig["data"][0]["y"]) > 0


@pytest.mark.parametrize(
    "log_psi_values, violin_overlay, list_of_calculated_junctions",
    [
        (True, False, ["psi_1", "psi_2"]),
        (True, True, ["psi_1", "psi_2"]),
        (False, False, ["psi_1", "psi_2"]),
        (False, True, ["psi_1", "psi_2"]),
    ],
)
def test_box_plot_multi_junction(multi_junction_srav3h, log_psi_values, violin_overlay, list_of_calculated_junctions):
    # format returned is indexed so rail_id needs to be folded back for testing purposes
    df = multi_junction_srav3h.get_results()
    df_with_index = df.reset_index()
    fig = graphs.get_box_plot_jiq(df_with_index, log_psi_values, violin_overlay, list_of_calculated_junctions)
    assert len(fig["data"]) == 2
    assert len(fig["data"][0]["y"]) > 0
    assert len(fig["data"][1]["y"]) > 0


@pytest.mark.parametrize(
    "log_psi_values, violin_overlay, list_of_calculated_junctions",
    [
        # single or multi junction
        (True, False, ["psi"]),
        (True, True, ["psi"]),
        (False, False, ["psi"]),
        (False, True, ["psi"]),
        (True, False, ["psi_1,psi_2"]),
        (True, True, ["psi_1,psi_2"]),
        (False, False, ["psi_1,psi_2"]),
        (False, True, ["psi_1,psi_2"]),
    ],
)
def test_box_plot_empty(junction_srav3h, log_psi_values, violin_overlay, list_of_calculated_junctions):
    df_with_index = pd.DataFrame()
    fig = graphs.get_box_plot_jiq(df_with_index, log_psi_values, violin_overlay, list_of_calculated_junctions)
    assert len(fig["data"]) > 0  # figure is created but empty data
    assert len(fig["data"][0]["y"]) == 0  # must be empty


@pytest.mark.parametrize(
    "log_psi_values, log_y, list_of_calculated_junctions",
    [
        (True, False, ["psi"]),
        (True, True, ["psi"]),
        (False, False, ["psi"]),
        (False, True, ["psi"]),
    ],
)
def test_histogram_single_junction(junction_srav3h, log_psi_values, log_y, list_of_calculated_junctions):
    # format returned is indexed so rail_id needs to be folded back for testing purposes
    df = junction_srav3h.get_results()
    df_with_index = df.reset_index()
    fig = graphs.get_histogram_jiq(df_with_index, log_psi_values, log_y, list_of_calculated_junctions)
    assert len(fig["data"]) == 1
    assert len(fig["data"][0]["x"]) > 0
    assert fig["data"][0]["nbinsx"] == 25


@pytest.mark.parametrize(
    "log_psi_values, log_y, list_of_calculated_junctions",
    [
        (True, False, ["psi_1", "psi_2"]),
        (True, True, ["psi_1", "psi_2"]),
        (False, False, ["psi_1", "psi_2"]),
        (False, True, ["psi_1", "psi_2"]),
    ],
)
def test_histogram_multi_junction(multi_junction_srav3h, log_psi_values, log_y, list_of_calculated_junctions):
    # format returned is indexed so rail_id needs to be folded back for testing purposes
    df = multi_junction_srav3h.get_results()
    df_with_index = df.reset_index()
    fig = graphs.get_histogram_jiq(df_with_index, log_psi_values, log_y, list_of_calculated_junctions)
    assert len(fig["data"]) == 2
    assert len(fig["data"][0]["x"]) > 0
    assert len(fig["data"][1]["x"]) > 0
    assert fig["data"][0]["nbinsx"] == 25


@pytest.mark.parametrize(
    "log_psi_values, violin_overlay, list_of_calculated_junctions",
    [
        # single or multi junction
        (True, False, ["psi"]),
        (True, True, ["psi"]),
        (False, False, ["psi"]),
        (False, True, ["psi"]),
        (True, False, ["psi_1,psi_2"]),
        (True, True, ["psi_1,psi_2"]),
        (False, False, ["psi_1,psi_2"]),
        (False, True, ["psi_1,psi_2"]),
    ],
)
def test_histogram_empty(junction_srav3h, log_psi_values, violin_overlay, list_of_calculated_junctions):
    fig = graphs.get_histogram_jiq(pd.DataFrame(), log_psi_values, violin_overlay, list_of_calculated_junctions)
    assert len(fig["data"]) == 0  # figure is created but empty data


@pytest.mark.parametrize(
    "log_values, violin_overlay",
    [
        (True, True),
        (True, False),
        (False, True),
        (False, False),
    ],
)
def test_get_box_plot_gene_expression_normalized(gene_query_srav3h_tardbp_with_edf1, log_values, violin_overlay):
    df = gene_query_srav3h_tardbp_with_edf1.get_results()
    df_with_index = df.reset_index()
    fig = graphs.get_box_plot_gene_expression(df_with_index, log_values, violin_overlay, True)
    assert len(fig["data"]) == 2
    assert len(fig["data"][0]["customdata"]) > 0
    assert len(fig["data"][0]["y"]) > 0
    assert len(fig["data"][1]["customdata"]) > 0
    assert len(fig["data"][1]["y"]) > 0


@pytest.mark.parametrize(
    "log_values, violin_overlay",
    [
        (True, True),
        (True, False),
        (False, True),
        (False, False),
    ],
)
def test_get_box_plot_gene_expression_not_normalized(gene_query_srav3h_tardbp_with_edf1, log_values, violin_overlay):
    df = gene_query_srav3h_tardbp_with_edf1.get_results()
    df_with_index = df.reset_index()
    fig = graphs.get_box_plot_gene_expression(df_with_index, log_values, violin_overlay, False)
    assert len(fig["data"]) == 1
    assert len(fig["data"][0]["customdata"]) > 0
    assert len(fig["data"][0]["y"]) > 0


@pytest.mark.parametrize(
    "log_count_values, log_y",
    [
        (True, True),
        (True, False),
        (False, True),
        (False, False),
    ],
)
def test_get_histogram_geq(gene_query_srav3h_tardbp_with_edf1, log_count_values, log_y):
    df = gene_query_srav3h_tardbp_with_edf1.get_results()
    df_with_index = df.reset_index()
    fig = graphs.get_histogram_geq(df_with_index, log_count_values, log_y)
    assert len(fig["data"]) == 1
    assert len(fig["data"][0]["x"]) > 0
    assert fig["data"][0]["nbinsx"] == 50
