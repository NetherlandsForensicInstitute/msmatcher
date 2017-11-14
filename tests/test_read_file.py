
from lcms.analysis import read_file
from hamcrest import assert_that, equal_to, not_none


def test_read_file():
    filename = "data/esi-blanco-screening.mzML"
    s = read_file(filename)
    assert_that(len(s), equal_to(1115))


def test_read_spectrum():
    filename = "data/esi-blanco-screening.mzML"
    s = read_file(filename)
    spectrum = s[100]
    assert_that(spectrum, not_none)
    for mz in spectrum.mz:
        print(mz)


def test_first_sample():
    filename = "data/esi-screening.mzML"
    s = read_file(filename)
    sample = s[1]
    mz = sample.mz
    assert_that(len(mz), equal_to(58))
    peaks = sample.peaks('raw')
    assert_that(len(peaks), equal_to(58))


def test_third_sample_raw():
    filename = "data/esi-screening.mzML"
    s = read_file(filename)
    sample = s[3]
    mz = sample.mz
    assert_that(len(mz), equal_to(130))
    peaks = sample.peaks('raw')
    print(peaks)
    assert_that(len(peaks), equal_to(130))


def test_third_sample_centroided():
    filename = "data/esi-screening.mzML"
    s = read_file(filename)
    sample = s[3]
    mz = sample.mz
    assert_that(len(mz), equal_to(130))
    peaks = sample.peaks('centroided')
    assert_that(len(peaks), equal_to(130))


def test_third_sample_reprofiled():
    filename = "data/esi-screening.mzML"
    s = read_file(filename)
    sample = s[3]
    mz = sample.mz
    assert_that(len(mz), equal_to(130))
    peaks = sample.peaks('reprofiled')
    assert_that(len(peaks), equal_to(1132))


def test_third_sample_highest():
    filename = "data/esi-screening.mzML"
    s = read_file(filename)
    sample = s[3]
    mz = sample.mz
    assert_that(len(mz), equal_to(130))
    peaks = sample.highest_peaks(5)
    assert_that(len(peaks), equal_to(5))
    got_peak = sample.has_peak(183.0717848)
    assert_that(got_peak, equal_to([]))
