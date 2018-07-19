import smartsheet
import json

# Application Passwords kept here
from ta_pov import my_secrets

# Smartsheet Config settings
ss_config = dict(
    SS_TOKEN = my_secrets.passwords["SS_TOKEN"]
)

def update_customer_req():
    ss_token = ss_config['SS_TOKEN']
    ss = smartsheet.Smartsheet(ss_token)

    # Configure email
    email_spec = ss.models.MultiRowEmail()
    email_spec.send_to = [
      ss.models.Recipient({'email': 'jpisano@cisco.com'})]
    #  ss.models.Recipient({'email': 'jpisano99@gmail.com'})]

    email_spec.subject = 'Please update based on meeting'
    email_spec.message = 'some message'
    email_spec.cc_me = False
    email_spec.row_ids = [8996155145119620]  # Second row from bottom
    email_spec.column_ids = [4813469095618436]  # Customer Name
    email_spec.include_attachments = False
    email_spec.include_discussions = False

    # Send update request
    new_update_request = ss.Sheets.send_update_request(
        550333354141572,           # sheet_id Tetration POV On-Demand POV Status-Test
        email_spec
    )

    return


if __name__ == "__main__":
    update_customer_req()

