import pymzml
from lcms import parse_mzml
from hamcrest import assert_that, equal_to, not_none


def test_create_experiment():
    filename = "data/esi-blanco-screening.mzML"
    run = pymzml.run.Reader(filename)
    info = run.info
    print(info)
    experiment = parse_mzml.create_experiment(run, filename)

    assert_that(experiment['run_id'], not_none)
    assert_that(experiment['run_start_time'], not_none)
    assert_that(experiment['run_start_time'], equal_to(1504783529.0))
    assert_that(experiment['run_id'], equal_to("ESI_x002b__x0020_blanco_x0020_-_x0020_screening_x0020_03"))
    assert_that(experiment['spectra_count'], equal_to(1115))
