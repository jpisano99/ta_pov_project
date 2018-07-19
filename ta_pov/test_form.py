import smartsheet
import json

# Application Passwords kept here
from ta_pov import my_secrets

# Smartsheet Config settings
ss_config = dict(
    SS_TOKEN = my_secrets.passwords["SS_TOKEN"]
)

ss_token = ss_config['SS_TOKEN']
ss = smartsheet.Smartsheet(SS_)
sheet_name = 'US Commercial Tetration Forecast'
customer_name = 'Advanced Disposal'

# Find my Sheet ID
response = ss.Sheets.list_sheets(include_all=True)
response_dict = response.to_dict()
sheets = response.data
for sheet in sheets:
    if sheet.name == sheet_name:
        sheet_id = sheet.id

# Get all the sheet info
sheet = ss.Sheets.get_sheet(sheet_id,include='rowIds')
sheet_dict = sheet.to_dict()

# GET SHEET RESPONSE DEBUG CODE - DO NOT DELETE
# print(json.dumps(sheet_dict, indent=2))


# Get all the columns from the primary sheet dict
columns = sheet.columns
col_id_dict = {}
for column in columns:
    col_id_dict[column.title] = column.id
    if column.title == 'Customer':
        customer_col_id = column.id
        print(column.title, column.id)

# Get all the rows from the primary sheet dict
# and pull out the customer names
rows = sheet_dict.get('rows', {})
customer_list = []
for row in rows:
    cells = row['cells']
    row_num = row['rowNumber']
    for cell in cells:
        if cell['columnId'] == customer_col_id:
            customer_list.append(cell['displayValue'])

print(customer_list)
print(customer_col_id)
# print('Customer Name # '+ str(row_num), cell['displayValue'])

exit()