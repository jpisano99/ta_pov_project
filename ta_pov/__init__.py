import os
from base64 import b64encode
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy

# Application Passwords kept here
from ta_pov import my_secrets

# Create the Flask App Object
app = Flask(__name__)

# Assign App Config Variables
token = os.urandom(64)
token = b64encode(token).decode('utf-8')
app.config['SECRET_KEY']= token
app.config['DEBUG'] = False # Enable/Disable debug toolbar
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False # allow page redirects without intercept
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# database configuration settings
db_config = dict(
    DATABASE = "povbot",
    USER     = "smartsheet",
    PASSWORD = my_secrets.passwords["DB_PASSWORD"],
    HOST     = "tet-pov-bot.cdo0mbvpds6n.us-east-2.rds.amazonaws.com"
)

# Smartsheet Config settings
ss_config = dict(
    SS_TOKEN = my_secrets.passwords["SS_TOKEN"]
)


#
# Various MySql Connectors
#

# AWS MySQL
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:' + database['PASSWORD'] + '@aa1ho1ni9nfz56e.cp1kaaiuayns.us-east-1.rds.amazonaws.com/cust_ref_db'

# Local MySQL
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:' + database['PASSWORD'] + '@localhost/cust_ref_db'

# Local sqllite
#application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'jimsDB.db')

# Remote connect to RaspPi (Stan)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:' + database['PASSWORD'] + '@overlook-mountain.com:12498/cust_ref_db'

# Local connect to RaspPi (Stan)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'+\
                                            db_config['USER']+\
                                        ':'+db_config['PASSWORD']+\
                                        '@'+db_config['HOST']+':3306/'+\
                                            db_config['DATABASE']

#
# Create db for SQL Alchemy
db = SQLAlchemy(app)

# Are we connected ?
db_status = (db.engine.execute("SHOW VARIABLES WHERE Variable_name = 'port'"))
for x in db_status:
    db_port = x.values()

db_status = (db.engine.execute("SHOW VARIABLES WHERE Variable_name = 'hostname'"))
for x in db_status:
    db_host = x.values()

db_status = (db.engine.execute('SELECT USER()'))
for x in db_status:
    db_user = x.values()

print('You are connected to MySQL Host '+db_host[1]+' on Port '+db_port[1]+' as '+db_user[0])

# import the model()s and views
from ta_pov import models
from ta_pov import views

# To turn on the Debug Toolbar set to True
#toolbar = DebugToolbarExtension(application)
