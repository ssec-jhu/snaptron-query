import pytest
import os
import httpx

from snaptron_query.app import snaptron_client as sc, global_strings as gs

IN_GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"


# skipping test on GITHUB as these tests are tests that run against the snaptron API itself and does a http request
@pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Skipping test on Github")
@pytest.mark.parametrize('compilation, region, query_mode',
                         [(gs.compilation_srav3h, 'chr19:4491836-4493702', 'snaptron'),
                          (gs.compilation_gtexv2, 'chr19:4491836-4493702', 'snaptron'),
                          (gs.compilation_tcgav2, 'chr19:4491836-4493702', 'snaptron'),
                          (gs.compilation_srav1m, 'chr19:4491836-4493702', 'snaptron')])
def test_snaptron(compilation, region, query_mode):
    df = sc.get_snpt_query_results_df(compilation, region, query_mode)
    assert not df.empty


# skipping test on GITHUB as these tests are tests that run against the snaptron API itself and does a http request
@pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Skipping test on Github - this must run locally")
@pytest.mark.parametrize('human_gene', ['TARDBP', 'ACTL6B', 'AGRN', 'EPB41L4A', 'GPSM2', 'PFKP', 'RANBP1', 'STMN2',
                                        'UNC13A', 'UNC13B', 'SLC24A3', 'IGLON5', 'KALRN', 'MYO18A', 'RSF1', 'SYT7',
                                        'SYNE1', 'CAMK2B', 'PXDN', 'TRRAP'])
def test_snaptron_gene_human(compilations, human_gene):
    for compilation in compilations:
        df = sc.get_snpt_query_results_df(compilation, human_gene, 'genes')
        assert not df.empty


# skipping test on GITHUB as these tests are tests that run against the snaptron API itself and does a http request
@pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Skipping test on Github - this must run locally")
@pytest.mark.parametrize('human_gene', ['MT1XP1', 'HDGFL2'])
def test_snaptron_gene_human_missing(compilations, human_gene):
    for compilation in compilations:
        with pytest.raises(httpx.RemoteProtocolError):
            sc.get_snpt_query_results_df(compilation, human_gene, 'genes')
