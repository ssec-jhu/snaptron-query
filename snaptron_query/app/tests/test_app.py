import pytest

from snaptron_query.app import global_strings as gs, snaptron_client as sc, exceptions
from snaptron_query.app.query_junction_inclusion import JunctionType


def test_jiq_rail_id_size(junction):
    rail_dict = junction.get_rail_id_dict()
    assert len(rail_dict) == 160578


@pytest.mark.parametrize('rail_id,count', [(992538, 100), (996729, 96)])
def test_jiq_lookup_rail_id_inclusion(junction, rail_id, count):
    rail_dict = junction.get_rail_id_dict()
    v_list = rail_dict.get(rail_id)
    assert len(v_list) == 1
    assert (v_list[0])['count'] == count
    assert (v_list[0])['type'] == JunctionType.EXCLUSION


@pytest.mark.parametrize('rail_id,exc_count,inc_count', [(1001806, 34, 4), (100107, 15, 1), (100073, 7, 2),
                                                         (100051, 35, 1), (100015, 14, 1), (100005, 31, 1),
                                                         (1975952, 86, 1)])
def test_jiq_rail_id_in_both_junctions(junction, rail_id, exc_count, inc_count):
    rail_dict = junction.get_rail_id_dict()
    v_list = rail_dict.get(rail_id)
    assert (v_list[0])['count'] == exc_count
    assert (v_list[0])['type'] == JunctionType.EXCLUSION
    assert (v_list[1])['count'] == inc_count
    assert (v_list[1])['type'] == JunctionType.INCLUSION


def test_jiq_results_size_cols(junction):
    assert junction.get_results().shape[1] == 11


@pytest.mark.parametrize('rail_id,external_id,inc,exc,psi', [(1000010, 'SRR3743424', 0, 11, 0.0),
                                                             (2171668, 'SRR5714918', 35, 0, 100.0),
                                                             (988956, 'SRR5461171', 66, 102, 39.29),
                                                             (1127039, 'SRR5398327', 4, 12, 25.0),
                                                             (499887, 'SRR3469415', 9, 23, 28.12),
                                                             (988942, 'SRR5461170', 65, 101, 39.16),
                                                             (1641727, 'SRR8083867', 17, 55, 23.61),
                                                             (1641757, 'SRR8083868', 12, 45, 21.05),
                                                             (2109561, 'SRR6873183', 12, 34, 26.09)])
def test_jiq_results(junction, rail_id, external_id, inc, exc, psi):
    s = junction.get_results().loc[rail_id]
    assert s[gs.snaptron_col_external_id] == external_id
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


@pytest.mark.parametrize('coordinates', ["chr50:5000-6000", 'chr:5000-6000', 'some_random_string', 'chrXY:4000-5000'])
def test_verify_bad_coordinates_with_errors(coordinates):
    with pytest.raises(exceptions.BadCoordinates):
        sc.verify_coordinates(coordinates)


def test_split_and_verify_mismatch_chromosomes():
    with pytest.raises(exceptions.BadCoordinates):
        sc.jiq_verify_coordinate_pairs('chr19:5000-6000', 'chr29:4000-5000')


@pytest.mark.parametrize('rail_id', [2171668, 988956, 1127039, 499887, 988942, 1641727, 1641757, 2109561])
def test_jiq_psi_results_vs_shinyapp_website(junction, ground_truth_df, rail_id):
    our_results = junction.get_results().loc[rail_id]
    ground_truth = ground_truth_df.loc[rail_id]
    assert our_results[gs.snaptron_col_external_id] == ground_truth[gs.snaptron_col_external_id]
    assert our_results[gs.table_jiq_col_psi] == ground_truth[gs.table_jiq_col_psi]
