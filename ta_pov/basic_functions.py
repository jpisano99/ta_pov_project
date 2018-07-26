def get_sheet(ss, sheet_name):
    # Get Sheet meta-data
    response = ss.Sheets.list_sheets(include_all=True)
    sheets = response.data
    sheet_info_dict = {}
    for sheet in sheets:
        if sheet.name == sheet_name:
            sheet_info_dict = sheet.to_dict()
    return sheet_info_dict


def create_sheet(ss, sheet_name, col_dict):
    # All columns are now defined
    # Send off to Smartsheets to create the sheet
    sheet_spec = ss.models.Sheet({'name': sheet_name, 'columns': col_dict})
    response = ss.Home.create_sheet(sheet_spec)

    # Create a dict of the response json data
    sheet_dict = response.to_dict()
    return sheet_dict


def delete_sheet(ss, sheet_id):
    response = ss.Sheets.delete_sheet(sheet_id)
    return response


def get_template(ss, template_name):
    # Get template meta-data
    response = ss.Templates.list_user_created_templates()
    templates = response.data
    template_info_dict = {}
    for template in templates:
        if template.name == template_name:
            template_info_dict = template.to_dict()
    return template_info_dict


def get_col_data(ss, sheet_id):
    # Get column data from sheet_id
    tmp = ss.Sheets.get_sheet(sheet_id, include='rowIds')
    sheet_dict = tmp.to_dict()
    columns = sheet_dict.get('columns', {})
    return columns


def get_row_data(ss, sheet_id):
    # Get row data from sheet_id
    tmp = ss.Sheets.get_sheet(sheet_id, include='rowIds')
    sheet_dict = tmp.to_dict()
    rows = sheet_dict.get('rows', {})
    return rows


def del_column(ss, sheet_id, col_id):
    pass
    return


def add_column(ss, sheet_id, col_id, col_dict):
    pass
    return


def del_row(ss, sheet_id, my_rows):
    pass
    return


def add_row(ss, sheet_id, my_rows):
    #
    # my_rows is a list of rows to be added
    # [ [{"strict": false, "columnId": 1, "value": "jim"}] }
    #
    rows_to_add = []
    for row in my_rows:
        # Create a row object
        row_next = ss.models.Row()
        row_next.to_top = True
        for cell in row:
            # Gather all the cells in __this__ row
            row_next.cells.append(cell)
            print('row', row_next)

        # Add to the list of row objects to send to SS
        rows_to_add.append(row_next)

    # Send to SS to ADD the rows
    response = ss.Sheets.add_rows(sheet_id, rows_to_add)
    return


def change_cell(ss, sheet_id, row_id, col_id, cell_dict):
    pass
    return
