import pandas as pd
import numpy as np
from sqlalchemy import MetaData, Table, Column

import config


def load_query(query):
    """
        loads data from db, based on the given sql query
    :param query: sql query in string
    :return: dataframe
    """
    df = pd.read_sql_query(query, con=config.db_connection)
    return df


def load_table(table):
    """
        loads table based from postgres and returns dataframe of the table
    :param table: string, table name
    :return: dataframe
    """
    df = pd.read_sql_table(table, con=config.db_connection)
    return df


def load_experiment_names():
    query = """SELECT experiment_id, filename FROM "Experiment" """
    return load_query(query)


def initialize_table(table_name, list_columns_types):
    """
    Creation (initialization) of postgressql table
    :return: empty table
    """
    con = config.db_connection
    if not con.dialect.has_table(con, table_name):
        metadata = MetaData(config.db_connection)
        Table(table_name, metadata, *(Column(**i) for i in list_columns_types))
        metadata.create_all()
        print("Table '{}' created".format(table_name))
    else:
        print("Table '{}' already exists, so the initialization will be skipped".format(table_name))


def append_to_experiment(table_name, column_names, check_existing=None):
    if check_existing is not None:
        col_name = check_existing
        value = column_names[col_name]
        sql = """SELECT {0} FROM "{1}" WHERE {0} = '{2}'""".format(col_name, table_name, value)
        if config.db_connection.execute(sql).fetchone() is not None:
            print("Value '{}' already exists in column '{}' in table '{}'. " +
                  "The value will not be added to the table".format(value, col_name, table_name))
            return None
    metadata = MetaData(bind=config.db_connection)
    mytable = Table(table_name, metadata, autoload=True)

    ins = mytable.insert()
    new_row = ins.values(column_names)
    config.db_connection.execute(new_row)
    print("Added values {} to table {}".format(column_names, table_name))


def return_heritage_id(file_name):
    """
    Check if file_name exists in heritage table. If so, return the heritage_id.
    :param file_name: name of file
    :return: heritage id that belongs to filename if it exists in the heritage_table
    """
    sql = """SELECT name, heritage_id FROM "Heritage" WHERE name = %s """

    result = config.db_connection.execute(sql, file_name).fetchone()
    if result is None:
        raise ValueError("file '{}' does not exist in 'Heritage' table. " +
                         "Check file name and/or add file name to 'Heritage table'"
                         .format(file_name))
    return result[1]


def load_peaks(experiment):
    if experiment == 'test':
        return pd.DataFrame(columns=['rt', 'mz', 'intensity', 'formula', 'label'], data=[[100, 85, 120, 'CO', 'blanco'],
                                                                                         [100, 95, 10, 'COH2', ''],
                                                                                         [100, 100.1, 30, 'COH3', ''],
                                                                                         [90, 100.1, 50, 'COH3', '']])
    if experiment == 'random':
        n = 200
        formulas = ['CO', 'COH2', 'COH3', None]
        weights = [.05, .15, .1, .7]
        peaks = np.random.randint(1, n, (n, 3))
        labels = np.random.choice(formulas, (n, 1), p=weights)
        blanco = np.random.choice(['blanco', None], (n, 1))
        data = np.concatenate((peaks, labels, blanco), axis=1)
        return pd.DataFrame(columns=['rt', 'mz', 'intensity', 'formula', 'label'], data=data)
    #
    # query = """SELECT
    #               spec.time_passed_since_start AS rt,
    #               peak.mz AS mz,
    #               peak.intensity AS intensity,
    #               fiv.base_formula AS formula,
    #               '' AS label --- TODO this could be more than one
    #             FROM "Experiment" exp
    #             JOIN "Spectrum" spec ON exp.experiment_id = spec.experiment_id
    #             JOIN "Peak" peak ON spec.spectrum_id = peak.spectrum_id AND spec.experiment_id = peak.experiment_id
    #             JOIN "PeakMatch" pm ON pm.spectrum_id = peak.spectrum_id AND pm.experiment_id = peak.experiment_id
    #             JOIN "FormulaIsotopeVariant" fiv ON pm.isotope_id = fiv.id
    #             JOIN "Label" label ON label.formula = fiv.base_formula
    #             where exp.experiment_id = {}""".format(experiment)
    #
    # # TODO deze staat erin omdat we de shortcut trivialpeakmatch gebruiken
    # # TODO dit kan problemen opleveren als we meerdere labels hebben
    # if True:
    query = """SELECT
              spec.time_passed_since_start AS rt,
              peak.mz AS mz,
              peak.intensity AS intensity,
              tpm.formula as formula
            FROM "Experiment" exp
            JOIN "Spectrum" spec ON exp.experiment_id = spec.experiment_id
            JOIN "Peak" peak ON spec.spectrum_id = peak.spectrum_id AND spec.experiment_id = peak.experiment_id
            LEFT JOIN "TrivialPeakMatch" tpm on tpm.matched_mass  = peak.mz
            where exp.experiment_id = {}""".format(experiment)

    return load_query(query)


def return_query_values_per_experiment(experiment_id):
    query = '''
    SELECT spec.time_passed_since_start AS rt, peak.mz AS mz, peak.intensity AS intensity, tpm.formula as formula, lab.label_name as label, exp.filename
    FROM "Experiment" exp
    JOIN "Spectrum" spec ON exp.experiment_id = spec.experiment_id
      JOIN "Peak" peak ON spec.spectrum_id = peak.spectrum_id AND spec.experiment_id = peak.experiment_id
      JOIN "TrivialPeakMatch" tpm on tpm.matched_mass = peak.mz LEFT JOIN "Label" lab on lab.formula = tpm.formula
    where exp.experiment_id = {} '''.format(experiment_id)
    return query


def load_df_per_exp(exp_id):
    df = load_query(return_query_values_per_experiment(exp_id))
    return df


def load_peaks_for_mz(experiment_id, min_value, max_value):
    """
    load peaks in an experiment where min_value <= mz < max_value per rt
    sums intensity of the peak where more than one mz on a rt
    concatenates the known formulas per rt, mz combination

    :param experiment_id: unique identifier of experiment (int)
    :param min_value: lower mz bound (float)
    :param max_value: upper mz bound (float)
    :return: pandas dataframe; rt, intensity, formulas
    """

    query = '''
        select
            spec.time_passed_since_start AS rt,
            sum(peak.intensity) AS intensity,
            string_agg(distinct tpm.formula, ', ') as formulas,
            string_agg(DISTINCT cn.name, ', ')     AS names
        FROM "Experiment" exp
            left JOIN "Spectrum" spec ON exp.experiment_id = spec.experiment_id
            left JOIN "Peak" peak ON spec.spectrum_id = peak.spectrum_id AND spec.experiment_id = peak.experiment_id
            left JOIN "TrivialPeakMatch" tpm on tpm.matched_mass = peak.mz and tpm.spectrum_id = spec.spectrum_id and exp.experiment_id = tpm.experiment_id
            left JOIN "ChemicalName" cn ON cn.formula = tpm.formula
        where
            exp.experiment_id = {0}
            and round(peak.mz::numeric,3) >= {1}
            and round(peak.mz::numeric,3) < {2}

        group by
            spec.time_passed_since_start '''.format(experiment_id, min_value, max_value)

    return load_query(query)


def load_peaks_for_rt(experiment_id, min_value, max_value):
    """
    load peaks in an experiment where min_value <= rt < max_value per mz
    sums intensity of the peaks where more than one mz on an rt
    concatenates the known formulas per rt, mz combination

    :param experiment_id: unique identifier of experiment (int)
    :param min_value: lower rt bound (float)
    :param max_value: upper rt bound (float)
    :return: pandas dataframe; mz, intensity, formulas
    """
    query = '''
        select
            round(peak.mz::numeric,3) AS mz,
            sum(peak.intensity) AS intensity,
            string_agg(distinct tpm.formula, ', ') as formulas,
            string_agg(DISTINCT cn.name, ', ')     AS names
        FROM "Experiment" exp
            left JOIN "Spectrum" spec ON exp.experiment_id = spec.experiment_id
            left JOIN "Peak" peak ON spec.spectrum_id = peak.spectrum_id AND spec.experiment_id = peak.experiment_id
            left JOIN "TrivialPeakMatch" tpm on tpm.matched_mass = peak.mz and tpm.spectrum_id = spec.spectrum_id and exp.experiment_id = tpm.experiment_id
            left JOIN "ChemicalName" cn ON cn.formula = tpm.formula
        where
            exp.experiment_id = {0}
            and spec.time_passed_since_start >= {1}
            and spec.time_passed_since_start < {2}
            and not peak.mz is null
        group by
            round(peak.mz::numeric,3) '''.format(experiment_id, min_value, max_value)

    return load_query(query)
