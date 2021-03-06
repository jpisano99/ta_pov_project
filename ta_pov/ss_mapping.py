#
# [sql_col_name, smartsheet_col_name, smartsheet key?, smartsheet data type, [list of choices for pick list]
#


sql_to_ss = [['id', 'POV ID', True, 'TEXT_NUMBER', ''],
              ['cisco_owner_name', 'POV Owner Name', False, 'TEXT_NUMBER', ''],
              ['company_name', 'Customer Name', False, 'TEXT_NUMBER', ''],
              ['LOOKUP', 'Forecast', False, 'TEXT_NUMBER', ''],
              ['total_sensors', 'total_sensors', False, 'TEXT_NUMBER', ''],
              ['start_date', 'Start Date', False, 'DATE', ''],
              ['end_date', 'End Date', False, 'DATE', ''],
              ['CALCULATED', 'POV Days', False, 'TEXT_NUMBER', ''],
              ['customer_first_name', 'Customer First Name', False, 'TEXT_NUMBER', ''],
              ['customer_last_name', 'Customer Last Name', False, 'TEXT_NUMBER', ''],
              ['customer_email', 'Customer Email', False, 'TEXT_NUMBER', ''],
              ['cisco_owner', 'POV Owner Email', False, 'TEXT_NUMBER', ''],
              ['tenant_name', 'Tenant Name', False, 'TEXT_NUMBER', ''],
              ['deleted_date', 'Deleted Date', False, 'DATE', ''],
              ['active', 'POV Status', False, 'PICKLIST', ['Active', 'Active - Extended', 'Deleted']]]


# sql_to_ss = [['id', 'POV ID', True, 'TEXT_NUMBER', ''],
#               ['cisco_owner_name', 'POV Owner Name', False, 'TEXT_NUMBER', ''],
#               ['company_name', 'Customer Name', False, 'TEXT_NUMBER', ''],
#               ['LOOKUP', 'Forecast', False, 'TEXT_NUMBER', ''],
#               ['start_date', 'Start Date', False, 'DATE', ''],
#               ['end_date', 'End Date', False, 'DATE', ''],
#               ['CALCULATED', 'POV Days', False, 'TEXT_NUMBER', ''],
#               ['customer_first_name', 'Customer First Name', False, 'TEXT_NUMBER', ''],
#               ['customer_last_name', 'Customer Last Name', False, 'TEXT_NUMBER', ''],
#               ['customer_email', 'Customer Email', False, 'TEXT_NUMBER', ''],
#               ['cisco_owner', 'POV Owner Email', False, 'TEXT_NUMBER', ''],
#               ['tenant_name', 'Tenant Name', False, 'TEXT_NUMBER', ''],
#               ['vrf_id', 'vrf_id', False, 'TEXT_NUMBER', ''],
#               ['root_scope_id', 'root_scope_id', False, 'TEXT_NUMBER', ''],
#               ['total_sensors', 'total_sensors', False, 'TEXT_NUMBER', ''],
#               ['windows_sensors', 'windows_sensors', False, 'TEXT_NUMBER', ''],
#               ['linux_sensors', 'linux_sensors', False, 'TEXT_NUMBER', ''],
#               ['enforcement_sensors', 'enforcement_sensors', False, 'TEXT_NUMBER', ''],
#               ['erspan_sensors', 'erspan_sensors', False, 'TEXT_NUMBER', ''],
#               ['netflow_sensors', 'netflow_sensors', False, 'TEXT_NUMBER', ''],
#               ['f5_sensors', 'f5_sensors', False, 'TEXT_NUMBER', ''],
#               ['netscaler_sensors', 'netscaler_sensors', False, 'TEXT_NUMBER', ''],
#               ['tenant_name', 'tenant_name', False, 'TEXT_NUMBER', ''],
#               ['aws_sensors', 'aws_sensors', False, 'TEXT_NUMBER', ''],
#               ['scopes_created', 'scopes_created', False, 'TEXT_NUMBER', ''],
#               ['workspaces_created', 'workspaces_created', False, 'TEXT_NUMBER', ''],
#               ['deleted_date', 'Deleted Date', False, 'DATE', ''],
#               ['active', 'Active', False, 'PICKLIST', ['Active', 'Active - Extended', 'Deleted']],
#               ['extended', 'Extended', False, 'PICKLIST', ['Yes', 'No']],
#               ['deleted', 'Deleted', False, 'PICKLIST', ['Yes', 'No']]]

