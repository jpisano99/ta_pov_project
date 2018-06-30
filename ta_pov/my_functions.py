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

def delete_sheet(sheet_dict):
    ss_token=ss_config['SS_TOKEN']
    ss = smartsheet.Smartsheet(ss_token)

    if sheet_dict['sheet_id'] != 'Not Found':
        sheet_id = sheet_dict['sheet_id']
        response = ss.Sheets.delete_sheet(sheet_id)       # sheet_id


def create_sheet(sheet_name):
    ss_token=ss_config['SS_TOKEN']
    ss = smartsheet.Smartsheet(ss_token)

    # # Run a Query to get the col names
    sql= "SHOW COLUMNS FROM povbot.tblPovs "
    cols = db.engine.execute(sql)

    new_col_list=[]
    primary_col = True

    for col in cols:
        # If this column is first make it the required SS primary column
        # else create they type of SS column we need (TEXT_NUMBER,DATE,CHECKBOX etc)
        if col.Type == 'datetime':
            new_col_list.append({'title': col.Field, 'primary': primary_col, 'type': 'DATE'})
        else:
            new_col_list.append({'title': col.Field, 'primary': primary_col, 'type': 'TEXT_NUMBER'})

        primary_col = False

    sheet_spec = ss.models.Sheet({'name': sheet_name, 'columns': new_col_list})
    response = ss.Home.create_sheet(sheet_spec)

def add_rows(sheet_dict):
    ss_token=ss_config['SS_TOKEN']
    ss = smartsheet.Smartsheet(ss_token)

    sheet_id= sheet_dict['sheet_id']   # "test" Sheet ID
    col_count = sheet_dict['col_count']

    # Build the SQL query from tblPovs
    povs = ta_povs.query.order_by(ta_povs.company_name).all()

    for pov in povs:
        row_next = ss.models.Row()
        row_next.to_top = True

        for x in range(1, col_count+1):
            col_id_key = 'col_id_' + str(x)
            col_name_key = 'col_name_' + str(x)

            col_id = sheet_dict[col_id_key]
            col_name = sheet_dict[col_name_key]
            row_value = eval("pov."+col_name)

            # Change None type to something else
            if row_value is None:
                row_value = ""

            # Change datetime to string
            if isinstance(row_value, datetime):
                row_value = row_value.strftime("%A, %d. %B %Y %I:%M%p")

            row_dict = { 'column_id':col_id ,'value': row_value, 'strict': False}
            row_next.cells.append(row_dict)

        response = ss.Sheets.add_rows(sheet_id, [row_next])

    # DEBUG CODE - DO NOT DELETE
    # print("Response: ",response.message)
    # resp_dict = response.to_dict()
    # print(json.dumps(resp_dict, indent=2))
    # exit()

def sheet_details(sheet_name):
    ss_token=ss_config['SS_TOKEN']
    ss = smartsheet.Smartsheet(ss_token)
    sheet_dict = {}

    # Find my Sheet ID
    response = ss.Sheets.list_sheets(include_all=True)
    sheets = response.data

    for sheet in sheets:
        if sheet.name == sheet_name:
            sheet_dict['sheet_name'] = sheet.name
            sheet_dict['sheet_id'] = sheet.id

    # If we found "sheet_name" find columns
    if 'sheet_id' in sheet_dict.keys():
        sheet = ss.Sheets.get_sheet(sheet_dict['sheet_id'])
        sheet_dict['row_count'] = sheet.total_row_count
        sheet_dict['sheet_url']= sheet.permalink
        sheet_dict['modified_at'] = sheet.modified_at.astimezone(pytz.timezone('US/Eastern'))

        columns = sheet.columns

        col_cnt = 1
        for column in columns:
            #print(sheet_dict['sheet_name'], column.title, column.id)
            sheet_dict['col_name_'+str(col_cnt)] = column.title
            sheet_dict['col_id_'+str(col_cnt)] = column.id
            sheet_dict['col_count']=(col_cnt)
            col_cnt += 1
    else:
        sheet_dict['sheet_id'] = "Not Found"

    return sheet_dict

if __name__ == "__main__":
    pass

    sheet_name = 'POV BOT Status'
    # # Get existing sheet info (if any)
    sheet_dict = sheet_details(sheet_name)
    print(sheet_dict['sheet_url'])

    #
    # # Delete existing sheet_name
    # delete_sheet(sheet_dict)
    #
    # # Recreate sheet and create new dict
    # create_sheet(sheet_name)
    # sheet_dict = sheet_details(sheet_name)
    #
    # # Add new rows
    # add_rows(sheet_dict)
