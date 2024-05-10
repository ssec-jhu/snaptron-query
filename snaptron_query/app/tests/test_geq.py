import pytest

from snaptron_query.app import global_strings as gs, snaptron_client as sc, exceptions
from snaptron_query.app.tests.conftest import GEXQuery


@pytest.mark.parametrize('rail_id, factor, normalized_count',
                         [(135471, 1.0, 83064.0),  # DRP000366
                          (123622, 1.0, 97738.0),  # DRP000425
                          (158830, 1.0, 406092.0),  # DRP000499
                          (158850, 0.33, 562352.66),  # DRP000499
                          (1000217, 1.0, 57605.0),  # SRP072835
                          (1000316, 1.0, 2025923),  # SRP092075
                          (1282825, 1.0, 634146),  # SRP072829
                          (475278, 1.0, 746481.0),  # SRP072864
                          (1282825, 1.0, 634146.0),  # ''SRR3330930''
                          (1000283, 0.51, 2606573.21)  # 'SRR4450435'
                          ])
def test_gex(gene_query, rail_id, factor, normalized_count):
    factors_df = gene_query.get_factor_table()
    assert (round(factors_df[rail_id], 2) == factor)

    s = gene_query.get_results().loc[rail_id]
    assert (round(s[gs.table_geq_col_norm_count], 2) == normalized_count)


@pytest.mark.parametrize('coordinates,chromosome,start,end',
                         [('chr3:5555-6666', 'chr3', 5555, 6666),
                          ('chr3:4000-5000', 'chr3', 4000, 5000),
                          ('chr19:5000-6000', 'chr19', 5000, 6000),
                          ('chr19:4000-5000', 'chr19', 4000, 5000)]
                         )
def test_geq_verify_coordinates(coordinates, chromosome, start, end):
    (geq_chr, geq_start, geq_end) = sc.geq_verify_coordinate(coordinates)
    assert geq_chr == chromosome
    assert geq_start == start
    assert geq_end == end


@pytest.mark.parametrize('pair', ['chr19:7000-5000', 'chr19:6000-3000'])
def test_geq_verify_coordinates_with_errors(pair):
    with pytest.raises(exceptions.BadCoordinates):
        sc.geq_verify_coordinate(pair)


def test_gex_errors_2():
    with pytest.raises(exceptions.NormalizationGeneNotFound):
        # EDF2 is a made up gene
        GEXQuery('TARDBP', 'EDF2')


# def test_gex_errors_1():
#     with pytest.raises(exceptions.QueryGeneNotFound):
#         GEXQuery('MT1XP1')
