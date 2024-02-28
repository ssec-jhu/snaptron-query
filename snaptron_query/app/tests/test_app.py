import pandas as pd

from snaptron_query.app import query_junction_inclusion as jiq

from snaptron_query.app import global_strings as gs

df_srav3h_meta_data = pd.read_csv('./data/test_samples_SRAv3h.csv',
                                  usecols=gs.srav3h_meta_data_required_list).set_index(gs.snaptron_col_rail_id)

df_from_snaptron = pd.read_csv('./data/test_srav3h_chr19_4491836_4493702.tsv', sep='\t')

exclusion_start = 4491836
exclusion_end = 4493702
inclusion_start = 4491836
inclusion_end = 4492014
# find the exclusion and inclusion junction rows
query_mgr = jiq.JunctionInclusionQueryManager(exclusion_start, exclusion_end, inclusion_start, inclusion_end)
df_jiq_results = query_mgr.run_junction_inclusion_query(df_from_snaptron, df_srav3h_meta_data)
df_jiq_results = df_jiq_results.set_index(gs.snaptron_col_rail_id)

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
    assert ((v_list[0])['count'] == 35)
    assert ((v_list[0])['inc'] == 'False')
    # check inclusion values
    assert ((v_list[1])['count'] == 1)
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

# turn these two tests on when testing with full data locally
# def test_jiq_results_size_data_count():
#     assert(df_jiq_results.shape[0]== 160576)
#     assert(df_jiq_results.shape[1] == 11)

def test_jiq_results_size_cols():
     assert(df_jiq_results.shape[1] == 11)

def test_jiq_results_1():
    s = df_jiq_results.loc[1000010]
    assert(s[gs.snaptron_col_external_id] == 'SRR3743424')
    assert (s['inc'] == 0)
    assert (s['exc'] == 11)
    assert (s['psi'] == 0.0)

def test_jiq_results_2():
    s = df_jiq_results.loc[2171668]
    assert(s[gs.snaptron_col_external_id] == 'SRR5714918')
    assert (s['inc'] == 35)
    assert (s['exc'] == 0)
    assert (s['psi'] == 100.0)

def test_jiq_results_3():
    s = df_jiq_results.loc[988956]
    assert(s[gs.snaptron_col_external_id] == 'SRR5461171')
    assert (s['inc'] == 66)
    assert (s['exc'] == 102)
    assert (s['psi'] == 39.29)
def test_jiq_results_4():
    s = df_jiq_results.loc[1127039]
    assert(s[gs.snaptron_col_external_id] == 'SRR5398327')
    assert (s['inc'] == 4)
    assert (s['exc'] == 12)
    assert (s['psi'] == 25.0)

def test_jiq_results_5():
    s = df_jiq_results.loc[499887]
    assert(s[gs.snaptron_col_external_id] == 'SRR3469415')
    assert (s['inc'] == 9)
    assert (s['exc'] == 23)
    assert (s['psi'] == 28.12)

def test_jiq_results_6():
    s = df_jiq_results.loc[988942]
    assert(s[gs.snaptron_col_external_id] == 'SRR5461170')
    assert (s['inc'] == 65)
    assert (s['exc'] == 101)
    assert (s['psi'] == 39.16)

def test_jiq_results_7():
    s = df_jiq_results.loc[1641727]
    assert(s[gs.snaptron_col_external_id] == 'SRR8083867')
    assert (s['inc'] == 17)
    assert (s['exc'] == 55)
    assert (s['psi'] == 23.61)

def test_jiq_results_8():
    s = df_jiq_results.loc[1641757]
    assert(s[gs.snaptron_col_external_id] == 'SRR8083868')
    assert (s['inc'] == 12)
    assert (s['exc'] == 45)
    assert (s['psi'] == 21.05)

def test_jiq_results_9():
    s = df_jiq_results.loc[2109561]
    assert(s[gs.snaptron_col_external_id] == 'SRR6873183')
    assert (s['inc'] == 12)
    assert (s['exc'] == 34)
    assert (s['psi'] == 26.09)