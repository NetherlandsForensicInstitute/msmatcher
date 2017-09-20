
from lcms.analysis import read_file
from hamcrest import assert_that, equal_to


def test_read_file():
    filename = "data/esi-screening.mzml"
    s = read_file(filename)
    assert_that(len(s), equal_to(1115))
