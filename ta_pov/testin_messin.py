import smartsheet
from ta_pov.basic_functions import *

ss_token = "yik85b7gkvst4a4p4waqz0hxgq"
ss = smartsheet.Smartsheet(ss_token)

sheet_info = get_sheet(ss, 'Tetration On-Demand POV Raw Data')
rows = get_row_data(ss, sheet_info['id'])
columns = get_col_data(ss, sheet_info['id'])

for column in columns:
    # print(column['index'], column['id'], column['title'])
    pass

# Go down the rows
rows_to_delete = []
for row in rows:
    cells = row['cells']
    for cell, column in zip(cells, columns):
        # Loop over the cells in the row and include the columns to get the names
        cell_val = cell['value'] if 'value' in cell else ''  # In case cell has no value assign null
        # print(row['rowNumber'], cell['columnId'], column['title'], cell_val)

        if column['title'] == 'company_name':
            if cell_val == 'blanche' or cell_val == 'ang':
                rows_to_delete.append(row['id'])
                print('i need to delete row ', rows_to_delete,cell_val)

#del_rows(ss, sheet_info['id'], rows_to_delete)

# find_it(ss,sheet_id, col_name,  )
query = 'Dirk'

# Search everything
result = ss.Search.search_sheet(sheet_info['id'], query)
print(result)
exit()


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
add_rows(ss, sheet_info['id'], my_rows)

#
# END Add Rows Example
#


template_info = get_template(ss, 'Tetration On-Demand POV Status-Template')
print(template_info['id'])




#
#
# response = ss.Templates.list_user_created_templates()
# templates =  response.data
#
# for template in templates:
#     if template.name == 'Tetration On-Demand POV Status-Template':
#         print(template.name,template.id)
# exit()
#
# # Create a new blank POV Update from the Template
# new_sheet_name = 'Tetration POV On-Demand POV Status'
# template_name = 'Tetration On-Demand POV Status-Template'
# template_id = 6937344860284804  # TA POV Template ID
# response = ss.Home.create_sheet_from_template(
#             ss.models.Sheet({'name': new_sheet_name, 'from_id': template_id}))
# new_sheet = response.result
# new_sheet_id = new_sheet.id
#
# # Copy all the rows from the working POV BOT Update to the
# # Newly created Status SS
#
# bot_update_id = 7723272335845252  # JIMs POV BOT Update
#
# # Gather all the row id's from the working file
# bot_update_rows = []
# sheet = ss.Sheets.get_sheet(bot_update_id)
# for row in sheet.rows:
#     bot_update_rows.append(row.id)
#
# response = ss.Sheets.copy_rows(
#   bot_update_id,               # sheet_id of rows to be copied
#   ss.models.CopyOrMoveRowDirective({
#     'row_ids': bot_update_rows,
#     'to': ss.models.CopyOrMoveRowDestination({
#       'sheet_id': new_sheet_id })}))
#
#
#
#
#
# exit()
# # Rename the newly created sheet
# updated_sheet = ss.Sheets.update_sheet(
#         new_sheet.id, ss.models.Sheet(
#             {'name': 'Tetration POV On-Demand POV Status'}))
#
# exit()
#
#
# # Find my Sheet ID
# response = ss.Sheets.list_sheets(include_all=True)
# response_dict = response.to_dict()
# sheets = response.data
#
# # for sheet in sheets:
# #     if sheet.name == sheet_name:
# #         sheet_id = sheet.id
#
# print(sheet_id)
#
# response = ss.Sheets.get_sheet(sheet_id, include=['format'])
# response_dict = response.to_dict()
#
# # RESPONSE DEBUG CODE - DO NOT DELETE
# print(json.dumps(response_dict, indent=2))
#
# #
# # new_cell = ss.models.Cell()
# # new_cell.column_id = 7950289333446532
# # new_cell.value = 'Complete'
# # new_cell.format = ",,,,,,,,,30,30,,,,,"
# #
# #
# # new_row = ss.models.Row()
# # new_row.id = row_id
# # new_row.cells.append(new_cell)
# #
# # # Update rows
# # response = ss.Sheets.update_rows(sheet_id, [new_row])
# # response_dict = response.to_dict()
# #
# # # RESPONSE DEBUG CODE - DO NOT DELETE
# # print(json.dumps(response_dict, indent=2))
