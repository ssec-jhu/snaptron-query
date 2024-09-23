import pytest

from snaptron_query.app import global_strings as gs, exceptions
from snaptron_query.app.tests.conftest import MultiJunctionQuery


def run_multijq_asserts(our_results, external_id, inc_1, exc_1, psi_1, inc_2, exc_2, psi_2):
    assert our_results[gs.snpt_col_external_id] == external_id
    assert our_results[f"{gs.table_jiq_col_inc}_1"] == inc_1
    assert our_results[f"{gs.table_jiq_col_exc}_1"] == exc_1
    assert our_results[f"{gs.table_jiq_col_psi}_1"] == psi_1

    assert our_results[f"{gs.table_jiq_col_inc}_2"] == inc_2
    assert our_results[f"{gs.table_jiq_col_exc}_2"] == exc_2
    assert our_results[f"{gs.table_jiq_col_psi}_2"] == psi_2


def run_multijq_psi_asserts(our_results, external_id, psi_1, psi_2):
    assert our_results[gs.snpt_col_external_id] == external_id
    assert our_results[f"{gs.table_jiq_col_psi}_1"] == psi_1
    assert our_results[f"{gs.table_jiq_col_psi}_2"] == psi_2


@pytest.mark.parametrize(
    "rail_id,external_id,inc_1,exc_1,psi_1,inc_2,exc_2,psi_2",
    [
        (1000010, "SRR3743424", 0, 11, 0, 0, 11, 0),
        (2171668, "SRR5714918", 35, 0, 100.0, 0, 0, 0),
        (988956, "SRR5461171", 66, 102, 39.29, 81, 102, 44.26),
        (1127039, "SRR5398327", 4, 12, 25.0, 0, 12, 0),
        (499887, "SRR3469415", 9, 23, 28.12, 1, 23, 4.17),
        (988942, "SRR5461170", 65, 101, 39.16, 77, 101, 43.26),
        (1641727, "SRR8083867", 17, 55, 23.61, 15, 55, 21.43),
        (1641757, "SRR8083868", 12, 45, 21.05, 10, 45, 18.18),
        (2109561, "SRR6873183", 12, 34, 26.09, 0, 34, 0),
    ],
)
def test_mjq(multi_junction_srav3h, rail_id, external_id, inc_1, exc_1, psi_1, inc_2, exc_2, psi_2):
    our_results = multi_junction_srav3h.get_results().loc[rail_id]
    run_multijq_asserts(our_results, external_id, inc_1, exc_1, psi_1, inc_2, exc_2, psi_2)


@pytest.mark.parametrize(
    "rail_id,external_id,inc_1,exc_1,psi_1,inc_2,exc_2,psi_2",
    [
        (1000010, "SRR3743424", 0, 11, 0, 0, 11, 0),
        (2171668, "SRR5714918", 35, 0, 100.0, 0, 0, 0),
        (988956, "SRR5461171", 66, 102, 39.29, 81, 102, 44.26),
        (1127039, "SRR5398327", 4, 12, 25.0, 0, 12, 0),
        (499887, "SRR3469415", 9, 23, 28.12, 1, 23, 4.17),
        (988942, "SRR5461170", 65, 101, 39.16, 77, 101, 43.26),
        (1641727, "SRR8083867", 17, 55, 23.61, 15, 55, 21.43),
        (1641757, "SRR8083868", 12, 45, 21.05, 10, 45, 18.18),
        (2109561, "SRR6873183", 12, 34, 26.09, 0, 34, 0),
    ],
)
def test_mjq_raw_results(
    multi_junction_srav3h_raw_results, rail_id, external_id, inc_1, exc_1, psi_1, inc_2, exc_2, psi_2
):
    # this test has a different return type from the other multi junction queries
    # this tests the default dictionary that is created
    our_results = multi_junction_srav3h_raw_results.get_results()[rail_id]
    assert our_results["meta"][gs.snpt_col_external_id] == external_id
    assert our_results["junctions"][0]["inc"] == inc_1
    assert our_results["junctions"][0]["exc"] == exc_1
    assert our_results["junctions"][0]["psi"] == psi_1
    assert our_results["junctions"][1]["inc"] == inc_2
    assert our_results["junctions"][1]["exc"] == exc_2
    assert our_results["junctions"][1]["psi"] == psi_2


@pytest.mark.parametrize(
    "rail_id,external_id,inc_1,exc_1,psi_1,inc_2,exc_2,psi_2",
    [
        (1000010, "SRR3743424", 0, 11, 0, 0, 11, 0),
        (2171668, "SRR5714918", 0, 0, 0, 35, 0, 100.0),
        (988956, "SRR5461171", 81, 102, 44.26, 66, 102, 39.29),
        (1127039, "SRR5398327", 0, 12, 0, 4, 12, 25.0),
        (499887, "SRR3469415", 1, 23, 4.17, 9, 23, 28.12),
        (988942, "SRR5461170", 77, 101, 43.26, 65, 101, 39.16),
        (1641727, "SRR8083867", 15, 55, 21.43, 17, 55, 23.61),
        (1641757, "SRR8083868", 10, 45, 18.18, 12, 45, 21.05),
        (2109561, "SRR6873183", 0, 34, 0, 12, 34, 26.09),
    ],
)
def test_mjq_2(multi_junction_srav3h_2, rail_id, external_id, inc_1, exc_1, psi_1, inc_2, exc_2, psi_2):
    our_results = multi_junction_srav3h_2.get_results().loc[rail_id]
    run_multijq_asserts(our_results, external_id, inc_1, exc_1, psi_1, inc_2, exc_2, psi_2)


@pytest.mark.parametrize(
    "rail_id,external_id,psi_1,psi_2",
    [
        (2171668, "SRR5714918", 0, 0),
        (988956, "SRR5461171", 74.39, 0),
        (988942, "SRR5461170", 72.22, 0),
        (1641727, "SRR8083867", 3.33, 0),
        (1641757, "SRR8083868", 17.65, 0),
        (2109561, "SRR6873183", 0, 0),
        (1127039, "SRR5398327", 0, 0),
        (499887, "SRR3469415", 3.12, 0),
        (1000010, "SRR3743424", 0, 0),
        (2566685, "SRR8571950", 39.34, 0),
        (2566230, "SRR8571942", 39.29, 0),
        (2566161, "SRR8571940", 28.87, 0),
        (988777, "SRR5461166", 23.57, 0),
        (988795, "SRR5461167", 37.63, 0),
        (1641757, "SRR8083868", 17.65, 0),
        (491716, "SRR10045018", 16.67, 0),
    ],
)
def test_mjq_3(multi_junction_srav3h_3, rail_id, external_id, psi_1, psi_2):
    our_results = multi_junction_srav3h_3.get_results().loc[rail_id]
    run_multijq_psi_asserts(our_results, external_id, psi_1, psi_2)


@pytest.mark.parametrize(
    "rail_id,external_id,psi_1,psi_2",
    [
        (668214, "SRR10007646", 27.27, 0),
        (669863, "SRR2119714", 36.84, 27.27),
        (669879, "SRR2119716", 37.38, 27.17),
        (669871, "SRR2119715", 37.14, 18.52),
        (2885781, "SRR5944044", 22.22, 0),
        (2885847, "SRR5944046", 25, 0),
        (213136, "DRR042048", 20, 0),
        (957629, "SRR10044397", 26.09, 0),
        (3072016, "SRR1971700", 100, 0),
    ],
)
def test_mjq_4(multi_junction_srav1m_1, rail_id, external_id, psi_1, psi_2):
    our_results = multi_junction_srav1m_1.get_results().loc[rail_id]
    run_multijq_psi_asserts(our_results, external_id, psi_1, psi_2)


def test_multijq_empty_inclusion_error(multi_junction_srav3h_one_empty_inclusion, meta_data_dict_srav3h):
    with pytest.raises(Exception) as exc_info:
        MultiJunctionQuery(
            junction_list=multi_junction_srav3h_one_empty_inclusion[0],
            meta_data_dict=meta_data_dict_srav3h,
            df_from_snaptron_map=multi_junction_srav3h_one_empty_inclusion[1],
        )
    assert exc_info.value.index == 3
    assert exc_info.type == exceptions.EmptyIncJunction
