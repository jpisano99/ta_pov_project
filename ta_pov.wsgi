#
# Basic mod_WSGI file
#
import sys

#
# This will execute our app inside the Virtual Env
#
activate_this = '/var/www/ta_pov_app/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

#
# Add the path to our package directory
#
sys.path.insert(0, '/var/www/ta_pov/')

# This pulls in the Flask app object from the package __init__.py file
from ta_pov import app as application
