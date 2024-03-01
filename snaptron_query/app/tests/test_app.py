from snaptron_query.app import global_strings as gs
from snaptron_query.app.query_junction_inclusion import JunctionType

def test_jiq_rail_id_size(junction):
    rail_dict = junction.get_rail_id_dict()
    assert len(rail_dict) == 160578


def test_jiq_lookup_rail_id_inclusion(junction):
    test_rail = [992538, 996729]
    test_count = [100, 96]
    rail_dict = junction.get_rail_id_dict()
    for i, r in enumerate(test_rail):
        v_list = rail_dict.get(r)
        assert len(v_list) == 1
        assert (v_list[0])['count'] == test_count[i]
        assert (v_list[0])['type'] == JunctionType.EXCLUSION


def test_jiq_rail_id_in_both_junctions_1(junction):
    rail_dict = junction.get_rail_id_dict()
    v_list = rail_dict.get(1975952)
    # has to have both junctions count
    assert len(v_list) == 2
    # check exclusion values
    assert (v_list[0])['count'] == 86
    assert (v_list[0])['type'] == JunctionType.EXCLUSION
    # check inclusion values
    assert (v_list[1])['count'] == 1
    assert (v_list[1])['type'] == JunctionType.INCLUSION


def test_jiq_rail_id_in_both_junctions_2(junction):
    rail_dict = junction.get_rail_id_dict()
    v_list = rail_dict.get(100005)
    # has to have both junctions count
    assert len(v_list) == 2
    # check exclusion values
    assert (v_list[0])['count'] == 31
    assert (v_list[0])['type'] == JunctionType.EXCLUSION
    # check inclusion values
    assert (v_list[1])['count'] == 1
    assert (v_list[1])['type'] == JunctionType.INCLUSION


def test_jiq_rail_id_in_both_junctions_3(junction):
    rail_dict = junction.get_rail_id_dict()
    v_list = rail_dict.get(100015)
    # has to have both junctions count
    assert len(v_list) == 2
    # check exclusion values
    assert (v_list[0])['count'] == 14
    assert (v_list[0])['type'] == JunctionType.EXCLUSION
    # check inclusion values
    assert (v_list[1])['count'] == 1
    assert (v_list[1])['type'] == JunctionType.INCLUSION


def test_jiq_rail_id_in_both_junctions_4(junction):
    rail_dict = junction.get_rail_id_dict()
    v_list = rail_dict.get(100051)
    # has to have both junctions count
    assert len(v_list) == 2
    # check exclusion values
    assert (v_list[0])['count'] == 35
    assert (v_list[0])['type'] == JunctionType.EXCLUSION
    # check inclusion values
    assert (v_list[1])['count'] == 1
    assert (v_list[1])['type'] == JunctionType.INCLUSION


def test_jiq_rail_id_in_both_junctions_5(junction):
    rail_dict = junction.get_rail_id_dict()
    v_list = rail_dict.get(100073)
    # has to have both junctions count
    assert len(v_list) == 2
    # check exclusion values
    assert (v_list[0])['count'] == 7
    assert (v_list[0])['type'] == JunctionType.EXCLUSION
    # check inclusion values
    assert (v_list[1])['count'] == 2
    assert (v_list[1])['type'] == JunctionType.INCLUSION


def test_jiq_rail_id_in_both_junctions_6(junction):
    rail_dict = junction.get_rail_id_dict()
    v_list = rail_dict.get(100107)
    # has to have both junctions count
    assert len(v_list) == 2
    # check exclusion values
    assert (v_list[0])['count'] == 15
    assert (v_list[0])['type'] == JunctionType.EXCLUSION
    # check inclusion values
    assert (v_list[1])['count'] == 1
    assert (v_list[1])['type'] == JunctionType.INCLUSION


def test_jiq_rail_id_in_both_junctions_7(junction):
    rail_dict = junction.get_rail_id_dict()
    v_list = rail_dict.get(1001806)
    # has to have both junctions count
    assert len(v_list) == 2
    # check exclusion values
    assert (v_list[0])['count'] == 34
    assert (v_list[0])['type'] == JunctionType.EXCLUSION
    # check inclusion values
    assert (v_list[1])['count'] == 4
    assert (v_list[1])['type'] == JunctionType.INCLUSION


# turn these two tests on when testing with full data locally
# def test_jiq_results_size_data_count():
#     assert(df_jiq_results.shape[0]== 160576)
#     assert(df_jiq_results.shape[1] == 11)

def test_jiq_results_size_cols(junction):
    assert junction.get_results().shape[1] == 11


def test_jiq_results_1(junction):
    s = junction.get_results().loc[1000010]
    assert s[gs.snaptron_col_external_id] == 'SRR3743424'
    assert s['inc'] == 0
    assert s['exc'] == 11
    assert s['psi'] == 0.0


def test_jiq_results_2(junction):
    s = junction.get_results().loc[2171668]
    assert s[gs.snaptron_col_external_id] == 'SRR5714918'
    assert s['inc'] == 35
    assert s['exc'] == 0
    assert s['psi'] == 100.0


def test_jiq_results_3(junction):
    s = junction.get_results().loc[988956]
    assert s[gs.snaptron_col_external_id] == 'SRR5461171'
    assert s['inc'] == 66
    assert s['exc'] == 102
    assert s['psi'] == 39.29


def test_jiq_results_4(junction):
    s = junction.get_results().loc[1127039]
    assert s[gs.snaptron_col_external_id] == 'SRR5398327'
    assert s['inc'] == 4
    assert s['exc'] == 12
    assert s['psi'] == 25.0


def test_jiq_results_5(junction):
    s = junction.get_results().loc[499887]
    assert s[gs.snaptron_col_external_id] == 'SRR3469415'
    assert s['inc'] == 9
    assert s['exc'] == 23
    assert s['psi'] == 28.12


def test_jiq_results_6(junction):
    s = junction.get_results().loc[988942]
    assert s[gs.snaptron_col_external_id] == 'SRR5461170'
    assert s['inc'] == 65
    assert s['exc'] == 101
    assert s['psi'] == 39.16


def test_jiq_results_7(junction):
    s = junction.get_results().loc[1641727]
    assert s[gs.snaptron_col_external_id] == 'SRR8083867'
    assert s['inc'] == 17
    assert s['exc'] == 55
    assert s['psi'] == 23.61


def test_jiq_results_8(junction):
    s = junction.get_results().loc[1641757]
    assert s[gs.snaptron_col_external_id] == 'SRR8083868'
    assert s['inc'] == 12
    assert s['exc'] == 45
    assert s['psi'] == 21.05


def test_jiq_results_9(junction):
    s = junction.get_results().loc[2109561]
    assert s[gs.snaptron_col_external_id] == 'SRR6873183'
    assert s['inc'] == 12
    assert s['exc'] == 34
    assert s['psi'] == 26.09
