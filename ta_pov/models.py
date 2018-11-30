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


