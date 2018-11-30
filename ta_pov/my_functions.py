from ta_pov.Ssheet_class import Ssheet
from ta_pov.models import *
from datetime import datetime
from ta_pov.smartsheet_basic_functions import *
from ta_pov.ss_mapping import sql_to_ss

ss_config = dict(
    SS_TOKEN=my_secrets.passwords["SS_TOKEN"]
)


def create_cols_from_sql():
    # # Run a Query to get the col names
    sql = "SHOW COLUMNS FROM povbot.tblPovs "
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

            row_value = eval("pov." + column_name)

            # Change None type to something else
            if row_value is None:
                row_value = ""

            # Change datetime to string
            if isinstance(row_value, datetime):
                # row_value = row_value.strftime("%A, %d. %B %Y %I:%M%p")
                row_value = row_value.strftime("%m/%d/%y")

            this_row.append({'column_id': column_id, 'value': row_value, 'strict': False})

        my_rows.append(this_row)

        this_row = []
    return my_rows


def test_this(ss):
    # Create a SmartSheet object for Raw data
    my_raw_ss = Ssheet('Tetration On-Demand POV Raw Data')
    my_status = Ssheet('Tetration On-Demand POV WORKING')

    # Build a fast lookup dict from the sql_to_ss mapping structure
    map_lookup = {}

    for x in sql_to_ss:
        # x[0] = the raw col
        map_lookup[x[0]] = x[1]

    #
    # Main Loop to loop over BOT data
    # and build status rows to be created
    col_id_idx = my_raw_ss.col_id_idx
    raw_rows = my_raw_ss.rows
    new_ss_rows = []

    for row in raw_rows:
        print()
        print('Processing Raw Row: ', row['rowNumber'], row['id'])
        this_ss_row = []
        this_row_dict = {}
        for cell in row['cells']:
            raw_cell_val = cell['value'] if 'value' in cell else ''
            raw_col_name = col_id_idx[cell['columnId']]
            this_row_dict[raw_col_name] = raw_cell_val

            # Determine how this raw_col maps to the final POV status
            # Build a row record
            if raw_col_name in map_lookup.keys():
                status_col_name = map_lookup[raw_col_name]
                status_col_id = my_status.col_name_idx[status_col_name]
                this_ss_row.append({'column_id': status_col_id, 'value': raw_cell_val, 'strict': False})
            else:
                # Does Nothing
                pass

        print('Raw Row: ', this_row_dict)
        print('SS formatted row: ', this_ss_row)

        # Append this_row to the collection of new_rows
        new_ss_rows.append(this_ss_row)

    return


if __name__ == "__main__":
    ss_token = ss_config['SS_TOKEN']
    ss = smartsheet.Smartsheet(ss_token)

    #test_this(ss)

    # exit()
    # Clean up and/or archive any existing SmartSheets
    ss_delete_sheet(ss, 'Tetration On-Demand POV Raw Data')
    ss_delete_sheet(ss, 'Tetration On-Demand POV WORKING')
    ss_delete_sheet(ss, 'Tetration On-Demand POV Status')

    #
    # Connect to mySQL db and pull raw BOT data into SmartSheets
    #

    # Get the column formats from mySQL & build an empty sheet
    my_cols = create_cols_from_sql()
    ss_create_sheet(ss, 'Tetration On-Demand POV Raw Data', my_cols)

    # Create a SmartSheet object for Raw data
    my_raw_ss = Ssheet('Tetration On-Demand POV Raw Data')

    # Get the row data from mySQL and add to my_raw_ss object
    my_rows = load_sql_rows(my_raw_ss.columns)
    my_raw_ss.add_rows(my_rows)
    my_raw_ss.refresh()

    #
    # All data has now be loaded from mySQL
    #
    # exit()
    # Get the column formats to create the POV WORKING sheet
    my_cols = create_status_cols()
    ss_create_sheet(ss, 'Tetration On-Demand POV WORKING', my_cols)
    my_status = Ssheet('Tetration On-Demand POV WORKING')

    # Build a fast lookup dict from the sql_to_ss mapping structure
    map_lookup = {}
    for x in sql_to_ss:
        # x[0] = the raw col
        map_lookup[x[0]] = x[1]

    #
    # Main Loop to loop over BOT data
    # and build status rows to be created
    col_id_idx = my_raw_ss.col_id_idx
    raw_rows = my_raw_ss.rows
    new_rows = []
    for row in raw_rows:
        print()
        print('Raw Row: ', row['rowNumber'], row['id'])
        this_row = []
        for cell in row['cells']:
            raw_cell_val = cell['value'] if 'value' in cell else ''
            raw_col_name = col_id_idx[cell['columnId']]

            # Determine how this raw_col maps to the final POV status
            # Build a row record
            if raw_col_name in map_lookup.keys():
                status_col_name = map_lookup[raw_col_name]
                status_col_id = my_status.col_name_idx[status_col_name]
                this_row.append({'column_id': status_col_id, 'value': raw_cell_val, 'strict': False})
            else:
                pass
                # print('Skipping: ', raw_col_name)
        # Append this_row to the collection of new_rows
        new_rows.append(this_row)

    # Send the list of the new_rows off to be added
    # To the final POV status sheet
    my_status.add_rows(new_rows)
    my_status.refresh()

    # Create a new blank POV Update from the Template
    template_sheet_id = ss_get_template(ss, 'Tetration On-Demand POV Status-Template-Rev1')
    response = ss.Home.create_sheet_from_template(
        ss.models.Sheet({'name': 'Tetration On-Demand POV Status', 'from_id': template_sheet_id['id']}))

    my_final_ss = Ssheet('Tetration On-Demand POV Status')

    # Gather all the row id's from the working file
    # Then Copy them over to the final status sheet
    status_update_rows = []
    for row in my_status.rows:
        status_update_rows.append(row['id'])

    print(status_update_rows)

    response = ss.Sheets.copy_rows(
        my_status.id,  # sheet_id of rows to be copied
        ss.models.CopyOrMoveRowDirective({
            'row_ids': status_update_rows,
            'to': ss.models.CopyOrMoveRowDestination({
                'sheet_id': my_final_ss.id})}))

    exit()
