from ta_pov.models import *
import smartsheet
import json
from datetime import datetime, date, time
import time
import pytz
# Application Passwords kept here
from ta_pov import my_secrets
from ta_pov.smartsheet_basic_functions import *

# Smartsheet Config settings
ss_config = dict(
    SS_TOKEN = my_secrets.passwords["SS_TOKEN"]
)


def create_ss_from_sql():
    # # Run a Query to get the col names
    sql= "SHOW COLUMNS FROM povbot.tblPovs "
    cols = db.engine.execute(sql)

    new_col_list = []
    primary_col = True

    for col in cols:
        # If this column is first make it the required SS primary column
        # else create they type of SS column we need (TEXT_NUMBER,DATE,CHECKBOX etc)
        if col.Type == 'datetime':
            new_col_list.append({'title': col.Field, 'primary': primary_col, 'type': 'DATE'})
        else:
            new_col_list.append({'title': col.Field, 'primary': primary_col, 'type': 'TEXT_NUMBER'})

        primary_col = False

    return new_col_list


def load_sql_rows(my_cols):
    my_rows = []
    this_row = []

    # Retrieve the SQL Data
    povs = ta_povs.query.order_by(ta_povs.company_name).all()
    row_count = 0

    for pov in povs:
        row_count += 1

        for column in my_cols:
            column_name = column['title']
            column_id = column['id']

            row_value = eval("pov."+column_name)

            # Change None type to something else
            if row_value is None:
                row_value = ""

            # Change datetime to string
            if isinstance(row_value, datetime):
                row_value = row_value.strftime("%A, %d. %B %Y %I:%M%p")

            this_row.append({'column_id':column_id, 'value': row_value, 'strict': False})

        my_rows.append(this_row)

        this_row = []

    print('my rows', my_rows)
    print(len(my_rows))
    return my_rows

def create_status_cols(my_ss):
    my_cols = []  # List of SS API formatted columns
    my_col_id_map = []  # List of (col_id,SQL col nam,SS col name, Data Type)

    # Loop through the SS model and build the new SS
    for x in my_ss:
        my_col_id_map.append(['', x[0], x[1], x[3]])

        # Create each column record for SS from the SS_Model object
        # Adjust accordingly if the 'option' property exists
        if x[4] == '':
            my_cols.append({'title': x[1], 'primary': x[2], 'type': x[3]})
        else:
            my_cols.append({'title': x[1], 'primary': x[2], 'type': x[3], 'options': x[4]})

    sheet_dict = ss_create_sheet(my_ss.ss, 'Tetration On-Demand POV Status', my_cols)

    # Retrieve each SS column 'id' from the 'columns' dict of the SS response
    col_data_dict = sheet_dict.get('result', {}).get('columns', {})

    # Update my_col_id_map with the col ids
    x = 0
    for col_record in col_data_dict:
        my_col_id_map[x][0] = col_record['id']
        x += 1

    my_ss.my_col_id_map = my_col_id_map

    return my_cols




def create_status_sheet_old(ss_model):
    ss = ss_model.ss
    sheet_name = ss_model.status_sheet_name
    my_sheet_build = []  # List of SS API formatted columns
    my_col_details = []  # List of (col_id,SQL col nam,SS col name, Data Type)

    # Loop through the SS model and build the new SS
    for x in ss_model:
        my_col_details.append(['', x[0], x[1], x[3]])

        # Create each column record for SS from the SS_Model object
        # Adjust accordingly if the 'option' property exists
        if x[4] == '':
            my_sheet_build.append({'title': x[1], 'primary': x[2], 'type': x[3]})
        else:
            my_sheet_build.append({'title': x[1], 'primary': x[2], 'type': x[3], 'options': x[4]})

    # All columns are now defined
    # Send off to Smartsheets to create the sheet
    sheet_spec = ss.models.Sheet({'name': sheet_name, 'columns': my_sheet_build})
    response = ss.Home.create_sheet(sheet_spec)

    # Create a dict of the response json data
    response_dict = response.to_dict()

    # Retrieve the sheet id & sheet url from the 'result' dict of the SS response
    result_dict = response_dict.get('result', {})
    ss_model.status_sheet_id = result_dict['id']
    ss_model.status_sheet_url = result_dict['permalink']

    # Retrieve each SS column 'id' from the 'columns' dict of the SS response
    col_data_dict = response_dict.get('result', {}).get('columns', {})

    # Update my_col_details with the col ids
    x = 0
    for col_record in col_data_dict:
        my_col_details[x][0] = col_record['id']
        x += 1
    ss_model.my_col_details = my_col_details

    print('status sheet creation ', response.message)
    return


def add_rows_test(raw_rows):
    # ss = ss_model.ss

    # Get Raw Data SS rows
    # raw_data_sheet_id = ss_model.raw_data_sheet['id']

    # tmp = ss.Sheets.get_sheet(raw_data_sheet_id, include='rowIds')
    # raw_data_sheet_dict = tmp.to_dict()
    #
    # raw_rows = raw_data_sheet_dict.get('rows', {})
    # raw_data_col_dict = ss_model.raw_data_col_dict # dict to loo up col ids

    # Newly created status sheet col-ids
    # my_col_details = ss_model.my_col_details

    for row in raw_rows:
        cells = row['cells']
        print('Processing Row Numbber: ', row['rowNumber'])
        for cell in cells:
            if 'value' in cell:
                print(cell['columnId'], cell['value'])
            else:
                print(cell['columnId'],)
        exit()

    # loop over each MySql POV record
    for pov in ss_model.povs:
        row_next = ss.models.Row()
        pov_status = ''
        row_next.to_top = True

        # Calculate the number of POV days
        pov_days = str(pov.end_date - pov.start_date)
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
            # row_next.cells.append(row_dict)


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
    status_sheet_name = ss_model.status_sheet_name
    template_id = ss_model.template_id
    response = ss.Home.create_sheet_from_template(
        ss.models.Sheet({'name': status_sheet_name, 'from_id': template_id}))
    status_sheet = response.result
    status_sheet_id = status_sheet.id

    bot_update_id = ss_model.status_sheet_id  # Working POV BOT sheet

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
                'sheet_id': status_sheet_id})}))

    return











# ****************



def create_sheet_old(my_ss_model):
    ss = my_ss_model.ss
    sheet_name = my_ss_model.raw_data_sheet_name
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

def add_rows_old(ss_model):
    ss = ss_model.ss
    my_col_details = ss_model.my_col_details
    raw_data_sheet_id = ss_model.raw_data_sheet_id
    raw_data_col_dict = ss_model.raw_data_col_dict
    sheet_id = ss_model.status_sheet_id

    # Get the MySQL data
    ss_model.load_sql()

    # loop over each MySql POV record
    for pov in ss_model.povs:
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
    status_sheet_name = ss_model.status_sheet_name
    template_id = ss_model.template_id
    response = ss.Home.create_sheet_from_template(
        ss.models.Sheet({'name': status_sheet_name, 'from_id': template_id}))
    status_sheet = response.result
    status_sheet_id = status_sheet.id

    bot_update_id = ss_model.status_sheet_id  # Working POV BOT sheet

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
                'sheet_id': status_sheet_id})}))

    return




def sheet_details(ss_model):
    ss = ss_model.ss
    ss_model.raw_data_sheet_id = 'None'
    ss_model.template_id = 'None'
    ss_model.status_sheet_id = 'None'

    # Find my Sheet ID
    response = ss.Sheets.list_sheets(include_all=True)
    sheets = response.data

    for sheet in sheets:
        if sheet.name == ss_model.raw_data_sheet_name:
            ss_model.raw_data_sheet_id = sheet.id

        if sheet.name == ss_model.status_sheet_name:
            ss_model.status_sheet_id = sheet.id
            ss_model.status_sheet_url = sheet.permalink
            ss_model.total_rows = sheet.total_row_count
            ss_model.last_modified = sheet.modified_at.astimezone(pytz.timezone('US/Eastern'))

    # Look for the Template ID
    response = ss.Templates.list_user_created_templates()
    templates = response.data
    for template in templates:
        if template.name == ss_model.template_name:
            ss_model.template_id = template.id

    return


if __name__ == "__main__":
    # Declare my_ss
    my_ss = SS_Model_r1()
    
    # Get Current Sheet Info
    my_ss.raw_data_sheet = ss_get_sheet(my_ss.ss, 'Tetration On-Demand POV Raw Data')
    my_ss.status_sheet = ss_get_sheet(my_ss.ss, 'Tetration On-Demand POV Status')
    my_ss.template_sheet = ss_get_template(my_ss.ss, 'Tetration On-Demand POV Status-Template')

    # Delete any existing sheets (if any)
    if 'id' in my_ss.raw_data_sheet:
        ss_delete_sheet(my_ss.ss, my_ss.raw_data_sheet['id'])
    if 'id' in my_ss.status_sheet:
        ss_delete_sheet(my_ss.ss, my_ss.status_sheet['id'])

    # Build the columns and create a new raw SS from the SQL Model
    my_raw_cols = create_ss_from_sql()
    ss_create_sheet(my_ss.ss, 'Tetration On-Demand POV Raw Data', my_raw_cols)

    # Get the sheet details of the newly created SS for Raw Data
    my_ss.raw_data_sheet = ss_get_sheet(my_ss.ss, 'Tetration On-Demand POV Raw Data')

    # Get all the col_ids and load the new raw SQL data
    col_ids  = ss_get_col_data(my_ss.ss, my_ss.raw_data_sheet['id'])

    my_rows = load_sql_rows(col_ids)
    ss_add_rows(my_ss.ss, my_ss.raw_data_sheet['id'], my_rows)


    # WORK IN PROGRESS
    #
    #
    # Make a working copy of the new raw sql data
    # do a simple copy of the raw sheet to a working sheet
    response = my_ss.ss.Sheets.copy_sheet(my_ss.raw_data_sheet['id'],  # sheet_id
                    my_ss.ss.models.ContainerDestination(
                        {'destination_type': 'home', 'new_name': 'tmp_pov_junk'}), include='data')
    tmp_sheet_id = response.result.id
    tmp_sheet_rows = ss_get_row_data(my_ss.ss, tmp_sheet_id)
    tmp_sheet_cols = ss_get_col_data(my_ss.ss, tmp_sheet_id)

    # print(tmp_sheet_id)
    # print(tmp_sheet_cols)
    # print(tmp_sheet_rows)

    #
    # Create a new empty Status Sheet in SS based on the model
    #
    my_status_cols = create_status_cols(my_ss)
    # ss_create_sheet(my_ss.ss, 'Tetration On-Demand POV Status', my_status_cols)
    my_ss.status_sheet = ss_get_sheet(my_ss.ss, 'Tetration On-Demand POV Status')

    exit()








    # Gather all the row id's from the working file
    # Then Copy them over to the final sheet
    # raw_rows = ss_get_row_data(my_ss.ss, my_ss.raw_data_sheet['id'])
    # row_ids = []
    # src_sheet_id = my_ss.raw_data_sheet['id']
    # dst_sheet_id = my_ss.status_sheet['id']
    # for row in raw_rows:
    #     row_ids.append(row['id'])
    #
    # print(row_ids)
    # print(src_sheet_id)
    # print(dst_sheet_id)


    response = my_ss.ss.Sheets.copy_rows(
                    src_sheet_id,  # sheet_id of rows to be copied
                    my_ss.ss.models.CopyOrMoveRowDirective({
                        'row_ids': row_ids,
                        'to': my_ss.ss.models.CopyOrMoveRowDestination({
                                'sheet_id': dst_sheet_id})}))


    # Get raw data rows
    raw_rows = ss_get_row_data(my_ss.ss, my_ss.raw_data_sheet['id'])

    for row in rows:
        print (row['cells'])

    exit()
    add_rows_test(raw_rows)
