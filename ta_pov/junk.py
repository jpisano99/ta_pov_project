from ta_pov.models import *
import smartsheet
import json
from datetime import datetime, date, time
import pytz

# Application Passwords kept here
from ta_pov import my_secrets



class SS_Model:

    def __init__(self):
        self.index = -1
        self.sql_to_ss = [['id', 'POV ID', True, 'TEXT_NUMBER',''],
                    ['cisco_owner', 'POV Owner Email', False, 'TEXT_NUMBER',''],
                    ['cisco_owner_name', 'POV Owner Name', False, 'TEXT_NUMBER',''],
                    ['company_name', 'Customer Name',False, 'TEXT_NUMBER',''],
                    ['customer_first_name', 'Customer First Name', False, 'TEXT_NUMBER',''],
                    ['customer_last_name', 'Customer Last Name', False, 'TEXT_NUMBER',''],
                    ['customer_email', 'Customer Email', False, 'TEXT_NUMBER',''],
                    ['tenant_name', 'Tenant Name', False, 'TEXT_NUMBER',''],
                    ['start_date', 'Start Date', False, 'DATE',''],
                    ['end_date', 'End Date',False, 'DATE',''],
                    ['deleted_date', 'Deleted Date', False, 'DATE',''],
                    ['active', 'Active',False, 'PICKLIST', ['Yes','No']],
                    ['extended', 'Extended',False, 'PICKLIST',['Yes','No']],
                    ['deleted', 'Deleted', False, 'PICKLIST', ['Yes','No']]]

    def load_sql(self):
        # Build the SQL query from tblPovs
        self.povs = ta_povs.query.order_by(ta_povs.company_name).all()
        print ('Data Loaded!')
        return

    def __iter__(self):
        return self

    def __next__(self):
        self.index += 1
        if self.index == len(self.sql_to_ss):
            raise StopIteration
        return self.sql_to_ss[self.index]


if __name__ == "__main__":
    # Smartsheet Config settings
    ss_config = dict(
        SS_TOKEN=my_secrets.passwords["SS_TOKEN"]
        )

    ss_token = ss_config['SS_TOKEN']
    ss = smartsheet.Smartsheet(ss_token)

    # Build the Sheet
    my_ss_model = SS_Model()
    sheet_name = 'junk test'
    my_sheet_build=[]
    my_col_details = []

    for x in my_ss_model:
        print (x[0],x[1],x[2],x[3],x[4])
        my_col_details.append(('', x[0], x[1], x[3]))

        if x[4] == '':
            my_sheet_build.append({'title': x[1], 'primary': x[2], 'type': x[3]})
        else:
            my_sheet_build.append({'title': x[1], 'primary': x[2], 'type': x[3], 'options': x[4]})

    sheet_spec = ss.models.Sheet({'name': sheet_name, 'columns': my_sheet_build})
    response = ss.Home.create_sheet(sheet_spec)

    # Did we create successfully ?
    # Create a dict of the response
    print("Response: ", response.message)
    resp_dict = response.to_dict()

    # DEBUG CODE - DO NOT DELETE
    # print("Response: ",response.message)
    # print(json.dumps(resp_dict, indent=2))
    # print ('done!')
    result_dict = resp_dict.get('result', {})
    sheet_id = result_dict['id']

    # Retrieve the column ids from the newly created sheet
    # Crete a dict of the SS col_ids which will contain (SS_column_name:SS_column_id)
    #
    col_data = resp_dict.get('result', {}).get('columns', {})
    col_id_dict = {}

    for col_record in col_data:
        col_id_dict[col_record['title']]= col_record['id']

    print ('Col id and names',col_id_dict)

    # Add SS col ids to the col details list
    # By build by using a tmp_list
    tmp_list=[]
    for x in my_col_details:
        # Use the Smartsheet col name x[2] to look up the col id
        col_id = col_id_dict[x[2]]
        tmp_list.append((col_id, x[1], x[2], x[3]))

    my_col_details = tmp_list
    print (my_col_details)

    # Add Rows to the new table

    # Get the MySQL data
    my_ss_model.load_sql()

    for pov in my_ss_model.povs:
        row_next = ss.models.Row()
        row_next.to_top = True

        for x in my_col_details:
            col_id = x[0]
            col_sql_name = x[1]
            col_ss_name = x[2]
            col_type = x[3]
            row_value = eval("pov." + col_sql_name)

            # Change None type to something else
            if row_value is None:
                row_value = ""

            # # Set value for a PICKLIST to Yes or No
            # if col_type == 'PICKLIST':
            #     if row_value == 0:
            #         row_value = 'No'
            #     else:
            #         row_value = 'Yes'
            #
            # if col_ss_name == 'Active':
            #     if row_value == 0:
            #         row_value = 'Deleted'
            #     else:
            #         row_value = 'Active'


            # Change datetime to string
            if isinstance(row_value, datetime):
                row_value = row_value.strftime("%A, %d. %B %Y %I:%M%p")

            row_dict = {'column_id': col_id, 'value': row_value, 'strict': False}
            row_next.cells.append(row_dict)

        response = ss.Sheets.add_rows(sheet_id, [row_next])

        # DEBUG CODE - DO NOT DELETE
        # print("Response: ", response.message)
        # resp_dict = response.to_dict()
        # print(json.dumps(resp_dict, indent=2))



