import pytest

from snaptron_query.app import global_strings as gs, snaptron_client as sc, exceptions
from snaptron_query.app.tests.conftest import GEXQuery


def assert_test_gex(q, rail_id, factor, normalized_count, study):
    factors_df = q.get_factor_table()
    assert round(factors_df[rail_id], 2) == factor

    s = q.get_results().loc[rail_id]
    assert round(s[gs.table_geq_col_norm_count], 2) == normalized_count
    assert s[gs.snpt_col_study] == study


@pytest.mark.parametrize(
    "rail_id, factor, normalized_count, study",
    [
        (135471, 1.0, 83064.0, "DRP000366"),
        (123622, 1.0, 97738.0, "DRP000425"),
        (123624, 0.82, 276830.69, "DRP000425"),
        (499886, 0.18, 648015.1, "SRP072835"),
        (1000235, 0.71, 1445641.39, "SRP092075"),
        (158830, 1.0, 406092.0, "DRP000499"),
        (158832, 0.56, 573876.23, "DRP000499"),
        (158850, 0.33, 562352.66, "DRP000499"),
        (1000217, 1.0, 57605.0, "SRP072835"),
        (1000316, 1.0, 2025923, "SRP092075"),
        (1282825, 1.0, 634146, "SRP072829"),
        (475278, 1.0, 746481.0, "SRP072864"),
        (1282825, 1.0, 634146.0, "SRP072829"),
        (623044, 0.57, 713783.38, "SRP072829"),
        (1000283, 0.51, 2606573.21, "SRP092075"),
    ],
)
def test_gex(gene_query_srav3h_tardbp_with_edf1, rail_id, factor, normalized_count, study):
    assert_test_gex(gene_query_srav3h_tardbp_with_edf1, rail_id, factor, normalized_count, study)


@pytest.mark.parametrize(
    "rail_id, factor, normalized_count, study",
    [
        (135471, 1.0, 83064.0, "DRP000366"),
        (123622, 1.0, 97738.0, "DRP000425"),
        (123624, 0.82, 276830.69, "DRP000425"),
        (499886, 0.18, 648015.1, "SRP072835"),
        (1000235, 0.71, 1445641.39, "SRP092075"),
        (158830, 1.0, 406092.0, "DRP000499"),
        (158832, 0.56, 573876.23, "DRP000499"),
        (158850, 0.33, 562352.66, "DRP000499"),
        (1000217, 1.0, 57605.0, "SRP072835"),
        (1000316, 1.0, 2025923, "SRP092075"),
        (1282825, 1.0, 634146, "SRP072829"),
        (475278, 1.0, 746481.0, "SRP072864"),
        (1282825, 1.0, 634146.0, "SRP072829"),
        (623044, 0.57, 713783.38, "SRP072829"),
        (1000283, 0.51, 2606573.21, "SRP092075"),
    ],
)
def test_gex_lowercase_srav3h(
    gene_query_case_sensitive_srav3h_tardbp_with_edf1, rail_id, factor, normalized_count, study
):
    # same set of test but different query genes - testing case sensitivity
    # human dataset has uppercase gene names
    assert_test_gex(gene_query_case_sensitive_srav3h_tardbp_with_edf1, rail_id, factor, normalized_count, study)


@pytest.mark.parametrize(
    "rail_id, raw_count, study,sample_name",
    [
        (668214, 92751, "SRP218930", ""),
        (669863, 160700, "SRP061340", ""),
        (669871, 169448, "SRP061340", "MouseHippocampus(3mo)"),
        (669879, 284718, "SRP061340", "MouseHippocampus(3mo)"),
        (2885781, 116227, "SRP124512", "GSM2746530"),
        (2885847, 103324, "SRP124512", "GSM2746532"),
        (3072016, 22830, "SRP057123", "GSM1656720"),
        (213136, 1961764, "DRP005356", "SAMD00035958"),
        (3466847, 63146, "SRP170686", "GSM3486851"),
        (957629, 87250, "SRP219859", "GSM4047704"),
    ],
)
def test_srav1m_adnp2_normalized_edf1(
    gene_query_case_sensitive_srav1m_adnp2_with_edf1, rail_id, raw_count, study, sample_name
):
    # note this test is to ensure raw count calculations are the same even with normalization
    # factor and normalized counts are inaccurate as those need to be derived from a "grouped study" table
    s_nn = gene_query_case_sensitive_srav1m_adnp2_with_edf1.get_results().loc[rail_id]
    assert s_nn[gs.table_geq_col_raw_count] == raw_count
    assert s_nn[gs.snpt_col_study] == study

    if sample_name:
        assert s_nn["sample_name"] == sample_name


@pytest.mark.parametrize(
    "rail_id, raw_count, study,sample_name",
    [
        (668214, 92751, "SRP218930", ""),
        (669863, 160700, "SRP061340", ""),
        (669871, 169448, "SRP061340", "MouseHippocampus(3mo)"),
        (669879, 284718, "SRP061340", "MouseHippocampus(3mo)"),
        (2885781, 116227, "SRP124512", "GSM2746530"),
        (2885847, 103324, "SRP124512", "GSM2746532"),
        (3072016, 22830, "SRP057123", "GSM1656720"),
        (213136, 1961764, "DRP005356", "SAMD00035958"),
        (3466847, 63146, "SRP170686", "GSM3486851"),
        (957629, 87250, "SRP219859", "GSM4047704"),
    ],
)
def test_srav1m_adnp2_not_normalized(
    gene_query_case_sensitive_srav1m_ADNP2_not_normalized, rail_id, raw_count, study, sample_name
):
    s_nn = gene_query_case_sensitive_srav1m_ADNP2_not_normalized.get_results().loc[rail_id]
    assert s_nn[gs.table_geq_col_raw_count] == raw_count
    assert s_nn[gs.snpt_col_study] == study

    if sample_name:
        assert s_nn["sample_name"] == sample_name


@pytest.mark.parametrize(
    "coordinates,chromosome,start,end",
    [
        ("chr3:5555-6666", "chr3", 5555, 6666),
        ("chr3:4000-5000", "chr3", 4000, 5000),
        ("chr19:5000-6000", "chr19", 5000, 6000),
        ("chr19:4000-5000", "chr19", 4000, 5000),
        ("chr1:1020120-1056116", "chr1", 1020120, 1056116),
        ("Chromosome 19: 4,472,297-4,502,208", "chr19", 4472297, 4502208),
        ("Chromosome19: 4,472,297-4,502,208", "chr19", 4472297, 4502208),
        ("Chromosome19 :4,472,297-4,502,208", "chr19", 4472297, 4502208),
        ("Chromosome19:4,472,297-4,502,208", "chr19", 4472297, 4502208),
        ("Chromosome19:4,472297-4502,208", "chr19", 4472297, 4502208),
        ("Chromosome 1: 16,567,708-16,567,893", "chr1", 16567708, 16567893),
        ("chr22:20117650-20127052", "chr22", 20117650, 20127052),
        ("chr2:1631887-1744515", "chr2", 1631887, 1744515),
    ],
)
def test_geq_verify_coordinates(coordinates, chromosome, start, end):
    coordinates = sc.geq_verify_coordinate(coordinates)
    assert coordinates.chr == chromosome
    assert coordinates.start == start
    assert coordinates.end == end


@pytest.mark.parametrize("pair", ["chr19:7000-5000", "chr19:6000-3000"])
def test_geq_verify_coordinates_with_errors(pair):
    with pytest.raises(exceptions.BadCoordinates):
        sc.geq_verify_coordinate(pair)


def test_gex_errors_2(meta_data_dict_srav3h, gex_data_srav3h_TARDBP, gex_data_srav3h_EDF1):
    with pytest.raises(exceptions.NormalizationGeneNotFound):
        # EDF2 is a made up gene
        GEXQuery(
            query_gene_id="TARDBP",
            query_gene_snaptron_data=gex_data_srav3h_TARDBP,
            query_gene_meta_data_dict=meta_data_dict_srav3h,
            norm_gene_id="EDF2",
            norm_gene_snaptron_data=gex_data_srav3h_EDF1,
            norm_gene_meta_data_dict=meta_data_dict_srav3h,
        )
