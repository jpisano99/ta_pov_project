from ta_pov import db

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
    tenant_name = db.Column(db.String(45))
    vrf_id = db.Column(db.Integer)
    root_scope_id = db.Column(db.String(100))
    windows_sensors_deployed = db.Column(db.Integer)
    linux_sensors_deployed = db.Column(db.Integer)
    enforcement_sensors_deployed = db.Column(db.Integer)
    erspan_sensors_deployed = db.Column(db.Integer)
    netflow_sensors_deployed = db.Column(db.Integer)
    scopes_created = db.Column(db.Integer)
    workspaces_created = db.Column(db.Integer)
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

class Coverage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pss_name = db.Column(db.String(30))
    tsa_name = db.Column(db.String(30))
    sales_level_1 = db.Column(db.String(30))
    sales_level_2 = db.Column(db.String(30))
    sales_level_3 = db.Column(db.String(30))
    sales_level_4 = db.Column(db.String(30))
    sales_level_5 = db.Column(db.String(30))
    fiscal_year = db.Column(db.String(30))

    @staticmethod
    def newest():
        return Coverage.query.order_by(Coverage.pss_name).all()

    def get_page(page_num):
        num_of_pages = Coverage.query.paginate(per_page=10)
        return Coverage.query.order_by(Coverage.id).offset(page_num*10)

    def newest_name(num):
        return Coverage.query.order_by(Coverage.pss_name).limit(num)

    # def get_pss(find_pss):
    #     print("looking for" ,find_pss)
    #     return Coverage.query.filter(Coverage.id==2)

    def __repr__(self):
       return "<name {}: '{} , {}'>".format(self.id, self.pss_name,self.tsa_name)

class Managers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(45))
    first_name = db.Column(db.String(45))
    segment = db.Column(db.String(45))

    @staticmethod
    def newest():
        return Managers.query.order_by(Managers.last_name).all()

    def __repr__(self):
       return "<name {}: '{} , {}'>".format(self.id, self.last_name,self.first_name,self.segment)

class sales_levels(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Sales_Level_1 = db.Column(db.String(30))
    Sales_Level_2 = db.Column(db.String(30))
    Sales_Level_3 = db.Column(db.String(30))
    Sales_Level_4 = db.Column(db.String(30))
    Sales_Level_5 = db.Column(db.String(30))

    # @staticmethod
    # def newest():
    #     return Managers.query.order_by(Managers.last_name).all()

    # def __repr__(self):
    #    return "<name {}: '{} , {}'>".format(sel