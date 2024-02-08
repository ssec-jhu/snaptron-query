import pandas as pd

from snaptron_query.app import query_junction_inclusion as jiq

# def test_run_query_sync():
#     from snaptron_query.app.snaptron_client import SnaptronClientManager
#     test_url = 'https://snaptron.cs.jhu.edu/srav3h/snaptron?regions=chr19:4491836-4493702'
#     sqm = SnaptronClientManager(test_url)
#     resp = sqm.run_query_sync()
#     assert resp.status_code == 200
#
# def test_run_query_sync_false():
#     from snaptron_query.app.snaptron_client import SnaptronClientManager
#     bad_url = 'https://snaptron.cs.jhu.edu/srav3/snaptron?regions=chr19:4491836-4493702'
#     test_url = 'https://snaptron.cs.jhu.edu/srav3h/snaptron?regions=chr19:4491836-4493702'
#     sqm = SnaptronClientManager(test_url)
#     resp = sqm.run_query_sync()
#     assert resp.status_code != 200

def test_jiq__srav3h_001():

    # read test snaptron data instead of web results
    df_from_snaptron = pd.read_csv('test_srav3h_chr19_4491836_4493702.tsv', sep='\t')
    df_srav3h_meta_data = jiq.read_srav3h()

    qm = jiq.JunctionInclusionQueryManager(4491836, 4493702,
                                           4491836, 4492014)

    qm = jiq.JunctionInclusionQueryManager(4491836, 4493702,
                                           4491836, 4492014)

    results_df = qm.run_junction_inclusion_query(df_from_snaptron, df_srav3h_meta_data)


