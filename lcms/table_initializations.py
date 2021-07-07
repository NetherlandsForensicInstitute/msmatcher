from sqlalchemy import types
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
from sqlalchemy.sql.expression import func

from utils import initialize_table

table_name = 'Heritage'
columns = [{'name': 'heritage_id', 'type_': types.Integer, 'primary_key': True, 'index': True},
           {'name': 'name', 'type_': types.String},
           {'name': 'entered', 'type_': types.DateTime, 'server_default': func.now()}]
initialize_table(table_name, columns)

table_name = 'Formula'
columns = [{'name': 'formula', 'type_': types.VARCHAR(length=255), 'index': True},
           {'name': 'mass', 'type_': DOUBLE_PRECISION},
           {'name': 'mass_minus', 'type_': DOUBLE_PRECISION},
           {'name': 'mass_plus', 'type_': DOUBLE_PRECISION},
           {'name': 'heritage_id', 'type_': types.Integer}]
initialize_table(table_name, columns)

table_name = 'Label'
columns = [{'name': 'formula', 'type_': types.VARCHAR(length=255), 'index': True},
           {'name': 'label_name', 'type_': types.VARCHAR(length=255)},
           {'name': 'preference', 'type_': types.Integer}]
initialize_table(table_name, columns)

table_name = 'Experiment'
columns = [{'name': 'experiment_id', 'type_': types.Integer, 'primary_key': True, 'index': True},
           {'name': 'run_id', 'type_': types.VARCHAR(length=255)},
           {'name': 'run_start_time', 'type_': DOUBLE_PRECISION},
           {'name': 'human_run_start_time', 'type_': types.DateTime},
           {'name': 'spectra_count', 'type_': types.Integer},
           {'name': 'experimental_state_id', 'type_': types.Integer},
           {'name': 'match_type_id', 'type_': types.Integer},
           {'name': 'filename', 'type_': types.VARCHAR(length=255)}]
initialize_table(table_name, columns)

table_name = 'ExperimentalState'
columns = [{'name': 'id', 'type_': types.Integer, 'primary_key': True, 'index': True},
           {'name': 'description', 'type_': types.VARCHAR(length=255)}]
initialize_table(table_name, columns)

table_name = 'Measurement'
columns = [{'name': 'experiment_id', 'type_': types.Integer, 'primary_key': True, 'index': True},
           {'name': 'spectrum_id', 'type_': types.Integer, 'primary_key': True, 'index': True},
           {'name': 'mz', 'type_': types.LargeBinary},
           {'name': 'intensity', 'type_': types.LargeBinary}]
initialize_table(table_name, columns)

table_name = 'MatchType'
columns = [{'name': 'id', 'type_': types.Integer, 'primary_key': True, 'index': True},
           {'name': 'name', 'type_': types.VARCHAR(length=255)},
           {'name': 'correction', 'type_': DOUBLE_PRECISION}]
initialize_table(table_name, columns)

table_name = 'Spectrum'
columns = [{'name': 'experiment_id', 'type_': types.Integer, 'index': True},
           {'name': 'spectrum_id', 'type_': types.Integer, 'primary_key': True, 'index': True},
           {'name': 'total_ion_current', 'type_': DOUBLE_PRECISION},
           {'name': 'time_passed_since_start', 'type_': DOUBLE_PRECISION},
           {'name': 'ms_level', 'type_': types.Integer},
           {'name': 'lowest_observed_mz', 'type_': DOUBLE_PRECISION},
           {'name': 'highest_observed_mz', 'type_': DOUBLE_PRECISION},
           {'name': 'scan_window_lower_limit', 'type_': DOUBLE_PRECISION},
           {'name': 'scan_window_upper_limit', 'type_': DOUBLE_PRECISION}]
initialize_table(table_name, columns)

#
# The following table is for storing the information resulting from a trivial
# match between a peak and a formula.
#
table_name = 'TrivialPeakMatch'
columns = [{'name': 'experiment_id', 'type_': types.Integer, 'primary_key': True, 'index': True},
           {'name': 'formula', 'type_': types.VARCHAR(length=255), 'primary_key': True,
            'index': True},
           {'name': 'spectrum_id', 'type_': types.Integer, 'primary_key': True, 'index': True},
           {'name': 'matched_mass', 'type_': DOUBLE_PRECISION},
           {'name': 'deviation', 'type_': DOUBLE_PRECISION},
           {'name': 'match_type_id', 'type_': types.Integer}]
initialize_table(table_name, columns)

table_name = 'PeakMatch'
columns = [{'name': 'experiment_id', 'type_': types.Integer, 'primary_key': True, 'index': True},
           {'name': 'isotope_id', 'type_': types.Integer, 'primary_key': True, 'index': True},
           {'name': 'base_formula', 'type_': types.VARCHAR(length=255), 'primary_key': True,
            'index': True},
           {'name': 'spectrum_id', 'type_': types.Integer, 'primary_key': True, 'index': True},
           {'name': 'deviation', 'type_': DOUBLE_PRECISION},
           {'name': 'uncertainty', 'type_': DOUBLE_PRECISION},
           {'name': 'match_type_id', 'type_': types.Integer}]
initialize_table(table_name, columns)

table_name = 'Peak'
columns = [{'name': 'experiment_id', 'type_': types.Integer, 'index': True},
           {'name': 'spectrum_id', 'type_': types.Integer, 'index': True},
           {'name': 'mz', 'type_': DOUBLE_PRECISION},
           {'name': 'intensity', 'type_': DOUBLE_PRECISION}]
initialize_table(table_name, columns)

table_name = 'FormulaIsotopeVariant'
columns = [{'name': 'id', 'type_': types.Integer, 'primary_key': True, 'index': True},
           {'name': 'base_formula', 'type_': types.VARCHAR(length=255), 'primary_key': True,
            'index': True},
           {'name': 'isotope_formula', 'type_': types.VARCHAR(length=255)},
           {'name': 'mass', 'type_': DOUBLE_PRECISION},
           {'name': 'mass_minus', 'type_': DOUBLE_PRECISION},
           {'name': 'mass_plus', 'type_': DOUBLE_PRECISION}]
initialize_table(table_name, columns)

table_name = 'Isomer'
columns = [
    {'name': 'formula', 'type_': types.VARCHAR(length=255), 'index': True},
    {'name': 'id', 'type_': types.Integer, 'primary_key': True, 'index': True,
     'autoincrement': True},
    {'name': 'retention_time', 'type_': DOUBLE_PRECISION},
    {'name': 'figure', 'type_': types.LargeBinary}]
initialize_table(table_name, columns)

table_name = 'ChemicalName'
columns = [
    {'name': 'formula', 'type_': types.VARCHAR(length=255), 'index': True},
    {'name': 'isomer_id', 'type_': types.Integer, 'index': True},
    {'name': 'name', 'type_': types.VARCHAR(length=255)},
    {'name': 'preference', 'type_': types.INTEGER}]
initialize_table(table_name, columns)
