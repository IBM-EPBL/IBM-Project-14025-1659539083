import datetime
import pickle
import sqlite3

import numpy as np
import pandas as pd
from flask import (Flask, flash, jsonify, redirect, render_template, request,
                   session, url_for)
from flask_cors import cross_origin

app = Flask(__name__, template_folder="templates")
app.secret_key="vicky"
model = pickle.load(open("models/cat.pkl", "rb"))
print("Model Loaded")

con=sqlite3.connect("database.db")
con.execute("create table if not exists user(pid integer primary key,name text,address text,contact integer,mail text)")
con.close()

@app.route("/",methods=['GET'])
@cross_origin()
def home():
    if not session:
        return redirect(url_for("login"))
    return render_template("index.html")

@app.route("/login", methods=['GET', 'POST'])
@cross_origin()
def login():
    if request.method=='POST':
        name=request.form['name']
        password=request.form['password']
        con=sqlite3.connect("database.db")
        con.row_factory=sqlite3.Row
        cur=con.cursor()
        cur.execute("select * from user where name=? and mail=?",(name,password))
        data=cur.fetchone()

        if data:
            session["name"]=data["name"]
            session["mail"]=data["mail"]
            return redirect("/")
        else:
            flash("Username and Password Mismatch","danger")

    return render_template("login.html")

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        try:
            name=request.form['name']
            address=request.form['address']
            contact=request.form['contact']
            mail=request.form['mail']
            con=sqlite3.connect("database.db")
            cur=con.cursor()
            cur.execute("insert into user(name,address,contact,mail)values(?,?,?,?)",(name,address,contact,mail))
            con.commit()
            flash("Record Added  Successfully","success")
        except:
            flash("Error in Insert Operation","danger")
        finally:
            con.close()
            return redirect(url_for("login"))

    return render_template('register.html')
		
@app.route("/index",methods=['GET', 'POST'])
@cross_origin()
def index():
    if not session:
        return redirect(url_for("login"))
    if request.method == "POST":
		# DATE
        date = request.form['date']
        day = float(pd.to_datetime(date, format="%Y-%m-%dT").day)
        month = float(pd.to_datetime(date, format="%Y-%m-%dT").month)
		# MinTemp
	    
        minTemp = float(request.form['mintemp'])
		# MaxTemp
        maxTemp = float(request.form['maxtemp'])
		# Rainfall
        rainfall = float(request.form['rainfall'])
		# Evaporation
        evaporation = float(request.form['evaporation'])
		# Sunshine
        sunshine = float(request.form['sunshine'])
		# Wind Gust Speed
        windGustSpeed = float(request.form['windgustspeed'])
		# Wind Speed 9am
        windSpeed9am = float(request.form['windspeed9am'])
		# Wind Speed 3pm
        windSpeed3pm = float(request.form['windspeed3pm'])
		# Humidity 9am
        humidity9am = float(request.form['humidity9am'])
		# Humidity 3pm
        humidity3pm = float(request.form['humidity3pm'])
		# Pressure 9am
        pressure9am = float(request.form['pressure9am'])
		# Pressure 3pm
        pressure3pm = float(request.form['pressure3pm'])
		# Temperature 9am
        temp9am = float(request.form['temp9am'])
		# Temperature 3pm
        temp3pm = float(request.form['temp3pm'])
		# Cloud 9am
        cloud9am = float(request.form['cloud9am'])
		# Cloud 3pm
        cloud3pm = float(request.form['cloud3pm'])
		# Cloud 3pm
        location = float(request.form['location'])
		# Wind Dir 9am
        winddDir9am = float(request.form['winddir9am'])
		# Wind Dir 3pm
        winddDir3pm = float(request.form['winddir3pm'])
		# Wind Gust Dir
        windGustDir = float(request.form['windgustdir'])
		# Rain Today
        rainToday = float(request.form['raintoday'])
        input_lst = [location , minTemp , maxTemp , rainfall , evaporation , sunshine ,
					 windGustDir , windGustSpeed , winddDir9am , winddDir3pm , windSpeed9am , windSpeed3pm ,
					 humidity9am , humidity3pm , pressure9am , pressure3pm , cloud9am , cloud3pm , temp9am , temp3pm ,
					 rainToday , month , day]

        pred = model.predict(input_lst)
        output = pred
        if output == 0:
            return redirect(url_for("sunny"))
        else:
            return redirect(url_for("rainy"))
    return render_template("predictor.html")
	
@app.route("/predict")
def predictor():
    if not session:
        return redirect(url_for("login"))
    return render_template('predictor.html')

@app.route("/sunny")
def sunny():
    if not session:
        return redirect(url_for("login"))
    return render_template('after_sunny.html')

@app.route("/rainy")
def rainy():
    if not session:
        return redirect(url_for("login"))
    return render_template('after_rainy.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__=='__main__':
	app.run(debug=True)