from ta_pov import db
from ta_pov import my_secrets
import smartsheet
# Smartsheet Config settings
ss_config = dict(
    SS_TOKEN = my_secrets.passwords["SS_TOKEN"]
)


class ta_povs(db.Model):
    __tablename__ = 'tblPovs'
    id = db.Column(db.Integer, primary_key=True)
    cluster = db.Column(db.Integer)
    cisco_owner = db.Column(db.String(45))
    cisco_owner_name = db.Column(db.String(45))
    company_name = db.Column(db.String(45))
    customer_first_name = db.Column(db.String(45))
    customer_last_name = db.Column(db.String(45))
    customer_email = db.Column(db.String(45))
    primary_use_case = db.Column(db.String(45))
    tenant_name = db.Column(db.String(45))
    vrf_id = db.Column(db.Integer)
    root_scope_id = db.Column(db.String(100))
    total_sensors = db.Column(db.Integer)
    windows_sensors = db.Column(db.Integer)
    linux_sensors = db.Column(db.Integer)
    enforcement_sensors = db.Column(db.Integer)
    erspan_sensors = db.Column(db.Integer)
    netflow_sensors = db.Column(db.Integer)
    f5_sensors = db.Column(db.Integer)
    netscaler_sensors = db.Column(db.Integer)
    aws_sensors = db.Column(db.Integer)
    scopes_created = db.Column(db.Integer)
    workspaces_created = db.Column(db.Integer)
    primary_workspaces = db.Column(db.Integer)
    enforcement_enabled = db.Column(db.Integer)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    deleted_date = db.Column(db.DateTime)
    active = db.Column(db.Integer)
    extended = db.Column(db.Integer)
    deleted = db.Column(db.Integer)

    def newest_name(num):
        return ta_povs.query.order_by(ta_povs.company_name).limit(num)

    def __repr__(self):
        return "{},{},{}".format(self.id, self.cisco_owner, self.company_name)


class SS_Model:

    def __init__(self):
        ss_token = ss_config['SS_TOKEN']
        self.index = -1
        self.povs = ''
        self.ss_token = ''
        self.sheet_name = ''
        self.sheet_id = ''
        self.sheet_url = ''
        self.last_modified = ''
        self.total_rows = ''
        self.my_col_details = ''
        self.template_name = ''
        self.template_id = ''
        self.new_sheet_name = ''
        self.new_sheet_id = ''
        self.ss = smartsheet.Smartsheet(ss_token)
        self.sql_to_ss = [['id', 'POV ID', True, 'TEXT_NUMBER', ''],
                    ['cisco_owner_name', 'POV Owner Name', False, 'TEXT_NUMBER', ''],
                    ['company_name', 'Customer Name', False, 'TEXT_NUMBER', ''],
                    ['start_date', 'Start Date', False, 'DATE', ''],
                    ['end_date', 'End Date', False, 'DATE', ''],
                    ['CALCULATED', 'POV Days', False, 'TEXT_NUMBER', ''],
                    ['customer_first_name', 'Customer First Name', False, 'TEXT_NUMBER', ''],
                    ['customer_last_name', 'Customer Last Name', False, 'TEXT_NUMBER', ''],
                    ['customer_email', 'Customer Email', False, 'TEXT_NUMBER', ''],
                    ['cisco_owner', 'POV Owner Email', False, 'TEXT_NUMBER', ''],
                    ['tenant_name', 'Tenant Name', False, 'TEXT_NUMBER', ''],
                    ['vrf_id', 'vrf_id', False, 'TEXT_NUMBER', ''],
                    ['root_scope_id', 'root_scope_id', False, 'TEXT_NUMBER', ''],
                    ['total_sensors', 'total_sensors', False, 'TEXT_NUMBER', ''],
                    ['windows_sensors', 'windows_sensors', False, 'TEXT_NUMBER', ''],
                    ['linux_sensors', 'linux_sensors', False, 'TEXT_NUMBER', ''],
                    ['enforcement_sensors', 'enforcement_sensors', False, 'TEXT_NUMBER', ''],
                    ['erspan_sensors', 'erspan_sensors', False, 'TEXT_NUMBER', ''],
                    ['netflow_sensors', 'netflow_sensors', False, 'TEXT_NUMBER', ''],
                    ['f5_sensors', 'f5_sensors', False, 'TEXT_NUMBER', ''],
                    ['netscaler_sensors', 'netscaler_sensors', False, 'TEXT_NUMBER', ''],
                    ['tenant_name', 'tenant_name', False, 'TEXT_NUMBER', ''],
                    ['aws_sensors', 'aws_sensors', False, 'TEXT_NUMBER', ''],
                    ['scopes_created', 'scopes_created', False, 'TEXT_NUMBER', ''],
                    ['workspaces_created', 'workspaces_created', False, 'TEXT_NUMBER', ''],
                    ['deleted_date', 'Deleted Date', False, 'DATE', ''],
                    ['active', 'Active',False, 'PICKLIST', ['Active', 'Active - Extended', 'Deleted']],
                    ['extended', 'Extended', False, 'PICKLIST',['Yes', 'No']],
                    ['deleted', 'Deleted', False, 'PICKLIST', ['Yes', 'No']]]

    def load_sql(self):
        # Build the SQL query from tblPovs
        self.povs = ta_povs.query.order_by(ta_povs.company_name).all()
        print('Data Loaded!')
        return

    def __iter__(self):
        return self

    def __next__(self):
        self.index += 1
        if self.index == len(self.sql_to_ss):
            raise StopIteration
        return self.sql_to_ss[self.index]

class SS_Model_r1:

    def __init__(self):
        ss_token = ss_config['SS_TOKEN']
        self.index = -1
        self.povs = ''
        self.ss_token = ''
        self.raw_data_sheet_name = ''
        self.raw_data_sheet_id = ''
        self.raw_data_col_dict = ''
        self.total_rows = ''
        self.my_col_details = ''
        self.template_name = ''
        self.template_id = ''
        self.status_sheet_name = ''
        self.status_sheet_id = ''
        self.status_sheet_url = ''
        self.last_modified = ''
        self.ss = smartsheet.Smartsheet(ss_token)
        self.sql_to_ss = [['id', 'POV ID', True, 'TEXT_NUMBER', ''],
                    ['cisco_owner_name', 'POV Owner Name', False, 'TEXT_NUMBER', ''],
                    ['company_name', 'Customer Name', False, 'TEXT_NUMBER', ''],
                    ['start_date', 'Start Date', False, 'DATE', ''],
                    ['end_date', 'End Date', False, 'DATE', ''],
                    ['CALCULATED', 'POV Days', False, 'TEXT_NUMBER', ''],
                    ['customer_first_name', 'Customer First Name', False, 'TEXT_NUMBER', ''],
                    ['customer_last_name', 'Customer Last Name', False, 'TEXT_NUMBER', ''],
                    ['customer_email', 'Customer Email', False, 'TEXT_NUMBER', ''],
                    ['cisco_owner', 'POV Owner Email', False, 'TEXT_NUMBER', ''],
                    ['tenant_name', 'Tenant Name', False, 'TEXT_NUMBER', ''],
                    ['vrf_id', 'vrf_id', False, 'TEXT_NUMBER', ''],
                    ['root_scope_id', 'root_scope_id', False, 'TEXT_NUMBER', ''],
                    ['total_sensors', 'total_sensors', False, 'TEXT_NUMBER', ''],
                    ['windows_sensors', 'windows_sensors', False, 'TEXT_NUMBER', ''],
                    ['linux_sensors', 'linux_sensors', False, 'TEXT_NUMBER', ''],
                    ['enforcement_sensors', 'enforcement_sensors', False, 'TEXT_NUMBER', ''],
                    ['erspan_sensors', 'erspan_sensors', False, 'TEXT_NUMBER', ''],
                    ['netflow_sensors', 'netflow_sensors', False, 'TEXT_NUMBER', ''],
                    ['f5_sensors', 'f5_sensors', False, 'TEXT_NUMBER', ''],
                    ['netscaler_sensors', 'netscaler_sensors', False, 'TEXT_NUMBER', ''],
                    ['tenant_name', 'tenant_name', False, 'TEXT_NUMBER', ''],
                    ['aws_sensors', 'aws_sensors', False, 'TEXT_NUMBER', ''],
                    ['scopes_created', 'scopes_created', False, 'TEXT_NUMBER', ''],
                    ['workspaces_created', 'workspaces_created', False, 'TEXT_NUMBER', ''],
                    ['deleted_date', 'Deleted Date', False, 'DATE', ''],
                    ['active', 'Active',False, 'PICKLIST', ['Active', 'Active - Extended', 'Deleted']],
                    ['extended', 'Extended', False, 'PICKLIST',['Yes', 'No']],
                    ['deleted', 'Deleted', False, 'PICKLIST', ['Yes', 'No']]]

    def load_sql(self):
        # Build the SQL query from tblPovs
        self.povs = ta_povs.query.order_by(ta_povs.company_name).all()
        print('Data Loaded!')
        return

    def __iter__(self):
        return self

    def __next__(self):
        self.index += 1
        if self.index == len(self.sql_to_ss):
            raise StopIteration
        return self.sql_to_ss[self.index]
