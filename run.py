#!flask/bin/python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for, request
from awslib.dynamodb_date import dynamodb_date
from awslib.SNS import sns
import boto3
import json
app = Flask(__name__)


@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] == "" or request.form['password'] == "":
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('.auth'), code=307)
    return render_template('login.html', error=error)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        render_template('signup.html', error=error)
    return render_template('signup.html', error=error)


@app.route('/home/editprofile', methods=['GET', 'POST'])
def editprofile():
    error = None
    if request.method == 'POST':
        username = request.form["myname"]
        print username
        db = dynamodb_date()
        user_data = db.get_user(username)
        print user_data.get("address")

        return render_template('edit.html', user=user_data, error =error )
    return render_template('edit.html', error =error )



@app.route('/home/subscribe', methods=['GET', 'POST'])
def subscribe():
    error = None
    print "sub"
    print "sub1"
    username = request.form["myname"]
    print username
    db = dynamodb_date()
    user_data = db.get_user(username)
    print user_data.get("address")
    notification = sns()
    print 'subscribe new'
    print user_data
    #db.update(user)
    if request.get('sbs') =='0':
        notification.subscribe1(user_data["email"])
    elif request.get('sbs') =='1':
        notification.subscribe1_phone(user_data["phone"])
    return render_template('subscribe.html', user=user_data, error =error )




@app.route('/home/updateprofile', methods=['GET', 'POST'])
def updateprofile():
    if request.method=='POST':
        print request.form['name'] == ""
        if (request.form['name'] == "" or request.form['password'] == "" or
                    request.form['emailid'] == "" or request.form['phone'] == "" or
                    request.form['dob'] == "" or request.form['addrline1'] == "" or
                    request.form['addrline2'] == "" or request.form['city'] == "" or
                    request.form['state'] == "" or request.form['country'] == "" or
                    request.form['Gender'] == "" or request.form['Interested'] == ""):
            msg = 'All fields should be filled to complete sign up.'
            print msg
        else:
            db = dynamodb_date()
            db.insert_user(name=request.form['name'], pwd=request.form['password'], email=request.form['emailid'],
                           phone=request.form['phone'], dob=request.form['dob'], addrline1=request.form['addrline1'],
                           addrline2=request.form['addrline2'], addrCity=request.form['city'], addrState=request.form['state'],
                           addrCountry=request.form['country'], gender=request.form['Gender'],
                           interestedIn=request.form['Interested'])
            msg = "Successfully updated"
    return redirect(url_for('.home', username=request.form['name']), code=302)




@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method=='POST':
        print request.form['name'] == ""
        if (request.form['name'] == "" or request.form['password'] == "" or
                    request.form['emailid'] == "" or request.form['phone'] == "" or
                    request.form['dob'] == "" or request.form['addrline1'] == "" or
                    request.form['addrline2'] == "" or request.form['city'] == "" or
                    request.form['state'] == "" or request.form['country'] == "" or
                    request.form['Gender'] == "" or request.form['Interested'] == ""):
            msg = 'All fields should be filled to complete sign up.'
            print msg
        else:
            db = dynamodb_date()
            db.insert_user(name=request.form['name'], pwd=request.form['password'], email=request.form['emailid'],
                           phone=request.form['phone'], dob=request.form['dob'], addrline1=request.form['addrline1'],
                           addrline2=request.form['addrline2'], addrCity=request.form['city'], addrState=request.form['state'],
                           addrCountry=request.form['country'], gender=request.form['Gender'],
                           interestedIn=request.form['Interested'])
            msg = "Successfully Registered"
    return render_template('signup.html', message=msg)


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        db = dynamodb_date()
        user = db.get_user(request.form['username'])
        if user["password"] == request.form['password']:
            return redirect(url_for('.home', username=request.form['username']), code=302)
        else:
            err = "Invalid Credentials! Try again"
    return render_template('login.html', error=err)


@app.route('/home/<username>', methods=['GET', 'POST'])
def home(username=None):
    if request.method == 'POST':
        db = dynamodb_date()
        user = db.get_user(username)
        notification = sns()
        print 'subscribe'
        print user
        db.update(user)
        notification.subscribe1(user["email"])


       #notification.sendtoSubscribe()
    db = dynamodb_date()
    user = db.get_user(username)
    interested_users = db.get_intereseted(user["uname"], user["gender"], user["interestedIn"])
    print type(user)
    print user
    return render_template("home.html", user_data=user, interested_users=interested_users)


app.run(debug=True, port=8122)