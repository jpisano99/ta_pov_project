from flask import render_template, flash, redirect, url_for, request, session,jsonify,g
import json
from ta_pov import  app
from ta_pov.models import *
from ta_pov.my_functions import *

# User Passwords kept here
from ta_pov import my_secrets

@app.route('/index')
def index():
    # Check in on the POV db
    povs = ta_povs.query.order_by(ta_povs.company_name).all()
    pov_count= ta_povs.query.count()
    # Get existing sheet info (if any)
    sheet_dict = sheet_details('POV BOT Status')

    return render_template('index.html',pov_count=pov_count,sheet_dict=sheet_dict)


# @app.route('/login',methods=['GET','POST'])
# def login():
#     if request.method == 'POST':
#         print ('User: ',request.form['inputEmail'])
#         print('Password: ',request.form['inputPassword'])
#     return render_template('login.html')


@app.route('/update_ss')
def update_ss():
    sheet_name = 'POV BOT Status'
    # Get existing sheet info (if any)
    sheet_dict = sheet_details(sheet_name)

    # Delete existing sheet_name (if any)
    delete_sheet(sheet_dict)
    print('deleted sheet')

    # Recreate sheet and create new dict
    create_sheet(sheet_name)
    sheet_dict = sheet_details(sheet_name)

    # Add new rows
    add_rows(sheet_dict)
    print('Added Rows')
    return redirect(url_for('index'))


@app.route('/process',methods=['POST'])
def process():
    process_req = json.loads((request.data).decode("utf-8"))
    sheet_dict = {}
    sheet_name = 'POV BOT Status'

    if process_req == 'get_sheet_data':
        # Get existing sheet info (if any)
        sheet_dict = sheet_details(sheet_name)
        print('got details')

    elif process_req == 'delete_sheet':
        # Delete existing sheet_name
        delete_sheet(sheet_dict)
        print('deleted sheet')

    elif process_req == 'create_sheet':
        # Recreate sheet and create new dict
        create_sheet(sheet_name)
        sheet_dict = sheet_details(sheet_name)
        print('created sheet')

    elif process_req == 'add_rows':
        # Add new rows
        add_rows(sheet_dict)
        print('rows added')

    print(process_req)
    print(sheet_dict)
    process_result = 'Got Sheet Data'
    return jsonify({'result': sheet_dict})


@app.route('/ajax_test')
def ajax_test():

    return render_template('ajax_test.html')


#
# Session related functions
#
@app.route('/', methods=['GET', 'POST'])
def login():
    print ("request is a",request.method)
    print ("Looking for: ",url_for('static',filename='images/ta_logo.png'))
    if request.method == 'POST':
        session.pop('user', None)

        if request.form['password'] == my_secrets.passwords["USER_PASSWORD"]:
            print('found password')
            session['user'] = request.form['username']
            return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/protected')
def protected():
    if g.user:
        return render_template('index.html')

    return redirect(url_for('login'))

@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@app.route('/getsession')
def getsession():
    if 'user' in session:
        return session['user']

    return 'Not logged in!'

@app.route('/dropsession')
def dropsession():
    session.pop('user', None)
    return 'Dropped!'


#
# Error Page Handling
#

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'),500