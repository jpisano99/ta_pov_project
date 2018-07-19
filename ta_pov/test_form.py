import smartsheet
import json

# Application Passwords kept here
from ta_pov import my_secrets

# Smartsheet Config settings
ss_config = dict(SS_TOKEN = my_secrets.passwords["SS_TOKEN"])
ss_token = ss_config['SS_TOKEN']
ss = smartsheet.Smartsheet(ss_token)


def get_sheet_id(sheet_name):
    # Find Sheet ID for "sheet_name"
    response = ss.Sheets.list_sheets(include_all=True)
    sheets = response.data
    for sheet in sheets:
        if sheet.name == sheet_name:
            sheet_id = sheet.id

    return(sheet_id)


def get_sheet_info(sheet_id):
    # Grab the entire sheet object from 'sheet_id'
    sheet = ss.Sheets.get_sheet(sheet_id, include='rowIds')

    # GET SHEET RESPONSE DEBUG CODE - DO NOT DELETE
    # sheet_dict = sheet.to_dict()
    # print(json.dumps(sheet_dict, indent=2))
    # print(dir(sheet))
    # print(type(sheet))
    return(sheet)

def get_col_id(sheet, col_name):
    # Get the col id from 'sheet' object with 'col_name'
    columns = sheet.columns
    col_id_dict = {}
    for column in columns:
        col_id_dict[column.title] = column.id
        if column.title == col_name:
            customer_col_id = column.id

    return (customer_col_id)


def get_customer_list(sheet, customer_col_id):
    # Get all the rows from the 'sheet' object
    # and pull out the customer names

    sheet_dict = sheet.to_dict()
    rows = sheet_dict.get('rows', {})
    customer_list = []
    for row in rows:
        cells = row['cells']
        row_num = row['rowNumber']
        for cell in cells:
            if cell['columnId'] == customer_col_id:
                customer_list.append(cell['displayValue'])

    # Sort the Customer List
    customer_list.sort()
    return (customer_list)


def update_pov_sheet(sheet_id, col_id, customer_list):
    # Update the Customer Pick List from the Forecast Customers
    column_spec = ss.models.Column({
      'type': 'PICKLIST',
      'options': customer_list,
    })

    # Update column & load the pick list in the Customer Name column
    response = ss.Sheets.update_column(sheet_id, col_id, column_spec)
    updated_column = response.result
    return()


if __name__ == "__main__":
    # Get the customers from the segment forecast sheet
    sheet_name = 'US Commercial Tetration Forecast'
    col_name = 'Customer'
    sheet_id = get_sheet_id(sheet_name)
    sheet = get_sheet_info(sheet_id)
    col_id = get_col_id(sheet, col_name)
    customer_list = get_customer_list(sheet, col_id)

    # Update the POV BOT sheet withCustomer Name pick list
    # Using customer list from the segment forecast
    sheet_name = 'Tetration POV On-Demand POV Status-Test'
    col_name = 'Customer Name'
    sheet_id = get_sheet_id(sheet_name)
    sheet = get_sheet_info(sheet_id)
    col_id = get_col_id(sheet, col_name)
    update_pov_sheet(sheet_id, col_id, customer_list)



