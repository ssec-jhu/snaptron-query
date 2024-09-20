import pytest

from snaptron_query.app import snaptron_client as sc, exceptions, utils, column_defs


@pytest.mark.parametrize("coordinates", ["chr50:5000-6000", "chr:5000-6000", "some_random_string", "chrXY:4000-5000"])
def test_verify_bad_coordinates_with_errors(coordinates):
    with pytest.raises(exceptions.BadCoordinates):
        sc.verify_coordinates(coordinates)


def test_get_element_id_and_value(sample_ui_children):
    inc_junctions, exc_junctions = utils.get_element_id_and_value(sample_ui_children, 0)
    assert len(inc_junctions) == 1
    assert len(exc_junctions) == 1
    assert inc_junctions == ["chr19:4491836-4492014"]
    assert exc_junctions == ["chr19:4491836-4493702"]


def test_get_element_id_and_value_error(sample_ui_children_with_error):
    with pytest.raises(exceptions.MissingUserInputs):
        utils.get_element_id_and_value(sample_ui_children_with_error, 0)


@pytest.mark.parametrize("junction_count", [1, 2, 3, 4])
def test_get_col_multi_jiq(junction_count):
    assert len(column_defs.get_col_multi_jiq_calculations(junction_count)) == 3 * junction_count + 1


def test_get_col_jiq():
    assert len(column_defs.get_col_jiq_calculations()) == 5


@pytest.mark.parametrize("psi,value", [(100, 6.64), (50, 5.64), (25, 4.64), (0, -6.64)])
def test_log_2_plus(psi, value):
    # add this test in case epsilon value changes
    log2 = round(utils.log_2_plus(psi), 2)
    assert log2 == value


@pytest.mark.parametrize(
    "coordinates,result",
    [
        ("Chromosome 19: 4,472,297-4,502,208", "chr19:4472297-4502208"),
        ("Chromosome 10: 3,099,353- 3,101,364", "chr10:3099353-3101364"),
    ],
)
def test_coordinates_to_formatted_string(coordinates, result):
    assert sc.coordinates_to_formatted_string(sc.geq_verify_coordinate(coordinates)) == result
