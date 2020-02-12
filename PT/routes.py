import os
import secrets
import datetime
import requests
import calendar
import time
import sqlite3
import smtplib
import uuid
import random

from flask import Flask, render_template, url_for, redirect, flash, request, session
from PT.models import AdminAccess, Devices, Invoices, Repair, Subscription, User
from PT.forms import RegistrationForm, LoginForm, RepairForm, RequestResetForm, ResetPasswordForm, UpdateAccountForm, SubscriptionForm, AdminRegistrationForm, InvoiceForm, DeviceRegistrationForm
from PT import app, db, bcrypt, mail
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message, Mail
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
from datetime import timedelta
from sqlalchemy import create_engine, select

global_system_status = "Online"

def send_system_status_failure_email():
    powelltech_email = "Powell.ind.inc@gmail.com"
    customer_email = "Powell.ind.inc@gmail.com"
    msg = MIMEMultipart('alternative')
    text = ''
    msg['Subject'] = "Fatal Alert | Systems Offline"
    msg['From'] = "PowellTech Inc. © Engineering"
    msg['To'] = customer_email
    html = '''
    <!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta http-equiv="X-UA-Compatible" content="ie=edge" />
    <link
      href="https://fonts.googleapis.com/css?family=Catamaran"
      rel="stylesheet"
    />
  </head>
  <body>
    <header>
      <h1
        style="text-align:center;font-family:Gothic A1,sans-serif;font-weight:100;"
      >
        <img
          src="https://i.ibb.co/bd26Cym/Small-Logo.jpg"
          alt="Small-Logo"
          style="max-width:25%; border:0"
        /> <br />
        (Internal - Distribution Strictly Prohibited)
      </h1>
      <div
        style="margin-left:5%;margin-right:5%;font-family:Gothic A1,sans-serif;font-weight:100;"
      >
        <h1
          style="text-align:center;font-family:Gothic A1,sans-serif;font-weight:100;"
        >
          System Status:
        </h1>
        <h2
          style="text-align:center;font-family:Gothic A1,sans-serif;font-weight:100;"
        >
          Systems <span style="color:red">OFFLINE</span>
        </h2>
        <hr />
        <h3
          style="text-align:center;font-family:Gothic A1,sans-serif; font-weight: 100"
        >
          Attention: PowellTech Vital Systems are currently:
          <span style="color:red">OFFLINE</span>
          <br />
          <br />
          Upon completion of a Systems Check, a PowellTech systems failure has
          been detected, and unresolved. <br />
          Vital systems are non-operational. <br />
          A system check will be attempted again in 5 minutes.
        </h3>
        <hr />
        <h6
          style="text-align:center;font-family:Gothic A1,sans-serif;font-weight:100;"
        >
          <img
            src="https://i.ibb.co/bd26Cym/Small-Logo.jpg"
            alt="Small-Logo"
            style="width:10%; border:0"
          />
        </h6>
        <p style="text-align:center;">
          Copyright &copy 2019 Powell Industries
        </p>
        <p style="text-align:center;">
          All Rights Reserved.
        </p>
      </div>
    </header>
  </body>
</html>

    '''
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)
    mail = smtplib.SMTP_SSL('smtp.gmail.com', 465)

    mail.ehlo()

    mail.login(powelltech_email, 'Powell2019!')
    mail.sendmail(powelltech_email, customer_email, msg.as_string())
    mail.quit()

def send_system_status_online_email():
    powelltech_email = "Powell.ind.inc@gmail.com"
    customer_email = "Powell.ind.inc@gmail.com"
    msg = MIMEMultipart('alternative')
    text = ''
    msg['Subject'] = "Alert | Vital Systems Online"
    msg['From'] = "PowellTech Inc. © Engineering"
    msg['To'] = customer_email
    html = '''
    <!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta http-equiv="X-UA-Compatible" content="ie=edge" />
    <link
      href="https://fonts.googleapis.com/css?family=Catamaran"
      rel="stylesheet"
    />
  </head>
  <body>
    <header>
      <h1
        style="text-align:center;font-family:Gothic A1,sans-serif;font-weight:100;"
      >
        <img
          src="https://i.ibb.co/bd26Cym/Small-Logo.jpg"
          alt="Small-Logo"
          style="max-width:25%; border:0"
        /> <br />
        (Internal - Distribution Strictly Prohibited)
      </h1>
      <div
        style="margin-left:5%;margin-right:5%;font-family:Gothic A1,sans-serif;font-weight:100;"
      >
        <h1
          style="text-align:center;font-family:Gothic A1,sans-serif;font-weight:100;"
        >
          System Status:
        </h1>
        <h2
          style="text-align:center;font-family:Gothic A1,sans-serif;font-weight:100;"
        >
          Systems <span style="color:green">ONLINE</span>
        </h2>
        <hr />
        <h3
          style="text-align:center;font-family:Gothic A1,sans-serif; font-weight: 100"
        >
          Attention: PowellTech Vital Systems are currently:
          <span style="color:green">ONLINE</span>
          <br />
          <br />
          Upon completion of a Systems Check, no PowellTech system failures have
          been detected. <br /> <br />
          Vital systems are operational. <br /> <br />
          An e-mail system check has been completed.
        </h3>
        <hr />
        <h6
          style="text-align:center;font-family:Gothic A1,sans-serif;font-weight:100;"
        >
          <img
            src="https://i.ibb.co/bd26Cym/Small-Logo.jpg"
            alt="Small-Logo"
            style="width:10%; border:0"
          />
        </h6>
        <p style="text-align:center;">
          Copyright &copy 2019 Powell Industries
        </p>
        <p style="text-align:center;">
          All Rights Reserved.
        </p>
      </div>
    </header>
  </body>
</html>

    '''
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)
    mail = smtplib.SMTP_SSL('smtp.gmail.com', 465)

    mail.ehlo()

    mail.login(powelltech_email, 'Powell2019!')
    mail.sendmail(powelltech_email, customer_email, msg.as_string())
    mail.quit()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('page_not_found.html')

def hash_password():
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    return hashed_password

@app.route('/admin', methods = ['GET', 'POST'])
@login_required
def admin():
    if current_user.account_type == 'Admin':
        response = requests.get('https://ipinfo.io/')
        data = response.json()
        city = data['city']
        state = data['region']
        return render_template('admin_access.html', legend="ADMIN ACCESS | " + current_user.first_name + ' ' + current_user.last_name, city = data['city'], state=data['region'], system_status = global_system_status)
    else:
        return render_template('restricted_access.html', legend="Restricted Access")

@app.route('/adduser', methods = ['GET', 'POST'])
@login_required
def adminAddCustomerUser():
    form = RegistrationForm()
    if form.validate_on_submit():
      hash_password()
      user = User(first_name = form.first_name.data, last_name = form.last_name.data, 
                  email = form.email.data, password = hashed_password, 
                  phone_number = form.phone_number.data, account_type = 'Customer', 
                  created_by = current_user.first_name + ' ' + current_user.last_name)
      db.session.add(user)
      db.session.commit()
      send_admin_register_email(user)
      flash(f"{form.first_name.data} {form.last_name.data} has been added to the database.", 'success')
      flash(f"A registration e-mail has been sent to: {form.email.data}.", 'primary')
      return redirect(url_for('admin'))
    return render_template('add_user.html', legend="Admin Access | Add New User", form = form, system_status = global_system_status)

@app.route('/addAdminUser', methods = ['GET', 'POST'])
@login_required
def adminAddAdminUser():
    form = AdminRegistrationForm()
    if form.validate_on_submit():
        hash_password()
        user = User(first_name = form.first_name.data, last_name = form.last_name.data, email = form.email.data, 
                    password = hashed_password, phone_number = form.phone_number.data, account_type = 'Admin', 
                    created_by = current_user.first_name + ' ' + current_user.last_name, department = form.department.data, 
                    employe_id = form.employe_id.data)
        db.session.add(user)
        db.session.commit()
        send_admin_registration_email(user)
        flash(f"{form.first_name.data} {form.last_name.data} has been added to the database", 'success')
        flash(f"{form.first_name.data} {form.last_name.data} has been granted Adminstrative Access to PowellTech Systems.", 'warning')
    return render_template('add_admin_user.html', legend="Admin Access | Add New Admin User", form = form, system_status = global_system_status)

def send_admin_register_email(user):
    form = AdminRegistrationForm()
    powelltech_email = "Powell.ind.inc@gmail.com"
    customer_email = form.email.data
    msg = MIMEMultipart('alternative')
    text = ''
    msg['Subject'] = "Welcome to PowellTech ©!"
    msg['From'] = "PowellTech Inc. ©"
    msg['To'] = customer_email
    html = render_template('admin_register_email.html')
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)
    mail = smtplib.SMTP_SSL('smtp.gmail.com', 465)

    mail.ehlo()

    mail.login(powelltech_email, 'Powell2019!')
    mail.sendmail(powelltech_email, customer_email, msg.as_string())
    mail.quit()

def send_admin_user_registration_email(user):
    form = AdminRegistrationForm()
    powelltech_email = "Powell.ind.inc@gmail.com"
    customer_email = form.email.data
    msg = MIMEMultipart('alternative')
    text = ''
    msg['Subject'] = "Admin Access Granted"
    msg['From'] = "PowellTech Inc. ©"
    msg['To'] = customer_email
    html = render_template('admin_user_registration_email.html')
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)
    mail = smtplib.SMTP_SSL('smtp.gmail.com', 465)

    mail.ehlo()

    mail.login(powelltech_email, 'Powell2019!')
    mail.sendmail(powelltech_email, customer_email, msg.as_string())
    mail.quit()

@app.route('/createInvoice', methods = ['GET', 'POST'])
@login_required
def createInvoice():
    form = InvoiceForm()
    ts = calendar.timegm(time.gmtime())
    timestamp = time.ctime(ts)
    user_data_invoice = Invoices.query.filter_by(email = current_user.email).first()
    user_data_repair = Repair.query.filter_by(email = current_user.email).first()

    if form.validate_on_submit():
        invoice = Invoices(order_number = form.order_number.data, first_name = form.first_name.data, last_name = form.last_name.data, 
                            email = form.email.data, phone_number = form.phone_number.data, issue = form.issue.data, 
                            device_manufacturer = form.device_manufacturer.data, device_model = form.device_model.data, 
                            device_os = form.device_os.data, repair_price = form.repair_price.data, parts_price = form.parts_price.data, 
                            labor = form.labor.data, promotions = form.promotions.data, 
                            completed_by = current_user.first_name + ' ' + current_user.last_name, return_address = form.return_address.data, 
                            return_type = form.return_type.data, invoice_due_date = timestamp, repair_status = 'Completed')
        repair = Repair(first_name = form.first_name.data, last_name = form.last_name.data, email = form.email.data, phone_number = form.phone_number.data,
                            issue = form.issue.data, device_model = form.device_model.data, device_manufacturer = form.device_manufacturer.data,
                            device_os = form.device_os.data, order_number = form.order_number.data, repair_price = form.repair_price.data,
                            repair_status = 'Completed', invoice_due_date = "30 Days From: " + timestamp)
        db.session.add(invoice, repair)
        db.session.commit()
        send_invoice_email()
        flash(f"Invoice [ {order_number} ] created for: {form.first_name.data} {form.last_name.data}, and sent to: {form.email.data}", 'success')
        return redirect(url_for('admin'))
    return render_template('invoice.html', legend="Admin Access | Create Invoice", form = form)

def send_invoice_email():
    form = InvoiceForm()
    powelltech_email = "Powell.ind.inc@gmail.com"
    customer_email = form.email.data
    msg = MIMEMultipart('alternative')
    text = ''
    msg['Subject'] = "Invoice: " + form.first_name.data + ' ' + form.last_name.data + " (" + form.order_number.data + ")"
    msg['From'] = "PowellTech Inc. ©"
    msg['To'] = customer_email
    html = render_template('invoice_email.html')
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)
    mail = smtplib.SMTP_SSL('smtp.gmail.com', 465)

    mail.ehlo()

    mail.login(powelltech_email, 'Powell2019!')
    mail.sendmail(powelltech_email, customer_email, msg.as_string())
    mail.quit()

@app.route('/generateRepars', methods = ['GET', 'POST'])
@login_required
def generateRepairs():
    if current_user.is_authenticated and current_user.account_type == 'Admin':
        user_data = Repair.query.all()
        return render_template('repairs.html', user_data = user_data, legend = "PowellTech Repairs | " + current_user.first_name + ' ' + current_user.last_name)
    else:
        return render_template('restricted_access.html', legend='Restricted Access')

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def welcome():
    response = requests.get('https://ipinfo.io')
    data = response.json()
    city = data['city']
    state = data['region']
    return render_template('index.html', legend = "PowellTech Homepage", city = data['city'], state = data['region'])

@app.route('/subscription', methods = ['GET', 'POST'])
def subscribed():
    form = SubscriptionForm()
    if form.validate_on_submit():
        subscriber = Subscription(email = form.email.data)
        db.session.add(subscriber)
        db.session.commit()
        flash("Welcome to the PowellTech Newsletter!", 'success')
    return render_template('index.html', legend = "PowellTech Homepage", city = data['city'], state = data['region'], form = form)

@app.route('/register')
def register():
    form = RestrationForm()
    receiver = {form.email.data}
    if form.validate_on_submit():
        hash_password()
        user = User(first_name = form.first_name.data, last_name = form.last_name.data, email = form.email.data, password = hashed_password, 
                    phone_number = form.phone_number.data, account_type = 'Customer', created_by = form.first_name.data + ' ' + form.last_name.data)
        db.session.add(user)
        db.session.commit()
        send_register_email(user)
        login_user()
        flash(f"Hello {form.first_name.data}, welcome to PowellTech!", 'success')
        return redirect(url_for('home'))
    return render_template('register.html', legend="Join | PowellTech ©", form = form)

def send_register_email(user):
    form = RegistrationForm()
    powelltech_email = 'Powell.ind.inc@gmail.com'
    customer_email = form.email.data
    msg = MIMEMultipart('alternative')
    text = ''
    msg['Subject'] = "Welcome to PowellTech, " + form.first_name.data + "!"
    msg['From'] = "PowellTech Inc. ©"
    msg['To'] = customer_email
    html = render_template('register_email.html')
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)
    mail = smtplib.SMTP_SSL('smtp.gmail.com', 465)

    mail.ehlo()

    mail.login(powelltech_email, 'Powell2019!')
    mail.sendmail(powelltech_email, customer_email, msg.as_string())
    mail.quit()

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit() and form.email.data == "powell.ind.inc@gmail.com" and form.password.data != "Jesus151515!!!!!!":
        admin_failed_login_email()
        return redirect(url_for('restricted_access'))
    elif form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        login_user(user)
        if current_user.account_type == 'Admin':
            session.permament = True
            app.permanent_session_lifetime = timedelta(minutes = 60)
            admin_login_email()
            admin_access = AdminAccess(first_name = current_user.first_name, last_name = current_user.last_name, email = current_user.email, 
                                        phone_number = current_user.phone_number, access_type = 'Login', department = current_user.department)
            db.session.add(admin_access)
            db.session.commit()
            return redirect(url_for('admin'))
        else:
            user = User.query.filter_by(email = form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember = form.remember.data)
                session.permanent = True
                app.permanent_session_lifetime = timedelta(minutes = 30)
                login_email()
                flash(f"Welcome back, {current_user.first_name}. You have been successfully logged in.", 'success')
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash(f"Please check your E-mail ({form.email.data}) and Password.", 'danger')
    return render_template('login.html', legend = "Login | PowellTech ©", form = form)

def login_email():
    form = LoginForm()
    response = requests.get('https://ipinfo.io/')
    data = response.json()
    city = data['city']
    state = data['region']
    country = data['country']
    if country == "US":
        country = "United States of America"
    ts = calendar.timegm(time.gmtime())
    timestamp = time.ctime(ts)
    powelltech_email = "Powell.ind.inc@gmail.com"
    customer_email = form.email.data
    text = ""
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f'''Sucessful login for {current_user.first_name}.'''
    msg['From'] = "PowellTech Inc. ©"
    msg['To'] = customer_email
    html = render_template('login_email.html')
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)
    mail = smtplib.SMTP_SSL('smtp.gmail.com', 465)

    mail.ehlo()

    mail.login(powelltech_email, 'Powell2019!')
    mail.sendmail(powelltech_email, customer_email, msg.as_string())
    mail.quit()

def admin_login_email():
    form = LoginForm()
    response = requests.get('https://ipinfo.io/')
    data = response.json()
    city = data['city']
    state = data['region']
    country = data['country']
    if country == "US":
        country = "United States of America"
    ts = calendar.timegm(time.gmtime())
    timestamp = time.ctime(ts)
    powelltech_email = 'Powell.ind.inc@gmail.com'
    receiver = powelltech_email
    text = ""
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f'''Alert: {current_user.first_name} {current_user.last_name} | Admin Access Login.'''
    msg['From'] = "PowellTech Inc. ©"
    msg['To'] = receiver
    html = render_template('admin_login_email.html', city = city, state = state, country = country, timestamp = timestamp)
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)
    mail = smtplib.SMTP_SSL('smtp.gmail.com', 465)

    mail.ehlo()

    mail.login(powelltech_email, 'Powell2019!')
    mail.sendmail(powelltech_email, receiver, msg.as_string())
    mail.quit()

def admin_failed_login_email():
    form = LoginForm()
    response = requests.get('https://ipinfo.io/')
    data = response.json()
    city = data['city']
    state = data['region']
    country = data['country']
    if country == "US":
        country = "United States of America"
    ts = calendar.timegm(time.gmtime())
    timestamp = time.ctime(ts)
    powelltech_email = 'Powell.ind.inc@gmail.com'
    customer_email = form.email.data
    text = ""
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f'''Unsuccessful AdminAccess Login.'''
    msg['From'] = "PowellTech Inc. ©"
    msg['To'] = customer_email
    html = render_template('admin_failed_login_email.html', city = city, state = state, country = country, timestamp = timestamp)
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)
    mail = smtplib.SMTP_SSL('smtp.gmail.com', 465)

    mail.ehlo()

    mail.login(powelltech_email, 'Powell2019!')
    mail.sendmail(powelltech_email, customer_email, msg.as_string())
    mail.quit()

@app.route('/logout')
def logout():
    if current_user.account_type == 'Admin':
        admin_access = AdminAccess(id = current_user.employee_id, first_name = current_user.first_name, last_name = current_user.last_name, 
                                    email = current_user.email, phone_number = current_user.phone_number, access_type = "Logout", department = current_user.department)
        db.session.add(admin_access)
        db.session.commit()
        admin_logout_email()
        logout_user()
    else:
        logout_email()
        flash(f"Enjoy the remainder of your day, {current_user.first_name}. You have successfully been logged out.", "success")
        logout_user()
    return redirect(url_for('welcome'))

def logout_email():
    powelltech_email = 'Powell.ind.inc@gmail.com'
    customer_email = current_user.email
    text = f"{current_user.first_name} has been logged out."
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f'''Successful logout for {current_user.first_name} {current_user.last_name}'''
    msg['From'] = "PowellTech Inc. ©"
    msg['To'] = customer_email
    html = render_template('logout_email.html')
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)
    mail = smtplib.SMTP_SSL('smtp.gmail.com', 465)

    mail.ehlo()

    mail.login(powelltech_email, 'Powell2019!')
    mail.sendmail(powelltech_email, customer_email, msg.as_string())
    mail.quit()

@app.route('/adminlogout')
def adminLogout():
    aa = AdminAccess(first_name = current_user.first_name, last_name = current_user.last_name, email = current_user.email, 
                    phone_number = current_user.phone_number, access_type = "Logout", department = current_user.department)
    db.session.add(aa)
    db.session.commit()
    admin_logout_email()
    logout_user()
    return redirect(url_for('welcome'))

def admin_logout_email():
    powelltech_email = 'Powell.ind.inc@gmail.com'
    admin_email = current_user.email
    text = f"{current_user.first_name} has been logged out."
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f'''Successful logout for {current_user.first_name} {current_user.last_name}'''
    msg['From'] = "PowellTech Inc. ©"
    msg['To'] = admin_email
    html = render_template('admin_logout_email.html')
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)
    mail = smtplib.SMTP_SSL('smtp.gmail.com', 465)

    mail.ehlo()

    mail.login(powelltech_email, 'Powell2019!')
    mail.sendmail(powelltech_email, admin_email, msg.as_string())
    mail.quit()

@app.route('/reset_request', methods = ['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent to " + form.email.data + " with instructions to reset your password.", 'info')
        return redirect(url_for('request_sent'))
    return render_template('reset_request.html', title = "Reset Password", form = form)

def send_reset_email(user):
    token = user.get_reset_token()
    form = RequestResetForm()
    powelltech_email = 'Powell.ind.inc@gmail.com'
    customer_email = form.email.data
    text = ""
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f'''Password Reset for {form.email.data}'''
    msg['From'] = "PowellTech Inc. ©"
    msg['To'] = customer_email
    html = render_template('reset_email.html')
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)
    mail = smtplib.SMTP_SSL('smtp.gmail.com', 465)

    mail.ehlo()

    mail.login(powelltech_email, 'Powell2019!')
    mail.sendmail(powelltech_email, customer_email, msg.as_string())
    mail.quit()

@app.route("/request_sent", methods = ['GET', 'POST'])
def request_sent():
    return render_template("request_sent.html")

@app.route("/reset_request/<token>", methods = ['GET', 'POST'])
def get_reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash("It appears that link is invalid or has expired. Please attempt to reset your password again.", 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    reset_form = RequestResetForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash("Your password has been updated! You are now able to log in", 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title = "Reset Password", form = form, reset_form = reset_form)

@app.route('/home', methods = ['GET', 'POST'])
@login_required
def home():
    if session.permanent == False:
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('home'))
    response = requests.get('https://ipinfo.io/')
    data = response.json()
    city = data['city']
    state = data['region']
    return render_template('home.html', legend="Hello, " + current_user.first_name + " " + current_user.last_name + ".", city = data['city'], state = data['region'])

@app.route('/repair', methods = ['GET', 'POST'])
@login_required
def repair():
    form = RepairForm()
    user_data = Devices.query.filter_by(email=current_user.email).all()
    ts = calendar.timegm(time.gmtime())
    timestamp = time.ctime(ts)
    if form.validate_on_submit():
        order_number = generate_order_number()
        repair = Repair(first_name = form.first_name.data, last_name = form.last_name.data, email = form.email.data, phone_number = form.phone_number.data, issue = form.issue.data,
                        troubleshooting = form.troubleshooting.data, device_model = form.device_model.data, device_manufacturer = form.device_manufacturer.data, created_date = timestamp,
                        device_os = form.device_os.data, order_number = order_number, repair_price = 'TBD', repair_status = 'Received | Pending Acceptance')
        date = datetime.date.today()
        db.session.add(repair)
        db.session.commit()
        flash(f'''Repair Request Created for: {form.first_name.data} {form.last_name.data} has been created for your {form.device_manufacturer.data} {form.device_model.data}.''', 'success')
        flash(f'''Your Order ID is: ''' + order_number, 'info')
        send_repair_email(repair)
        return redirect(url_for('home'))
    return render_template('repair.html', legend = "New Repair For: " +  current_user.first_name + ' ' + current_user.last_name + '.', user_data = user_data, form = form)

def generate_order_number():
    gen_order_number = random.sample(range(123456,999999), 1)
    final_order_number = ''.join(str(o) for o in gen_order_number)
    return final_order_number

def send_repair_email(repair):
    form = RepairForm()
    powelltech_email = 'Powell.ind.inc@gmail.com'
    customer_email = current_user.email
    text = ""
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f'''Repair request received for {form.first_name.data}'''
    msg['From'] = "PowellTech Inc. ©"
    msg['To'] = customer_email
    html = render_template('repair_email.html')
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)
    mail = smtplib.SMTP_SSL('smtp.gmail.com', 465)

    mail.ehlo()

    mail.login(powelltech_email, 'Powell2019!')
    mail.sendmail(powelltech_email, customer_email, msg.as_string())
    mail.quit()

@app.route('/account', methods = ['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        current_user.password = form.password.data
        current_user.phone_number = form.phone_number.data
        db.session.commit()
        update_account_information_email(update_account_information_email)
        flash(f"Your account information has been updated {current_user.first_name}.")
        return redirect(url_for("home"))
    elif request.method == 'GET':
        form.email.data = current_user.email
    return render_template('account.html', legend=current_user.first_name + " " + current_user.last_name + "'s Account Details", form=form)

def update_account_information_email(update_account_information_email):
    form = UpdateAccountForm()
    powelltech_email = 'Powell.ind.inc@gmail.com'
    customer_email = current_user.email
    text = ''
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f'''Account information changed for {form.first_name.data}'''
    msg['From'] = "PowellTech Inc. ©"
    msg['To'] = customer_email
    html = render_template('update_account_information_email.html')
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)
    mail = smtplib.SMTP_SSL('smtp.gmail.com', 465)

    mail.ehlo()

    mail.login(powelltech_email, 'Powell2019!')
    mail.sendmail(powelltech_email, customer_email, msg.as_string())
    mail.quit()

@app.route('/adddevice', methods = ['GET', 'POST'])
@login_required
def addDevice():
    form = DeviceRegistrationForm()
    if form.validate_on_submit():
        device = Devices(email = current_user.email, device_name = form.device_name.data, owner_first_name = current_user.first_name, 
                        owner_last_name = current_user.last_name, device_manufacturer = form.device_manufacturer.data, 
                        device_model = form.device_model.data, serial_number = form.serial_number.data)
        db.session.add(device)
        db.session.commit()
        flash(f"{form.device_name.data} has been added to your devices list, {current_user.first_name}", 'success')
        return redirect(url_for('home'))
    return render_template('adddevice.html', form = form)

@app.route('/devices', methods = ['GET', 'POST'])
@login_required
def devices():
    user_data = Devices.query.filter_by(email = current_user.email).first()
    return render_template('devices.html', user_data = user_data)

@app.route('/devicerepair', methods = ['GET', 'POST'])
@login_required
def deviceRepair():
    form = RepairForm()
    user_data = Devices.query.filter_by(email = current_user.email).first()
    if form.validate_on_submit():
        order_number = generate_order_number()
        repair = Repair(first_name = form.first_name.data, last_name = form.last_name.data, email = form.email.data, 
                        phone_number = form.phone_number.data, issue = form.issue.data, troubleshooting = form.troubleshooting.data, 
                        device_model = form.device_model.data, device_manufacturer = form.device_manufacturer.data,
                        device_os = form.device_os.data, order_number = order_number, repair_status = "Received | Pending Acceptance")
        date = datetime.date.today()
        db.session.add(repair)
        db.session.commit()
        flash(f"Repair Request Created for: " + form.first_name.data + " " + form.last_name.data + " for " + form.device_manufacturer.data + " " + form.device_model.data + ". Your order ID is: " + order_number + ".", "success")
        send_repair_email(repair)
        return redirect(url_for('home'))
    return render_template('devicerepair.html', legend = "New Repair For: " +  current_user.first_name + " " + current_user.last_name + ".", user_data = user_data, form = form)

@app.route('/history', methods = ['GET', 'POST'])
@login_required
def repairHistory():
    response = requests.get('https://ipinfo.io/')
    data = response.json()
    city = data['city']
    state = data['region']
    user_data = Repair.query.all()
    print(user_data)
    return render_template('history.html', repair = repair, user_data = user_data, legend = "Repair History | " + current_user.first_name + " " + current_user.last_name, city = data['city'], state = data['region'])

@app.route('/testing', methods = ['GET', 'POST'])
@login_required
def siteEmailTest():
    user = User.query.filter_by(email=current_user.email).first()
    TEST_send_register_email(user)
    TEST_send_repair_email(repair)
    TEST_send_reset_email(user)            
    TEST_login_email()
    TEST_update_account_information_email(user)
    TEST_logout_email()
    return render_template('testing.html')

def systemEmailTestCheck():
    user = "powell.ind.inc@gmail.com"
    TEST_send_register_email(user)
    TEST_send_repair_email(user)
    TEST_send_reset_email(user)            
    TEST_login_email()
    TEST_update_account_information_email(user)
    TEST_logout_email()

def TEST_send_register_email(user):
    form = RegistrationForm()
    powelltech_email = 'Powell.ind.inc@gmail.com'
    customer_email = current_user.email
    msg = MIMEMultipart('alternative')
    text = ""
    msg['Subject'] = "Welcome to PowellTech!"
    msg['From'] = "PowellTech Inc. ©"
    msg['To'] = customer_email
    html = render_template('test_register_email.html')
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)
    mail = smtplib.SMTP_SSL('smtp.gmail.com', 465)

    mail.ehlo()

    mail.login(powelltech_email, 'Powell2019!')
    mail.sendmail(powelltech_email, customer_email, msg.as_string())
    mail.quit()

def TEST_send_repair_email(repair):
    form = RepairForm()
    powelltech_email = 'Powell.ind.inc@gmail.com'
    customer_email = current_user.email
    text = ""
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f'''Repair request received for {current_user.first_name}'''
    msg['From'] = "PowellTech Inc. ©"
    msg['To'] = customer_email
    html = render_template('test_repair_email.html')
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)
    mail = smtplib.SMTP_SSL('smtp.gmail.com', 465)

    mail.ehlo()

    mail.login(powelltech_email, 'Powell2019!')
    mail.sendmail(powelltech_email, customer_email, msg.as_string())
    mail.quit()

def TEST_send_reset_email(user):
    token = user.get_reset_token()
    form = RequestResetForm()
    powelltech_email = 'Powell.ind.inc@gmail.com'
    customer_email = current_user.email
    text = ""
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f'''Password Reset for {customer_email}'''
    msg['From'] = "PowellTech Inc. ©"
    msg['To'] = customer_email
    html = render_template('test_send_reset_email.html')
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)
    mail = smtplib.SMTP_SSL('smtp.gmail.com', 465)

    mail.ehlo()

    mail.login(powelltech_email, 'Powell2019!')
    mail.sendmail(powelltech_email, customer_email, msg.as_string())
    mail.quit()

def TEST_login_email():
    form = LoginForm()
    response = requests.get('https://ipinfo.io/')
    data = response.json()
    city = data['city']
    state = data['region']
    country = data['country']
    if country == "US":
        country = "United States of America"
    ts = calendar.timegm(time.gmtime())
    timestamp = time.ctime(ts)
    powelltech_email = 'Powell.ind.inc@gmail.com'
    customer_email = current_user.email
    text = ""
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f'''Sucessful login for {current_user.first_name}.'''
    msg['From'] = "PowellTech Inc. ©"
    msg['To'] = customer_email
    html = render_template('test_login_email.html', city = city, state = state, country = country, timestamp = timestamp)
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)
    mail = smtplib.SMTP_SSL('smtp.gmail.com', 465)

    mail.ehlo()

    mail.login(powelltech_email, 'Powell2019!')
    mail.sendmail(powelltech_email, customer_email, msg.as_string())
    mail.quit()

def TEST_update_account_information_email(update_account_information_email):
    form = UpdateAccountForm()
    powelltech_email = 'Powell.ind.inc@gmail.com'
    customer_email = current_user.email
    text = ""
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f'''Account information changed for {current_user.first_name}'''
    msg['From'] = "PowellTech Inc. ©"
    msg['To'] = customer_email
    html = render_template('test_update_account_information_email.html')
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)
    mail = smtplib.SMTP_SSL('smtp.gmail.com', 465)

    mail.ehlo()

    mail.login(powelltech_email, 'Powell2019!')
    mail.sendmail(powelltech_email, customer_email, msg.as_string())
    mail.quit()

def TEST_logout_email():
    powelltech_email = 'Powell.ind.inc@gmail.com'
    customer_email = current_user.email
    text = f"{current_user.first_name} has been logged out."
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f'''Successful logout for {current_user.first_name} {current_user.last_name}'''
    msg['From'] = "PowellTech Inc. ©"
    msg['To'] = customer_email
    html = render_template('test_logout_email.html')
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)
    mail = smtplib.SMTP_SSL('smtp.gmail.com', 465)

    mail.ehlo()

    mail.login(powelltech_email, 'Powell2019!')
    mail.sendmail(powelltech_email, customer_email, msg.as_string())
    mail.quit()