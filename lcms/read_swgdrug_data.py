import numpy as np
import pandas as pd

import config
from utils import append_to_experiment, return_heritage_id, load_table

file_name = 'SWGDRUG formulae and exact masses 112916'
extension = 'xlsx'
swgdrug_path = '{}{}.{}'.format(config.data_dir, file_name, extension)

swgdrug = pd.read_excel(swgdrug_path, sheetname=0, skiprows=7,
                        names=['formula', 'name', 'mass', 'mass_plus', 'mass_minus'])

append_to_experiment('Heritage', {'name': file_name}, 'name')
heritage_id = return_heritage_id(file_name)

#  fill formula table
formula = swgdrug.drop('name', axis=1, inplace=False, errors='raise')
formula.drop_duplicates(inplace=True)  # only unique formulas
formula.insert(0, 'heritage_id', heritage_id)
formula.to_sql('Formula', con=config.db_connection, index=False, if_exists='append')

# fill Isomer table
# todo: retention time/ figure
isomer = swgdrug[['formula']]
isomer.insert(1, 'retention_time', np.nan)  # waar halen we die vandaan?
isomer.insert(2, 'figure', np.nan)  # waar halen we die vandaan?
isomer.to_sql('Isomer', con=config.db_connection, index=False, if_exists='append')

# fill label table
label = swgdrug[['formula', 'name']]
label.insert(2, 'preference', np.nan)
label.insert(3, 'isomer_id', np.nan)
isomer_table = load_table('Isomer')

# loop over the isomer table and get index of the formula name.
# for now we can only match on formula name, and there can be multiple formulas with the same name
# we match on the first match found, and this match will then be removed from isomer_table.
for index, row in label.iterrows():
    formula, name = row['formula'], row['name']
    try:
        id_match = isomer_table[isomer_table['formula'] == formula].iloc[0]['id']
    except:
        raise ValueError("Formula name '{}' does not exist in Isomer table".format(formula))
    isomer_table = isomer_table[isomer_table.id != id_match]
    label.at[index, 'isomer_id'] = id_match

label.to_sql('ChemicalName', con=config.db_connection, index=False, if_exists='append')
