from ta_pov.models import *
import smartsheet
import json
from datetime import datetime, date, time
import pytz
# Application Passwords kept here
from ta_pov import my_secrets

# Smartsheet Config settings
ss_config = dict(
    SS_TOKEN = my_secrets.passwords["SS_TOKEN"]
)


def delete_sheet(my_ss_model):
    ss = my_ss_model.ss

    if my_ss_model.sheet_id != 'None':
        response = ss.Sheets.delete_sheet(my_ss_model.sheet_id)

    return


def create_sheet(my_ss_model):
    ss = my_ss_model.ss
    sheet_name = my_ss_model.sheet_name
    my_sheet_build = []  # List of SS API formatted columns
    my_col_details = []  # List of (col_id,SQL col nam,SS col name, Data Type)

    for x in my_ss_model:
        my_col_details.append(('', x[0], x[1], x[3]))

        # Create each column record for SS from the SS_Model object
        # Adjust accordingly if the 'option' property exists
        if x[4] == '':
            my_sheet_build.append({'title': x[1], 'primary': x[2], 'type': x[3]})
        else:
            my_sheet_build.append({'title': x[1], 'primary': x[2], 'type': x[3], 'options': x[4]})

    # my_sheet_build.append({'title': 'POV Days', 'primary': False, 'type': 'TEXT_NUMBER', 'formula': '=[End Date] - [Start Date]'})

    # All columns are now defined
    # Send off to Smartsheets to create the sheet
    sheet_spec = ss.models.Sheet({'name': sheet_name, 'columns': my_sheet_build})
    response = ss.Home.create_sheet(sheet_spec)

    # Did we create successfully ?
    print("Sheet Creation: ", response.message)

    # Create a dict of the response data
    response_dict = response.to_dict()

    # RESPONSE DEBUG CODE - DO NOT DELETE
    # print(json.dumps(resp_dict, indent=2))
    # exit()

    # Retrieve the sheet id & sheet url from the 'result' dict of the SS response
    result_dict = response_dict.get('result', {})
    sheet_id = result_dict['id']
    sheet_url = result_dict['permalink']

    # Retrieve each SS column 'id' from the 'columns' dict of the SS response
    col_data_dict = response_dict.get('result', {}).get('columns', {})

    # Crete a dict to lookup SS col ids by SS col_name (SS_column_name:SS_column_id)
    col_id_lookup = {}

    for col_record in col_data_dict:
        col_id_lookup[col_record['title']] = col_record['id']

    # Add SS col ids to the my_col_details list
    # Build by using a tmp_list to insert the cold ids
    tmp_list = []
    for x in my_col_details:
        # Use the Smartsheet col name x[2] to look up the col id
        # Update the my_col_details list to include col id
        col_id = col_id_lookup[x[2]]
        tmp_list.append((col_id, x[1], x[2], x[3]))

    my_col_details = tmp_list

    # my_col_details now has everything we need to Add Rows
    my_ss_model.my_col_details = my_col_details

    return

def add_rows(my_ss_model):
    ss = my_ss_model.ss
    my_col_details = my_ss_model.my_col_details
    sheet_id = my_ss_model.sheet_id

    # Get the MySQL data
    my_ss_model.load_sql()

    # loop over each MySql POV record
    for pov in my_ss_model.povs:
        row_next = ss.models.Row()
        pov_status = ''
        row_next.to_top = True

        # Calculate the number of POV days
        pov_days = str(pov.end_date -  pov.start_date)
        pov_days = pov_days[:pov_days.find('d')] + 'Days'

        # Create the POV Status tag
        if pov.active == 1 and pov.extended == 1:
            pov_status = 'Active - Extended'
        elif pov.active == 1:
            pov_status = 'Active'
        elif pov.deleted == 1:
            pov_status = 'Deleted'

        # Loop Across all columns in this row
        for x in my_col_details:
            col_id = x[0]
            col_sql_name = x[1]
            col_ss_name = x[2]
            col_type = x[3]

            if col_sql_name == 'CALCULATED':
                row_value = pov_days
            else:
                row_value = eval("pov." + col_sql_name)

            # print (col_sql_name,row_value,type(row_value))
            # Change None type to something else since SS will throw
            # a error on a 'None' row value
            if row_value is None:
                row_value = ""

            if col_ss_name == 'Active':
                row_value = pov_status

            # Change datetime to string
            if isinstance(row_value, datetime):
                row_value = row_value.strftime("%m/%d/%y")

            # Apply some row level formatting
            row_dict = {'column_id': col_id, 'value': row_value, 'strict': False}
            row_next.cells.append(row_dict)

        response = ss.Sheets.add_rows(sheet_id, [row_next])

    #
    #  Clean up and do some formatting
    #

    # Delete columns extended & deleted
    for x in my_col_details:
        if x[2] == 'Extended':
            col_id = x[0]
    ss.Sheets.delete_column(sheet_id, col_id)

    for x in my_col_details:
        if x[2] == 'Deleted':
            col_id = x[0]
    ss.Sheets.delete_column(sheet_id, col_id)

    # Rename Active to POV Status
    for x in my_col_details:
        if x[2] == 'Active':
            col_id = x[0]

    col_spec = ss.models.Column({'title': 'POV Status'})
    response = ss.Sheets.update_column(sheet_id, col_id, col_spec)

    # Create a new blank POV Update from the Template
    new_sheet_name = 'Tetration On-Demand POV Status'
    template_name = 'Tetration On-Demand POV Status-Template'
    template_id = 6937344860284804  # TA POV Template ID
    response = ss.Home.create_sheet_from_template(
        ss.models.Sheet({'name': new_sheet_name, 'from_id': template_id}))
    new_sheet = response.result
    new_sheet_id = new_sheet.id

    bot_update_id = my_ss_model.sheet_id  # Working POV BOT sheet

    # Gather all the row id's from the working file
    # Then Copy them over to the final sheet
    bot_update_rows = []
    sheet = ss.Sheets.get_sheet(bot_update_id)
    for row in sheet.rows:
        bot_update_rows.append(row.id)

    response = ss.Sheets.copy_rows(
        bot_update_id,  # sheet_id of rows to be copied
        ss.models.CopyOrMoveRowDirective({
            'row_ids': bot_update_rows,
            'to': ss.models.CopyOrMoveRowDestination({
                'sheet_id': new_sheet_id})}))

    return


def sheet_details(my_ss_model):
    ss = my_ss_model.ss
    sheet_name = my_ss_model.sheet_name
    my_ss_model.sheet_id = 'None'

    # Find my Sheet ID
    response = ss.Sheets.list_sheets(include_all=True)
    sheets = response.data

    for sheet in sheets:
        if sheet.name == sheet_name:
            my_ss_model.sheet_id = sheet.id
            my_ss_model.sheet_url = sheet.permalink
            my_ss_model.total_rows = sheet.total_row_count
            my_ss_model.last_modified = sheet.modified_at.astimezone(pytz.timezone('US/Eastern'))

    return


if __name__ == "__main__":
    # Build the Sheet
    my_ss_model = SS_Model()
    my_ss_model.sheet_name = 'Tetration POV Raw BOT Data'

    # # Get existing sheet info (if any)
    sheet_details(my_ss_model)

    # Delete existing sheet_name (if any)
    delete_sheet(my_ss_model)

    # Recreate sheet and get new sheet details
    create_sheet(my_ss_model)
    sheet_details(my_ss_model)

    # # Add new rows
    add_rows(my_ss_model)


