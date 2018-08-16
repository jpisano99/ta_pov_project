from ta_pov.Ssheet_class import Ssheet
from ta_pov.models import *
from datetime import datetime
from ta_pov.smartsheet_basic_functions import *
from ta_pov.ss_mapping import sql_to_ss

ss_config = dict(
    SS_TOKEN = my_secrets.passwords["SS_TOKEN"]
)


def create_cols_from_sql():
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


def create_status_cols():
    my_cols = []  # List of SS API formatted columns
    # my_col_details = []  # List of (col_id,SQL col nam,SS col name, Data Type)

    for x in sql_to_ss:
        # my_col_details.append(('', x[0], x[1], x[3]))

        # Create each column record for SS from the SS_Model object
        # Adjust accordingly if the 'option' (x[4]) property exists
        if x[4] == '':
            my_cols.append({'title': x[1], 'primary': x[2], 'type': x[3]})
        else:
            my_cols.append({'title': x[1], 'primary': x[2], 'type': x[3], 'options': x[4]})

    return my_cols


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

            this_row.append({'column_id': column_id, 'value': row_value, 'strict': False})

        my_rows.append(this_row)

        this_row = []
    return my_rows


if __name__ == "__main__":
    ss_token = ss_config['SS_TOKEN']
    ss = smartsheet.Smartsheet(ss_token)

    # Clean up and/or archive any existing SmartSheets
    ss_delete_sheet(ss, 'Tetration On-Demand POV Raw Data')
    ss_delete_sheet(ss, 'Tetration On-Demand POV Status')

    #
    # Connect to mySQL db and pull raw BOT data into SmartSheets
    #

    # Get the column formats from mySQL & build an empty sheet
    my_cols = create_cols_from_sql()
    ss_create_sheet(ss, 'Tetration On-Demand POV Raw Data', my_cols)

    # Create a SmartSheet object for Raw data
    my_ss = Ssheet('Tetration On-Demand POV Raw Data')

    # Get the row data from mySQL and add to my_ss object
    my_rows = load_sql_rows(my_ss.columns)
    my_ss.add_rows(my_rows)
    my_ss.refresh()

    #
    # All data has now be loaded from mySQL
    #

    # Get the column formats to create the POV Status sheet
    my_cols = create_status_cols()
    ss_create_sheet(ss, 'Tetration On-Demand POV Status', my_cols)
    my_status = Ssheet('Tetration On-Demand POV Status')

    # Main Loop to go over BOT data
    col_id_idx = my_ss.col_id_idx
    raw_rows = my_ss.rows

    for row in raw_rows:
        print()
        print('Row: ', row['rowNumber'], row['id'])
        for cell in row['cells']:
            cell_val = cell['value'] if 'value' in cell else ''
            #
            # Now WHAT ? ! :)
            # Keep this cell data ?
            # Rename it ?
            # Modify it ?
            print('    ', col_id_idx[cell['columnId']], cell_val)

    exit()





