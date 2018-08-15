import smartsheet
from ta_pov.basic_functions import *

ss_token = "your key"
ss = smartsheet.Smartsheet(ss_token)

sheet_info = get_sheet(ss, 'Tetration On-Demand POV Raw Data')
template_info = get_template(ss, 'Tetration On-Demand POV Status-Template')
print(template_info['id'])

rows = get_row_data(ss, sheet_info['id'])
columns = get_col_data(ss, sheet_info['id'])

for column in columns:
    print(column['index'], column['id'], column['title'])

for row in rows:
    cells = row['cells']
    for cell, column in zip(cells, columns):
        cell_val = cell['value'] if 'value' in cell else ''
        print(row['rowNumber'], cell['columnId'], column['title'], cell_val)

#
# ADD Rows Example
#
my_rows = []

row_data = []
row_data.append({
    'column_id': 625538021779332,
    'value': 'ang',
    'strict': False})
row_data.append({
    'column_id': 5129137649149828,
    'value': 'stan',
    'strict': False})
my_rows.append(row_data)

row_data = []
row_data.append({
    'column_id': 625538021779332,
    'value': 'blanche',
    'strict': False})
row_data.append({
    'column_id': 5129137649149828,
    'value': 'larry',
    'strict': False})
my_rows.append(row_data)

print ('my rows ', my_rows)
add_row(ss, sheet_info['id'], my_rows)

#
# END Add Rows Example
#





