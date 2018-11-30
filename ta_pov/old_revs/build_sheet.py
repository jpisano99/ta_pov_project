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

ss_token = ss_config['SS_TOKEN']
ss = smartsheet.Smartsheet(ss_token)

ss_cols=[]
ss_cols.append({'title':'POV ID','primary': True,'type':'TEXT_NUMBER'})

db_to_ss = {'id' :'POV ID',
        'cisco_owner' : 'POV Owner Email',
        'cisco_owner_name' : 'POV Owner Name',
        'company_name' :'Customer Name',
        'customer_first_name' :'Customer Contact',
        'customer_last_name' :'Customer Contact',
        'customer_email' :'Customer Email',
        'tenant_name' :'Tenant Name',
        'start_date' : 'Start Date',
        'end_date' : 'End Date',
        'deleted_date' : 'Deleted Date',
        'active' : 'Active',
        'extended' : 'Extended',
        'deleted' : 'Deleted'}

ss_cols.append({'title':'Customer Name','primary': False,'type':'TEXT_NUMBER'})
ss_cols.append({'title':'Customer Contact','primary': False,'type':'TEXT_NUMBER'})
ss_cols.append({'title':'Customer Email','primary': False,'type':'TEXT_NUMBER'})
ss_cols.append({'title':'POV Owner Email','primary': False,'type':'TEXT_NUMBER'})
ss_cols.append({'title':'POV Owner Name','primary': False,'type':'TEXT_NUMBER'})
ss_cols.append({'title':'Tenant Name','primary': False,'type':'TEXT_NUMBER'})
ss_cols.append({'title':'Start Date','primary': False,'type':'DATE'})
ss_cols.append({'title':'End Date','primary': False,'type':'DATE'})
ss_cols.append({'title':'Deleted Date','primary': False,'type':'DATE'})
ss_cols.append({'title': 'Active', 'primary': False, 'type': 'PICKLIST', 'options': ['Yes', 'No']})
ss_cols.append({'title': 'Extended', 'primary': False, 'type': 'PICKLIST', 'options': ['Yes', 'No']})
ss_cols.append({'title': 'Deleted', 'primary': False, 'type': 'PICKLIST', 'options': ['Yes', 'No']})

# Build the SQL query from tblPovs
povs = ta_povs.query.order_by(ta_povs.company_name).all()
for pov in povs:
    row_next = ss.models.Row()
    row_next.to_top = True
    print(pov.company_name)



# cluster = db.Column(db.Integer)
# vrf_id = db.Column(db.Integer)
# root_scope_id = db.Column(db.String(100))
# windows_sensors_deployed = db.Column(db.Integer)
# linux_sensors_deployed = db.Column(db.Integer)
# enforcement_sensors_deployed = db.Column(db.Integer)
# erspan_sensors_deployed = db.Column(db.Integer)
# netflow_sensors_deployed = db.Column(db.Integer)
# scopes_created = db.Column(db.Integer)
# workspaces_created = db.Column(db.Integer)

sheet_spec = ss.models.Sheet({'name': 'POV BOT Status', 'columns': ss_cols})
response = ss.Home.create_sheet(sheet_spec)




# # # Run a Query to get the col names
# sql = "SHOW COLUMNS FROM povbot.tblPovs "
# db_cols = db.engine.execute(sql)
#
# ss_cols = []
# primary_col = True
#
# for db_col in db_cols:
#     jim = Map_it(db_col)
#     # print(db_col.Field,db_col.Type,db_col[0])
#     # primary_col= False
#     ss_cols.append