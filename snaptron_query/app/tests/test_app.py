import pandas as pd

from snaptron_query.app import query_junction_inclusion as jiq

from snaptron_query.app import global_strings

df_srav3h_meta_data = pd.read_csv('test_samples_SRAv3h.tsv', sep='\t',
                                  usecols=global_strings.srav3h_meta_data_required_list).set_index(
    global_strings.snaptron_col_rail_id)
df_from_snaptron = pd.read_csv('test_srav3h_chr19_4491836_4493702.tsv', sep='\t')

exclusion_start = 4491836
exclusion_end = 4493702
inclusion_start = 4491836
inclusion_end = 4492014
# find the exclusion and inclusion junction rows
query_mgr = jiq.JunctionInclusionQueryManager(exclusion_start, exclusion_end, inclusion_start, inclusion_end)
results_df = query_mgr.run_junction_inclusion_query(df_from_snaptron, df_srav3h_meta_data)


def test_jiq_find_junction_1():
    j1 = query_mgr._find_junction(df_from_snaptron, exclusion_start, exclusion_end)
    assert (j1.shape[0] == 1)


def test_jiq_find_junction_2():
    j2 = query_mgr._find_junction(df_from_snaptron, inclusion_start, inclusion_end)
    assert (j2.shape[0] == 1)


def test_jiq_find_junction_3():
    j3 = query_mgr._find_junction(df_from_snaptron, 3866073, 4530904)
    assert (j3.shape[0] == 1)


def test_jiq_find_junction_4():
    # test for a junction not in the results
    j4 = query_mgr._find_junction(df_from_snaptron, 3866073, 4530903)
    assert (j4.shape[0] == 0)  # does not exist


def test_jiq_rail_id_size():
    rail_dict = query_mgr.get_rail_id_dictionary()
    assert (len(rail_dict) == 160578)


def test_jiq_lookup_rail_id_1():
    rail_dict = query_mgr.get_rail_id_dictionary()
    v_list = rail_dict.get(992538)
    assert (len(v_list) == 1)
    assert ((v_list[0])['count'] == 100)
    assert ((v_list[0])['inc'] == 'False')


def test_jiq_lookup_rail_id_2():
    rail_dict = query_mgr.get_rail_id_dictionary()
    v_list = rail_dict.get(996729)
    assert (len(v_list) == 1)
    assert ((v_list[0])['count'] == 96)
    assert ((v_list[0])['inc'] == 'False')


def test_jiq_rail_id_in_both_junctions_1():
    rail_dict = query_mgr.get_rail_id_dictionary()
    v_list = rail_dict.get(1975952)
    # has to have both junctions count
    assert (len(v_list) == 2)
    # check exclusion values
    assert ((v_list[0])['count'] == 86)
    assert((v_list[0])['inc'] == 'False')
    # check inclusion values
    assert ((v_list[1])['count'] == 1)
    assert ((v_list[1])['inc'] == 'True')


def test_jiq_rail_id_in_both_junctions_2():
    rail_dict = query_mgr.get_rail_id_dictionary()
    v_list = rail_dict.get(100005)
    # has to have both junctions count
    assert (len(v_list) == 2)
    # check exclusion values
    assert ((v_list[0])['count'] == 31)
    assert ((v_list[0])['inc'] == 'False')
    # check inclusion values
    assert ((v_list[1])['count'] == 1)
    assert ((v_list[1])['inc'] == 'True')


def test_jiq_rail_id_in_both_junctions_3():
    rail_dict = query_mgr.get_rail_id_dictionary()
    v_list = rail_dict.get(100015)
    # has to have both junctions count
    assert (len(v_list) == 2)
    # check exclusion values
    assert ((v_list[0])['count'] == 14)
    assert ((v_list[0])['inc'] == 'False')
    # check inclusion values
    assert ((v_list[1])['count'] == 1)
    assert ((v_list[1])['inc'] == 'True')


def test_jiq_rail_id_in_both_junctions_4():
    rail_dict = query_mgr.get_rail_id_dictionary()
    v_list = rail_dict.get(100051)
    # has to have both junctions count
    assert (len(v_list) == 2)
    # check exclusion values
    assert ((v_list[0])['count'] == 7)
    assert ((v_list[0])['inc'] == 'False')
    # check inclusion values
    assert ((v_list[1])['count'] == 2)
    assert ((v_list[1])['inc'] == 'True')


def test_jiq_rail_id_in_both_junctions_5():
    rail_dict = query_mgr.get_rail_id_dictionary()
    v_list = rail_dict.get(100073)
    # has to have both junctions count
    assert (len(v_list) == 2)
    # check exclusion values
    assert ((v_list[0])['count'] == 7)
    assert ((v_list[0])['inc'] == 'False')
    # check inclusion values
    assert ((v_list[1])['count'] == 2)
    assert ((v_list[1])['inc'] == 'True')


def test_jiq_rail_id_in_both_junctions_6():
    rail_dict = query_mgr.get_rail_id_dictionary()
    v_list = rail_dict.get(100107)
    # has to have both junctions count
    assert (len(v_list) == 2)
    # check exclusion values
    assert ((v_list[0])['count'] == 15)
    assert ((v_list[0])['inc'] == 'False')
    # check inclusion values
    assert ((v_list[1])['count'] == 1)
    assert ((v_list[1])['inc'] == 'True')


def test_jiq_rail_id_in_both_junctions_7():
    rail_dict = query_mgr.get_rail_id_dictionary()
    v_list = rail_dict.get(1001806)
    # has to have both junctions count
    assert (len(v_list) == 2)
    # check exclusion values
    assert ((v_list[0])['count'] == 34)
    assert ((v_list[0])['inc'] == 'False')
    # check inclusion values
    assert ((v_list[1])['count'] == 4)
    assert ((v_list[1])['inc'] == 'True')
