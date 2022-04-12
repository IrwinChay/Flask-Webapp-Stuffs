from flask import Flask, render_template, request
import ssh
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

@main.route("/head")
def head():
    return render_template("head.html")


#if __name__ == "__main__":
    #app.run(debug=True)