import pytest

from snaptron_query.app import (
    column_defs,
    global_strings as gs,
)


@pytest.mark.parametrize(
    "string, result",
    [(gs.snpt_col_rail_id, "Rail_Id"), (gs.snpt_col_external_id, "External_Id")],
)
def test_capitalize_underscored_string(string, result):
    assert result == column_defs.capitalize_underscored_string(string)


def test_get_rail_id():
    assert column_defs.get_rail_id()[0]["field"] == gs.snpt_col_rail_id
    assert column_defs.get_col_meta_tcgav2_before()[0]["field"] == gs.snpt_col_rail_id
    assert column_defs.get_col_meta_gtexv2_before()[0]["field"] == gs.snpt_col_rail_id
    assert column_defs.get_col_meta_encode_before()[0]["field"] == gs.snpt_col_rail_id


def test_get_generic_col():
    assert len(column_defs.get_generic_col("my_item")) == 1
    assert column_defs.get_generic_col("my_item")[0]["field"] == "my_item"


@pytest.mark.parametrize(
    "index, value",
    [
        (0, gs.snpt_col_rail_id),
        (1, gs.snpt_col_external_id),
        (2, gs.snpt_col_study),
        (3, gs.snpt_col_study_title),
    ],
)
def test_get_col_meta_srav3h_a(index, value):
    assert len(column_defs.get_col_meta_srav3h_before()) == 4
    assert column_defs.get_col_meta_srav3h_before()[index]["field"] == value


@pytest.mark.parametrize(
    "index, value",
    [
        (0, gs.snpt_col_sample_name),
        (1, gs.snpt_col_sample_title),
        (2, gs.snpt_col_library_layout),
        (3, gs.snpt_col_sample_description),
    ],
)
def test_get_col_meta_srav3h_b(index, value):
    assert column_defs.get_col_meta_srav3h_after()[index]["field"] == value


@pytest.mark.parametrize(
    "index, value",
    [
        (0, gs.snpt_col_rail_id),
        (1, gs.snpt_col_gdc_prim_site),
        (2, gs.snpt_col_study),
    ],
)
def test_get_col_meta_tcgav2_a(index, value):
    assert len(column_defs.get_col_meta_tcgav2_before()) == 3
    assert column_defs.get_col_meta_tcgav2_before()[index]["field"] == value


@pytest.mark.parametrize(
    "index, value",
    [
        (0, "tcga_barcode"),
        (1, "gdc_cases.project.name"),
    ],
)
def test_get_col_meta_tcgav2_b(index, value):
    assert len(column_defs.get_col_meta_tcgav2_after()) == 15
    assert column_defs.get_col_meta_tcgav2_after()[index]["field"] == value


@pytest.mark.parametrize(
    "index, value",
    [
        (0, gs.snpt_col_rail_id),
        (1, gs.snpt_col_run_acc),
        (2, gs.snpt_col_study),
    ],
)
def test_get_col_meta_gtexv2_a(index, value):
    assert len(column_defs.get_col_meta_gtexv2_before()) == 3
    assert column_defs.get_col_meta_gtexv2_before()[index]["field"] == value


@pytest.mark.parametrize(
    "index, value",
    [
        (0, gs.snpt_col_sex),
        (1, gs.snpt_col_caps_age),
        (2, gs.snpt_col_SUBJID),
        (3, gs.snpt_col_SAMPID),
        (4, gs.snpt_col_smts),
        (5, gs.snpt_col_smtsd),
    ],
)
def test_get_col_meta_gtexv2_b(index, value):
    assert len(column_defs.get_col_meta_gtexv2_after()) == 6
    assert column_defs.get_col_meta_gtexv2_after()[index]["field"] == value


@pytest.mark.parametrize(
    "index, value",
    [
        (0, gs.snpt_col_rail_id),
        (1, gs.snpt_col_exp_acc),
        (2, gs.snpt_col_cell_line),
        (3, gs.snpt_col_exp_target),
    ],
)
def test_get_col_meta_encode_a(index, value):
    assert len(column_defs.get_col_meta_encode_before()) == 4
    assert column_defs.get_col_meta_encode_before()[index]["field"] == value


@pytest.mark.parametrize(
    "index, value",
    [
        (0, gs.snpt_col_biosamp_life_stage),
        (1, gs.snpt_col_biosamp_life_sex),
        (2, gs.snpt_col_biosamp_life_age),
        (3, gs.snpt_col_assay),
        (4, gs.snpt_col_exp_date_rel),
    ],
)
def test_get_col_meta_encode_b(index, value):
    assert len(column_defs.get_col_meta_encode_after()) == 5
    assert column_defs.get_col_meta_encode_after()[index]["field"] == value


@pytest.mark.parametrize(
    "compilation, junction_count, index, value",
    [  # multi junction query on srav3h
        (gs.compilation_srav3h, 2, 0, gs.snpt_col_rail_id),
        (gs.compilation_srav3h, 2, 1, gs.snpt_col_external_id),
        (gs.compilation_srav3h, 2, 2, gs.snpt_col_study),
        (gs.compilation_srav3h, 2, 3, gs.snpt_col_study_title),
        (gs.compilation_srav3h, 2, 4, "avg_psi"),
        (gs.compilation_srav3h, 2, 5, "psi_1"),
        # three junctions same compilation
        (gs.compilation_srav3h, 3, 0, gs.snpt_col_rail_id),
        (gs.compilation_srav3h, 3, 1, gs.snpt_col_external_id),
        (gs.compilation_srav3h, 3, 2, gs.snpt_col_study),
        (gs.compilation_srav3h, 3, 3, gs.snpt_col_study_title),
        (gs.compilation_srav3h, 3, 4, "avg_psi"),
        (gs.compilation_srav3h, 3, 5, "psi_1"),
        # four junctions same compilation
        (gs.compilation_srav3h, 4, 0, gs.snpt_col_rail_id),
        (gs.compilation_srav3h, 4, 1, gs.snpt_col_external_id),
        (gs.compilation_srav3h, 4, 2, gs.snpt_col_study),
        (gs.compilation_srav3h, 4, 3, gs.snpt_col_study_title),
        (gs.compilation_srav3h, 4, 4, "avg_psi"),
        (gs.compilation_srav3h, 4, 5, "psi_1"),
        # gtexv2 compilation
        (gs.compilation_gtexv2, 2, 0, gs.snpt_col_rail_id),
        (gs.compilation_gtexv2, 2, 1, gs.snpt_col_run_acc),
        (gs.compilation_gtexv2, 2, 2, gs.snpt_col_study),
        (gs.compilation_gtexv2, 2, 3, "avg_psi"),
        (gs.compilation_gtexv2, 2, 4, "psi_1"),
        # three junctions
        (gs.compilation_gtexv2, 3, 0, gs.snpt_col_rail_id),
        (gs.compilation_gtexv2, 3, 1, gs.snpt_col_run_acc),
        (gs.compilation_gtexv2, 3, 2, gs.snpt_col_study),
        (gs.compilation_gtexv2, 3, 3, "avg_psi"),
        (gs.compilation_gtexv2, 3, 4, "psi_1"),
        # four junctions
        (gs.compilation_gtexv2, 4, 0, gs.snpt_col_rail_id),
        (gs.compilation_gtexv2, 4, 1, gs.snpt_col_run_acc),
        (gs.compilation_gtexv2, 4, 2, gs.snpt_col_study),
        (gs.compilation_gtexv2, 4, 3, "avg_psi"),
        (gs.compilation_gtexv2, 4, 4, "psi_1"),
        # tcga compilation
        (gs.compilation_tcgav2, 2, 0, gs.snpt_col_rail_id),
        (gs.compilation_tcgav2, 2, 1, gs.snpt_col_gdc_prim_site),
        (gs.compilation_tcgav2, 2, 2, gs.snpt_col_study),
        (gs.compilation_tcgav2, 2, 3, "avg_psi"),
        (gs.compilation_tcgav2, 2, 4, "psi_1"),
        # three junctions
        (gs.compilation_tcgav2, 3, 0, gs.snpt_col_rail_id),
        (gs.compilation_tcgav2, 3, 1, gs.snpt_col_gdc_prim_site),
        (gs.compilation_tcgav2, 3, 2, gs.snpt_col_study),
        (gs.compilation_tcgav2, 3, 3, "avg_psi"),
        (gs.compilation_tcgav2, 3, 4, "psi_1"),
        # four junctions
        (gs.compilation_tcgav2, 4, 0, gs.snpt_col_rail_id),
        (gs.compilation_tcgav2, 4, 1, gs.snpt_col_gdc_prim_site),
        (gs.compilation_tcgav2, 4, 2, gs.snpt_col_study),
        (gs.compilation_tcgav2, 4, 3, "avg_psi"),
        (gs.compilation_tcgav2, 4, 4, "psi_1"),
        # encode compilation
        (gs.compilation_encode, 2, 0, gs.snpt_col_rail_id),
        (gs.compilation_encode, 2, 1, gs.snpt_col_exp_acc),
        (gs.compilation_encode, 2, 2, gs.snpt_col_cell_line),
        (gs.compilation_encode, 2, 3, gs.snpt_col_exp_target),
        (gs.compilation_encode, 2, 4, "avg_psi"),
        (gs.compilation_encode, 2, 5, "psi_1"),
        # three junctions
        (gs.compilation_encode, 3, 0, gs.snpt_col_rail_id),
        (gs.compilation_encode, 3, 1, gs.snpt_col_exp_acc),
        (gs.compilation_encode, 3, 2, gs.snpt_col_cell_line),
        (gs.compilation_encode, 2, 3, gs.snpt_col_exp_target),
        (gs.compilation_encode, 2, 4, "avg_psi"),
        (gs.compilation_encode, 2, 5, "psi_1"),
        # four junctions
        (gs.compilation_encode, 4, 0, gs.snpt_col_rail_id),
        (gs.compilation_encode, 4, 1, gs.snpt_col_exp_acc),
        (gs.compilation_encode, 4, 2, gs.snpt_col_cell_line),
        (gs.compilation_encode, 2, 3, gs.snpt_col_exp_target),
        (gs.compilation_encode, 2, 4, "avg_psi"),
        (gs.compilation_encode, 2, 5, "psi_1"),
        # mouse compilation
        (gs.compilation_srav1m, 2, 0, gs.snpt_col_rail_id),
        (gs.compilation_srav1m, 2, 1, gs.snpt_col_external_id),
        (gs.compilation_srav1m, 2, 2, gs.snpt_col_study),
        (gs.compilation_srav1m, 2, 3, gs.snpt_col_study_title),
        (gs.compilation_srav1m, 2, 4, "avg_psi"),
        (gs.compilation_srav1m, 2, 5, "psi_1"),
        # three junctions same compilation
        (gs.compilation_srav1m, 3, 0, gs.snpt_col_rail_id),
        (gs.compilation_srav1m, 3, 1, gs.snpt_col_external_id),
        (gs.compilation_srav1m, 3, 2, gs.snpt_col_study),
        (gs.compilation_srav1m, 3, 3, gs.snpt_col_study_title),
        (gs.compilation_srav1m, 3, 4, "avg_psi"),
        (gs.compilation_srav1m, 3, 5, "psi_1"),
        # four junctions same compilation
        (gs.compilation_srav1m, 4, 0, gs.snpt_col_rail_id),
        (gs.compilation_srav1m, 4, 1, gs.snpt_col_external_id),
        (gs.compilation_srav1m, 4, 2, gs.snpt_col_study),
        (gs.compilation_srav1m, 4, 3, gs.snpt_col_study_title),
        (gs.compilation_srav1m, 4, 4, "avg_psi"),
        (gs.compilation_srav1m, 4, 5, "psi_1"),
    ],
)
def test_get_junction_query_column_def(compilation, junction_count, index, value):
    columns = column_defs.get_junction_query_column_def(compilation, junction_count)
    assert columns[index]["field"] == value


@pytest.mark.parametrize(
    "compilation, normalized,index,value",
    [
        (gs.compilation_srav3h, True, 0, gs.snpt_col_rail_id),
        (gs.compilation_srav3h, True, 1, gs.snpt_col_external_id),
        (gs.compilation_srav3h, True, 2, gs.snpt_col_study),
        (gs.compilation_srav3h, True, 3, gs.snpt_col_study_title),
        (gs.compilation_srav3h, True, 4, gs.table_geq_col_raw_count),
        (gs.compilation_srav3h, True, 5, "factor"),
        (gs.compilation_srav3h, True, 6, "normalized_count"),
        # not normalized
        (gs.compilation_srav3h, False, 0, gs.snpt_col_rail_id),
        (gs.compilation_srav3h, False, 1, gs.snpt_col_external_id),
        (gs.compilation_srav3h, False, 2, gs.snpt_col_study),
        (gs.compilation_srav3h, False, 3, gs.snpt_col_study_title),
        (gs.compilation_srav3h, False, 4, gs.table_geq_col_raw_count),
        (gs.compilation_srav3h, False, 5, gs.table_geq_col_log_2_raw),
        # gtexv2 compilation
        (gs.compilation_gtexv2, True, 0, gs.snpt_col_rail_id),
        (gs.compilation_gtexv2, True, 1, gs.snpt_col_run_acc),
        (gs.compilation_gtexv2, True, 2, gs.snpt_col_study),
        (gs.compilation_gtexv2, True, 3, gs.table_geq_col_raw_count),
        (gs.compilation_gtexv2, True, 4, "factor"),
        (gs.compilation_gtexv2, True, 5, "normalized_count"),
        # not normalized
        (gs.compilation_gtexv2, False, 0, gs.snpt_col_rail_id),
        (gs.compilation_gtexv2, False, 1, gs.snpt_col_run_acc),
        (gs.compilation_gtexv2, False, 2, gs.snpt_col_study),
        (gs.compilation_gtexv2, False, 3, gs.table_geq_col_raw_count),
        (gs.compilation_gtexv2, False, 4, gs.table_geq_col_log_2_raw),
        # tcgav2 compilation
        (gs.compilation_tcgav2, True, 0, gs.snpt_col_rail_id),
        (gs.compilation_tcgav2, True, 1, gs.snpt_col_gdc_prim_site),
        (gs.compilation_tcgav2, True, 2, gs.snpt_col_study),
        (gs.compilation_tcgav2, True, 3, gs.table_geq_col_raw_count),
        (gs.compilation_tcgav2, True, 4, "factor"),
        (gs.compilation_tcgav2, True, 5, "normalized_count"),
        # not normalized
        (gs.compilation_tcgav2, False, 0, gs.snpt_col_rail_id),
        (gs.compilation_tcgav2, False, 1, gs.snpt_col_gdc_prim_site),
        (gs.compilation_tcgav2, False, 2, gs.snpt_col_study),
        (gs.compilation_tcgav2, False, 3, gs.table_geq_col_raw_count),
        (gs.compilation_tcgav2, False, 4, gs.table_geq_col_log_2_raw),
        # encode compilation (should not have normalized values)
        (gs.compilation_encode, True, 0, gs.snpt_col_rail_id),
        (gs.compilation_encode, True, 1, gs.snpt_col_exp_acc),
        (gs.compilation_encode, True, 2, gs.snpt_col_cell_line),
        (gs.compilation_encode, True, 3, gs.snpt_col_exp_target),
        (gs.compilation_encode, True, 4, gs.table_geq_col_raw_count),
        (gs.compilation_encode, True, 5, "factor"),
        (gs.compilation_encode, True, 6, "normalized_count"),
        # not normalized
        (gs.compilation_encode, False, 0, gs.snpt_col_rail_id),
        (gs.compilation_encode, True, 1, gs.snpt_col_exp_acc),
        (gs.compilation_encode, True, 2, gs.snpt_col_cell_line),
        (gs.compilation_encode, True, 3, gs.snpt_col_exp_target),
        (gs.compilation_encode, False, 4, gs.table_geq_col_raw_count),
        (gs.compilation_encode, False, 5, gs.table_geq_col_log_2_raw),
        # mouse compilation
        (gs.compilation_srav1m, True, 0, gs.snpt_col_rail_id),
        (gs.compilation_srav1m, True, 1, gs.snpt_col_external_id),
        (gs.compilation_srav1m, True, 2, gs.snpt_col_study),
        (gs.compilation_srav1m, True, 3, gs.snpt_col_study_title),
        (gs.compilation_srav1m, True, 4, gs.table_geq_col_raw_count),
        (gs.compilation_srav1m, True, 5, "factor"),
        (gs.compilation_srav1m, True, 6, "normalized_count"),
        # not normalized
        (gs.compilation_srav1m, False, 0, gs.snpt_col_rail_id),
        (gs.compilation_srav1m, False, 1, gs.snpt_col_external_id),
        (gs.compilation_srav1m, False, 2, gs.snpt_col_study),
        (gs.compilation_srav1m, False, 3, gs.snpt_col_study_title),
        (gs.compilation_srav1m, False, 4, gs.table_geq_col_raw_count),
        (gs.compilation_srav1m, False, 5, gs.table_geq_col_log_2_raw),
    ],
)
def test_get_gene_expression_query_column_def(compilation, normalized, index, value):
    c = column_defs.get_gene_expression_query_column_def(compilation, normalized)
    assert c[index]["field"] == value


@pytest.mark.parametrize(
    "junction_count, column, r",
    [
        (1, gs.table_jiq_col_total, gs.const_filter_total),
        (1, gs.table_jiq_col_psi, gs.const_filter_psi),
        (2, gs.table_jiq_col_avg_psi, gs.const_filter_psi),
        (2, f"{gs.table_jiq_col_total}_1", gs.const_filter_total),
        (2, f"{gs.table_jiq_col_total}_2", gs.const_filter_total),
        (3, gs.table_jiq_col_avg_psi, gs.const_filter_psi),
        (3, f"{gs.table_jiq_col_total}_1", gs.const_filter_total),
        (3, f"{gs.table_jiq_col_total}_2", gs.const_filter_total),
        (3, f"{gs.table_jiq_col_total}_3", gs.const_filter_total),
        (4, gs.table_jiq_col_avg_psi, gs.const_filter_psi),
        (4, f"{gs.table_jiq_col_total}_1", gs.const_filter_total),
        (4, f"{gs.table_jiq_col_total}_2", gs.const_filter_total),
        (4, f"{gs.table_jiq_col_total}_3", gs.const_filter_total),
        (4, f"{gs.table_jiq_col_total}_4", gs.const_filter_total),
        (5, gs.table_jiq_col_avg_psi, gs.const_filter_psi),
        (5, f"{gs.table_jiq_col_total}_1", gs.const_filter_total),
        (5, f"{gs.table_jiq_col_total}_2", gs.const_filter_total),
        (5, f"{gs.table_jiq_col_total}_3", gs.const_filter_total),
        (5, f"{gs.table_jiq_col_total}_4", gs.const_filter_total),
        (5, f"{gs.table_jiq_col_total}_5", gs.const_filter_total),
    ],
)
def test_get_jiq_table_filter_model(junction_count, column, r):
    column_def = column_defs.get_jiq_table_filter_model(junction_count)[column]["filter"]
    assert column_def == r


@pytest.mark.parametrize(
    "junction_count, dictionary_count",
    [
        (1, 2),
        (2, 3),
        (3, 4),
        (4, 5),
        (5, 6),
    ],
)
def test_get_jiq_table_filter_model_count_of_items(junction_count, dictionary_count):
    assert len(column_defs.get_jiq_table_filter_model(junction_count)) == dictionary_count


def test_get_geq_table_filter_model_norm():
    assert column_defs.get_geq_table_filter_model(True)[gs.table_geq_col_factor]["filter"] == 0


def test_get_geq_table_filter_model():
    assert column_defs.get_geq_table_filter_model(False) == {}


@pytest.mark.parametrize(
    "filter_value",
    [
        gs.const_filter_total,
        gs.const_filter_psi,
    ],
)
def test_make_dash_ag_grid_greater_than_or_equal_filter(filter_value):
    assert column_defs.make_dash_ag_grid_greater_than_or_equal_filter(filter_value)["filter"] == filter_value
    assert column_defs.make_dash_ag_grid_greater_than_or_equal_filter(filter_value)["type"] == "greaterThanOrEqual"
    assert column_defs.make_dash_ag_grid_greater_than_or_equal_filter(filter_value)["filterType"] == "number"


def test_get_geq_table_filter_model_2():
    assert column_defs.get_geq_table_filter_model(False) == {}


@pytest.mark.parametrize(
    "index, name",
    [
        (0, gs.table_jiq_col_inc),
        (1, gs.table_jiq_col_exc),
        (2, gs.table_jiq_col_total),
    ],
)
def test_get_col_jiq(index, name):
    assert column_defs.get_col_jiq_calculations()[index]["field"] == name
