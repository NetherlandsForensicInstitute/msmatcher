import glob
from collections import namedtuple

import dateutil.parser
import numpy as np
import pandas as pd
import pymzml

import config
import lcms.utils as utils


def create_spectrum_and_peak_tables(msrun_list, experiment_id):
    '''
    fills the Spectrum table and for each spectrum the Peak table

    :param msrun_list:
    :param experiment_id:
    :return:
    '''

    spectrum = namedtuple('spectrum',
                          'experiment_id ' +
                          'spectrum_id ' +
                          'total_ion_current ' +
                          'time_passed_since_start ' +
                          'ms_level ' +
                          'highest_observed_mz ' +
                          'lowest_observed_mz ' +
                          'scan_window_upper_limit ' +
                          'scan_window_lower_limit')
    measurement = namedtuple('measurement',
                             'experiment_id ' +
                             'spectrum_id' +
                             ' mz' +
                             ' intensity')

    spectrum_list = []
    measurement_list = []
    for i, spc in enumerate(msrun_list):
        if i % 100 == 0:
            print("Spectrum {}".format(i))
        s = spectrum(experiment_id=experiment_id, spectrum_id=spc.ID,
                     total_ion_current=spc['total ion current'],
                     time_passed_since_start=spc['scan start time'], ms_level=spc['ms level'],
                     highest_observed_mz=spc['highest observed m/z'],
                     lowest_observed_mz=spc['lowest observed m/z'],
                     scan_window_upper_limit=spc['scan window upper limit'],
                     scan_window_lower_limit=spc['scan window lower limit'])
        spectrum_list.append(s)

        if i == 0:
            m = measurement(experiment_id=experiment_id, spectrum_id=spc.ID, mz=np.nan,
                            intensity=np.nan)
        else:
            m = measurement(experiment_id=experiment_id, spectrum_id=spc.ID, mz=spc.mz,
                            intensity=spc.i)

            # Fill peak table if experiment_id + spectrum_id do not already exist in table Peak
            check_peak = config.db_connection.execute(
                """SELECT experiment_id from "Peak"
                   WHERE experiment_id = '{}'
                         AND spectrum_id = '{}'"""
                .format(experiment_id, spc.ID)).fetchone()
            if check_peak is not None:
                print(
                    ("Experiment_id {} + spectrum_id {} combination already exists in Peak table. " +
                     "To avoid duplicates the spectra won't be added to the Peak table").format(experiment_id, spc.ID))
            else:
                peak_table = pd.DataFrame({"mz": spc.mz, "intensity": spc.i})
                peak_table['experiment_id'] = experiment_id
                peak_table['spectrum_id'] = spc.ID
                peak_table.to_sql('Peak', con=config.db_connection, index=False, if_exists='append')
                print("Appended to Peak table from experiment_id: {}, spectrum_id: {}".format(experiment_id, spc.ID))
        measurement_list.append(m)

    # check if experiment_id already exists in Spectrum table. If not, append data to Spectrum table
    check_spectrum = config.db_connection.execute(
        """SELECT experiment_id from "Spectrum" WHERE experiment_id = '{}' """
        .format(experiment_id)).fetchone()
    if check_spectrum is not None:
        print(("Experiment_id {} already exists in Spectrum table. " +
              "To avoid duplicates the spectra won't be added to the Spectrum table")
              .format(experiment_id))
    else:
        spectrum_table = pd.DataFrame(spectrum_list)
        spectrum_table.to_sql('Spectrum', con=config.db_connection, index=False, if_exists='append')
        print("Appended to Spectrum table with info from experiment_id: {}".format(experiment_id))


def create_experiment(msrun_list, filename):
    """
    Create a new experiment structure based on the information in the msrun_list.

    :param msrun_list: an open pymzml runner
    :param filename: name of the pymzml file
    :return: a dictionary containing the initialized experiment
    """
    experiment = dict.fromkeys(['run_id', 'run_start_time', 'human_run_start_time', 'spectra_count',
                                'experimental_state_id', 'match_type_id', 'filename'])

    # Todo: waarden in onderstaande tabel moeten nog ingevuld worden
    experiment['run_id'] = msrun_list.info['run_id']
    if "start_time" in msrun_list.info.keys():
        start_time_str = msrun_list.info["start_time"]
        start_time = dateutil.parser.parse(start_time_str)
        experiment['run_start_time'] = start_time.timestamp()
        experiment['human_run_start_time'] = start_time
    else:
        experiment['run_start_time'] = None
        experiment['human_run_start_time'] = None
    experiment['spectra_count'] = msrun_list.info['spectrum_count']
    experiment['experimental_state_id'] = None
    experiment['match_type_id'] = None
    experiment['filename'] = filename.split('/')[-1]
    return experiment


def create_experiment_table(msrun_list, filename):
    """
    fills the Experiment table.

    :param msrun_list: an open pymzml runner
    :param filename: name of the pymzml file
    :return:
    """
    experiment = create_experiment(msrun_list, filename)
    utils.append_to_experiment('Experiment', experiment)

    experiment_id = config.db_connection.execute(
        """SELECT experiment_id from "Experiment" WHERE filename = '{}' """.format(
            filename.split('/')[-1])).fetchone()[0]
    return experiment_id


def read_file(filename):
    msrun = pymzml.run.Reader(filename)
    msrun_list = list(msrun)

    # check if filename already in Experiment table
    check = config.db_connection.execute(
        """SELECT experiment_id from "Experiment" WHERE filename = '{}' """.format(
            filename.split('/')[-1])).fetchone()
    if check is not None:
        print("File already exists in DB. Continue to filling Spectrum table")
        experiment_id = check[0]
    else:
        # fill the Experiment table with data from file
        experiment_id = create_experiment_table(msrun_list, filename)

    # fill the Spectrum and Peak table with data from file
    create_spectrum_and_peak_tables(msrun_list, experiment_id)


if __name__ == "__main__":
    for n, filename in enumerate(glob.iglob('{}Geconverteerd/*.mzML'.format(config.data_dir))):
        print("reading file {} ({})".format(n, filename.split('/')[-1]))
        if '+' in filename.split('/')[-1]:
            print("Raw data, will be skipped for now")
            continue
        read_file(filename)
