import pandas as pd
import pytest

from snaptron_query.app import global_strings as gs, snaptron_client as sc, exceptions
from snaptron_query.app.query_junction_inclusion import JunctionType
from snaptron_query.app.tests.conftest import JunctionQuery, path_sample_junction_data


def test_jiq_rail_id_size(junction_srav3h):
    rail_dict = junction_srav3h.get_rail_id_dict()
    assert len(rail_dict) == 160578


@pytest.mark.parametrize('rail_id, count', [(992538, 100), (996729, 96)])
def test_jiq_lookup_rail_id_inclusion(junction_srav3h, rail_id, count):
    rail_dict = junction_srav3h.get_rail_id_dict()
    v_list = rail_dict.get(rail_id)
    assert len(v_list) == 1
    # assert (v_list[0])['count'] == count
    # assert (v_list[0])['type'] == JunctionType.EXCLUSION


@pytest.mark.parametrize('rail_id,count', [(10044963, 39), (1198331, 86), (301619, 9), (1239258, 13), (1124564, 49)])
def test_jiq_lookup_rail_id_inclusion_gtexv2(junction_gtexv2, rail_id, count):
    rail_dict = junction_gtexv2.get_rail_id_dict()
    v_list = rail_dict.get(rail_id)
    assert len(v_list) == 1
    assert (v_list[0])['count'] == count
    assert (v_list[0])['type'] == JunctionType.EXCLUSION


@pytest.mark.parametrize('rail_id,exc_count,inc_count', [(1001806, 34, 4), (100107, 15, 1), (100073, 7, 2),
                                                         (100051, 35, 1), (100015, 14, 1), (100005, 31, 1),
                                                         (1975952, 86, 1)])
def test_jiq_rail_id_in_both_junctions(junction_srav3h, rail_id, exc_count, inc_count):
    rail_dict = junction_srav3h.get_rail_id_dict()
    v_list = rail_dict.get(rail_id)
    assert (v_list[0])['count'] == exc_count
    assert (v_list[0])['type'] == JunctionType.EXCLUSION
    assert (v_list[1])['count'] == inc_count
    assert (v_list[1])['type'] == JunctionType.INCLUSION


@pytest.mark.parametrize('rail_id,exc_count,inc_count', [(10044980, 67, 1), (10045247, 43, 1), (1165564, 48, 1),
                                                         (1140931, 67, 1), (1124546, 39, 2), (2167295, 82, 3),
                                                         (4301568, 95, 2)])
def test_jiq_rail_id_in_both_junctions_gtexv2(junction_gtexv2, rail_id, exc_count, inc_count):
    rail_dict = junction_gtexv2.get_rail_id_dict()
    v_list = rail_dict.get(rail_id)
    assert (v_list[0])['count'] == exc_count
    assert (v_list[0])['type'] == JunctionType.EXCLUSION
    assert (v_list[1])['count'] == inc_count
    assert (v_list[1])['type'] == JunctionType.INCLUSION


def test_jiq_results_size_cols(junction_srav3h):
    assert junction_srav3h.get_results().shape[1] == 12


@pytest.mark.parametrize('rail_id,external_id,inc,exc,psi', [(1000010, 'SRR3743424', 0, 11, 0.0),
                                                             (2171668, 'SRR5714918', 35, 0, 100.0),
                                                             (988956, 'SRR5461171', 66, 102, 39.29),
                                                             (1127039, 'SRR5398327', 4, 12, 25.0),
                                                             (499887, 'SRR3469415', 9, 23, 28.12),
                                                             (988942, 'SRR5461170', 65, 101, 39.16),
                                                             (1641727, 'SRR8083867', 17, 55, 23.61),
                                                             (1641757, 'SRR8083868', 12, 45, 21.05),
                                                             (2109561, 'SRR6873183', 12, 34, 26.09)])
def test_jiq_results_srav3h(junction_srav3h, rail_id, external_id, inc, exc, psi):
    s = junction_srav3h.get_results().loc[rail_id]
    assert s[gs.snpt_col_external_id] == external_id
    assert s[gs.table_jiq_col_inc] == inc
    assert s[gs.table_jiq_col_exc] == exc
    assert s[gs.table_jiq_col_psi] == psi


@pytest.mark.parametrize('rail_id,study,inc,exc,psi', [(2216416, 'BLOOD', 2, 27, 6.9),
                                                       (4399966, 'LUNG', 2, 31, 6.06),
                                                       (4301657, 'ADIPOSE_TISSUE', 2, 20, 9.09),
                                                       (2199960, 'THYROID', 2, 33, 5.71),
                                                       (4236071, 'THYROID', 2, 38, 5.00),
                                                       (4530990, 'THYROID', 2, 22, 8.33),
                                                       (9914021, 'THYROID', 2, 30, 6.25),
                                                       (2462190, 'HEART', 1, 19, 5.00),
                                                       (4498305, 'MUSCLE', 3, 39, 7.14),
                                                       (9783109, 'MUSCLE', 2, 17, 10.53)])
def test_jiq_results_gtexv2(junction_gtexv2, rail_id, study, inc, exc, psi):
    s = junction_gtexv2.get_results().loc[rail_id]
    assert s[gs.snpt_col_study] == study
    assert s[gs.table_jiq_col_inc] == inc
    assert s[gs.table_jiq_col_exc] == exc
    assert s[gs.table_jiq_col_psi] == psi


@pytest.mark.parametrize('rail_id,study,inc,exc,psi', [(858212, 'UCEC', 2, 18, 10.0),
                                                       (220457, 'CESC', 2, 21, 8.7),
                                                       (886326, 'STAD', 2, 21, 8.7),
                                                       (219485, 'STAD', 2, 26, 7.14),
                                                       (54627, 'BLCA', 1, 14, 6.67),
                                                       (870564, 'HNSC', 1, 14, 6.67),
                                                       (869858, 'UCEC', 1, 14, 6.67),
                                                       (234844, 'LIHC', 1, 15, 6.25),
                                                       (472121, 'PRAD', 1, 19, 5.0)])
def test_jiq_results_tcgav2(junction_tcgav2, rail_id, study, inc, exc, psi):
    s = junction_tcgav2.get_results().loc[rail_id]
    assert s[gs.snpt_col_study] == study
    assert s[gs.table_jiq_col_inc] == inc
    assert s[gs.table_jiq_col_exc] == exc
    assert s[gs.table_jiq_col_psi] == psi


@pytest.mark.parametrize('rail_id,study,inc,exc,psi', [(3072016, 'SRP057123', 21, 0, 100.0),
                                                       (669879, 'SRP061340', 40, 67, 37.38),
                                                       (669871, 'SRP061340', 13, 22, 37.14),
                                                       (669863, 'SRP061340', 14, 24, 36.84),
                                                       (3466847, 'SRP170686', 10, 23, 30.3),
                                                       (668214, 'SRP218930', 6, 16, 27.27),
                                                       (957629, 'SRP219859', 6, 17, 26.09),
                                                       (2885847, 'SRP124512', 10, 30, 25.0),
                                                       (2885781, 'SRP124512', 6, 21, 22.22)])
def test_jiq_results_srav1m(junction_srav1m, rail_id, study, inc, exc, psi):
    s = junction_srav1m.get_results().loc[rail_id]
    assert s[gs.snpt_col_study] == study
    assert s[gs.table_jiq_col_inc] == inc
    assert s[gs.table_jiq_col_exc] == exc
    assert s[gs.table_jiq_col_psi] == psi


@pytest.mark.parametrize('pair_a,pair_b,chr_a,chr_b,start_a,end_a,start_b,end_b',
                         [('chr3:5555-6666', 'chr3:4000-5000', 'chr3', 'chr3', 5555, 6666, 4000, 5000),
                          ('chr19:5000-6000', 'chr19:4000-5000', 'chr19', 'chr19', 5000, 6000, 4000, 5000)]
                         )
def test_jiq_verify_coordinates(pair_a, pair_b, chr_a, chr_b, start_a, end_a, start_b, end_b):
    (A_chr, A_start, A_end), (B_chr, B_start, B_end) = sc.jiq_verify_coordinate_pairs(pair_a, pair_b)
    assert A_chr == chr_a
    assert B_chr == chr_b
    # make sure they are cast correctly
    assert A_start == start_a
    assert A_end == end_a
    assert B_start == start_b
    assert B_end == end_b


@pytest.mark.parametrize('pair_a,pair_b', [('chr19:5000-6000', 'chr29:4000-5000')])
def test_jiq_verify_coordinates_with_errors(pair_a, pair_b):
    with pytest.raises(exceptions.BadCoordinates):
        sc.jiq_verify_coordinate_pairs(pair_a, pair_b)


def test_split_and_verify_mismatch_chromosomes():
    with pytest.raises(exceptions.BadCoordinates):
        sc.jiq_verify_coordinate_pairs('chr19:5000-6000', 'chr29:4000-5000')


@pytest.mark.parametrize('rail_id', [2171668, 988956, 1127039, 499887, 988942, 1641727, 1641757, 2109561])
def test_jiq_psi_results_vs_shinyapp_website(junction_srav3h, ground_truth_df, rail_id):
    our_results = junction_srav3h.get_results().loc[rail_id]
    ground_truth = ground_truth_df.loc[rail_id]
    assert our_results[gs.snpt_col_external_id] == ground_truth[gs.snpt_col_external_id]
    assert our_results[gs.table_jiq_col_psi] == ground_truth[gs.table_jiq_col_psi]


def test_jiq_empty_junctions():
    with pytest.raises(exceptions.EmptyJunction):
        df_sample_junctions_from_snaptron = pd.read_csv(path_sample_junction_data, sep='\t')
        JunctionQuery(4491836, 4493702, 0, 0, {}, df_sample_junctions_from_snaptron)