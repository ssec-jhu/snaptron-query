from contextvars import copy_context

import dash.exceptions
import dash_bootstrap_components as dbc
import pandas as pd
import pytest
from dash import no_update
from dash._callback_context import context_value
from dash._utils import AttributeDict

import snaptron_query.app.global_strings as gs

TARDBP_coordinates = "Chromosome 1: 11,012,344-11,030,528"
EDF_coordinates = "Chromosome 9: 136,862,119-136,866,308"


@pytest.fixture()
def mock_get_snpt_query_results_df_geq(mocker, gex_data_srav3h_TARDBP, gex_data_srav3h_EDF1):
    # mock the httpx return results

    def args_based_return(*args, **kwargs):
        if kwargs == {"compilation": "SRAv3h", "query_mode": "genes", "region": "TARDBP"}:
            return gex_data_srav3h_TARDBP
        elif kwargs == {"compilation": "SRAv3h", "query_mode": "genes", "region": "EDF1"}:
            return gex_data_srav3h_EDF1
        elif kwargs == {"compilation": "SRAv3h", "query_mode": "genes", "region": "TARDBP-X"}:
            return pd.DataFrame()
        elif kwargs == kwargs == {"compilation": "SRAv3h", "query_mode": "genes", "region": "EDF1-X"}:
            return pd.DataFrame()
        elif kwargs == {"compilation": "SRAv3h", "query_mode": "genes", "region": "chr1:11012344-11030528"}:
            return gex_data_srav3h_TARDBP
        elif kwargs == {"compilation": "SRAv3h", "query_mode": "genes", "region": EDF_coordinates}:
            return gex_data_srav3h_EDF1
        else:
            return Exception("exception occurred inn args_based_return")

    mock = mocker.patch("snaptron_query.app.snaptron_client.get_snpt_query_results_df")

    # Set the side effect of the mock
    mock.side_effect = args_based_return
    return mock


@pytest.mark.parametrize(
    "compilation,use_coordinates,query_gene_id,query_gene_coordinates,normalize_data,norm_gene_id,norm_gene_coordinates",
    [
        # classic
        (gs.compilation_srav3h, False, "TARDBP", None, True, "EDF1", None),
        # don't normalize
        (gs.compilation_srav3h, False, "TARDBP", None, False, "EDF1", None),
        # use coordinates
        (gs.compilation_srav3h, True, "TARDBP", TARDBP_coordinates, True, "EDF1", EDF_coordinates),
    ],
)
def test_mock_on_button_click_geq_run(
    monkeypatch_meta_data,
    mock_get_snpt_query_results_df_geq,
    compilation,
    use_coordinates,
    query_gene_id,
    query_gene_coordinates,
    normalize_data,
    norm_gene_id,
    norm_gene_coordinates,
):
    def run_callback():
        from snaptron_query.app.main_dash_app import on_button_click_geq_run

        context_value.set(AttributeDict(**{"triggered_inputs": [{"prop_id": "id-results-cleared-geq.n_clicks"}]}))
        return on_button_click_geq_run(
            n_clicks=1,
            results_are_cleared=True,
            compilation=compilation,
            use_coordinates=use_coordinates,
            query_gene_id=query_gene_id,
            query_gene_coordinates=query_gene_coordinates,
            normalize_data=normalize_data,
            norm_gene_id=norm_gene_id,
            norm_gene_coordinates=norm_gene_coordinates,
            box_plot_log_x=True,
            violin_overlay=False,
            histogram_log_x=True,
            histogram_log_y=False,
        )

    ctx = copy_context()
    output = ctx.run(run_callback)
    assert len(output) == 13
    assert output[5] == no_update  # no alerts were given


def test_mock_on_button_click_geq_run_callback_with_incorrect_trigger(
    monkeypatch_meta_data, mock_get_snpt_query_results_df_geq
):
    def run_callback():
        from snaptron_query.app.main_dash_app import on_button_click_geq_run

        context_value.set(AttributeDict(**{"triggered_inputs": [{"prop_id": "id-results-cleared-geq-typo.n_clicks"}]}))
        return on_button_click_geq_run(
            n_clicks=1,
            results_are_cleared=True,
            compilation=gs.compilation_srav3h,
            use_coordinates=False,
            query_gene_id="TARDBP",
            query_gene_coordinates="",
            normalize_data=True,
            norm_gene_id="EDF1",
            norm_gene_coordinates="",
            box_plot_log_x=True,
            violin_overlay=False,
            histogram_log_x=True,
            histogram_log_y=False,
        )

    ctx = copy_context()
    with pytest.raises(dash.exceptions.PreventUpdate):
        ctx.run(run_callback)


@pytest.mark.parametrize(
    "compilation,use_coordinates,query_gene_id,query_gene_coordinates,normalize_data,norm_gene_id,norm_gene_coordinates",
    [
        # missing compilation
        (None, False, "TARDBP", None, True, "EDF1", None),
        # query gene not found
        (gs.compilation_srav3h, False, "TARDBP-X", None, True, "EDF1", None),
        # normalization gene not found
        (gs.compilation_srav3h, False, "TARDBP", None, True, "EDF1-X", None),
        # use coordinates but missing query coordinates
        (gs.compilation_srav3h, True, "TARDBP", None, True, "EDF1", EDF_coordinates),
        # use coordinates but missing norm coordinates
        (gs.compilation_srav3h, True, "TARDBP", TARDBP_coordinates, True, "EDF1", None),
        # normalize gene but user did not provide norm gene
        (gs.compilation_srav3h, False, "TARDBP-X", None, True, None, None),
    ],
)
def test_mock_on_button_click_geq_run_raises_alerts(
    monkeypatch_meta_data,
    mock_get_snpt_query_results_df_geq,
    compilation,
    use_coordinates,
    query_gene_id,
    query_gene_coordinates,
    normalize_data,
    norm_gene_id,
    norm_gene_coordinates,
):
    def run_callback():
        from snaptron_query.app.main_dash_app import on_button_click_geq_run

        context_value.set(AttributeDict(**{"triggered_inputs": [{"prop_id": "id-results-cleared-geq.n_clicks"}]}))
        return on_button_click_geq_run(
            n_clicks=1,
            results_are_cleared=True,
            compilation=compilation,
            use_coordinates=use_coordinates,
            query_gene_id=query_gene_id,
            query_gene_coordinates=query_gene_coordinates,
            normalize_data=normalize_data,
            norm_gene_id=norm_gene_id,
            norm_gene_coordinates=norm_gene_coordinates,
            box_plot_log_x=True,
            violin_overlay=False,
            histogram_log_x=True,
            histogram_log_y=False,
        )

    ctx = copy_context()
    output = ctx.run(run_callback)
    assert len(output) == 13
    assert isinstance(output[5][1], dbc.Alert)  # alerts was given
