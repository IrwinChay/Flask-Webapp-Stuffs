from flask import Flask, render_template, jsonify, request
import ssh
import client
import json
import time
from timeloop import Timeloop
from datetime import timedelta
from flask import Flask,Blueprint,render_template, url_for, request, redirect, flash
from flask_login import login_user,logout_user,login_required
from werkzeug.security import check_password_hash


main = Blueprint('main',__name__)

@main.route("/")
def home():
    return render_template("home.html")

@main.route("/contact")
def contact():
    return render_template("contact.html")

@main.route('/sensors')
def sensor_reading():
    if (raspPi):
        return jsonify(grove.sensor_readings())
    return ""

@main.route("/settings", methods=['POST', 'GET'])
def settings():
    if request.method == "POST":
        ssh = ssh()
        UV_mode_value = request.form['UV_mode']     # 'UV_mode' need to be same as the value of 'name' input in HTML file
        Auto_mode_value = request.form['Auto_mode'] #  Same as above
        Hour_value = int(request.form['Hours'])     #  Same as above 
        Minute_value = int(request.form['Minutes']) #  Same as above
        Sec_value = int(request.form['Seconds'])    #  Same as above
        ssh.uv_on_off(UV_mode_value)                #  Turn on or off UV
        ssh.kill_auto_mode()                        #  Terminate the auto_mode
        ssh.run_auto_mode((Hour_value * 3600 + Minute_value * 60 + Sec_value), Auto_mode_value) # Make sure runtime is in seconds
    return render_template("settings.html")         

@main.route('/admin')
def admin():
    with open('plots.json', 'r', encoding="utf8") as f:
        content = f.read()
    content = content.replace('\n', ' ').replace('\r', '')
    with open('db.json', 'r', encoding="utf8") as f:
        content2 = f.read()
    content2 = content2.replace('\n', ' ').replace('\r', '')
    return render_template('admin.html', plotsJson = content, dbJSON = content2)

@main.route('/overrides')
def overrides():
    return render_template('overrides.html', sensor_reading="Click to view current sensor readings")

@main.route('/move')
def move():
    if (request.args.get('direction', default = 'none', type = str) == 'forward'):
        message = "f"
    elif (request.args.get('direction', default = 'forward', type = str) == 'backward'):
        message="b"
    else:
        message = request.args.get('x', default = '1', type= str) +','+ request.args.get('y', default = '1', type = str)
    print("Message is: " + message)
    client.initClient(message)

    # add to action log
    action = 'Moved to position ' + message
    addToActions(action)

    return render_template('overrides.html', sensor_reading="Click to view current sensor readings")

@main.route("/head")
def head():
    return render_template("head.html")

@main.route('/gridReact')
def gridding():
    with open('plots.json', 'r', encoding="utf8") as f:
        content = f.read()
    content = content.replace('\n', ' ').replace('\r', '')
    return render_template('grid11.html', plotsJson = content)

@main.route("/getPlots")
def getPlots():
    return "plots.json"

