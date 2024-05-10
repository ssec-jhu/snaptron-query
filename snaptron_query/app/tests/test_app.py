import pytest

from snaptron_query.app import snaptron_client as sc, exceptions, utils


@pytest.mark.parametrize('coordinates', ["chr50:5000-6000", 'chr:5000-6000', 'some_random_string', 'chrXY:4000-5000'])
def test_verify_bad_coordinates_with_errors(coordinates):
    with pytest.raises(exceptions.BadCoordinates):
        sc.verify_coordinates(coordinates)


def test_get_element_id_and_value(sample_ui_children):
    inc_junctions, exc_junctions = utils.get_element_id_and_value(sample_ui_children, 0)
    assert len(inc_junctions) == 1
    assert len(exc_junctions) == 1
    assert inc_junctions == ['chr19:4491836-4492014']
    assert exc_junctions == ['chr19:4491836-4493702']


def test_get_element_id_and_value_error(sample_ui_children_with_error):
    with pytest.raises(exceptions.MissingUserInputs):
        utils.get_element_id_and_value(sample_ui_children_with_error, 0)