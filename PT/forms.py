from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, SubmitField, IntegerField, BooleanField, PasswordField, TextField, SelectField
from wtforms.validators import Email, ValidationError, DataRequired, EqualTo, Length
from PT.models import User, Repair, Subscription, AdminAccess, Invoices

class RegistrationForm(FlaskForm):
    first_name = StringField("What is your first name?",
        validators=[DataRequired(), Length(max=20)])
    last_name = StringField("What is your last name?",
        validators=[DataRequired(), Length(max=20)])
    email = StringField("What is your email address?",
        validators=[DataRequired(), Email()])
    confirm_email = StringField("Confirm your email address.",
        validators=[DataRequired(), EqualTo("email")])
    password = PasswordField("Create a password.",
        validators=[DataRequired(), Length(min=8, max=120)])
    confirm_password = PasswordField("Confirm your password.",
        validators=[DataRequired(), EqualTo("password")])
    phone_number = IntegerField("What is your phone number?",
        validators=[DataRequired()])
    terms_and_conditions = BooleanField("Accept Terms and Conditions:",
        validators=[DataRequired()])
    submit = SubmitField("Create Account")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Hmm, it appears we already have a PowellTech account associated with that e-mail address, please check the spelling of your e-mail address or login.")

class AdminRegistrationForm(FlaskForm):
    first_name = StringField("First Name",
        validators=[DataRequired(), Length(max=20)])
    last_name = StringField("Last Name",
        validators=[DataRequired(), Length(max=20)])
    email = StringField("Email Address",
        validators=[DataRequired(), Email()])
    confirm_email = StringField("Confirm Email Address",
        validators=[DataRequired(), EqualTo("email")])
    password = PasswordField("Temporary Password",
        validators=[DataRequired(), Length(min=8, max=120)])
    confirm_password = PasswordField("Confirm Temporary Password",
        validators=[DataRequired(), EqualTo("password")])
    phone_number = IntegerField("Phone Number",
        validators=[DataRequired()])
    employee_id = StringField("Employee Identification Number",
        validators=[DataRequired(), Length(min=6, max=6)])
    confirm_employee_id = StringField("Confirm Employee Identification Number",
        validators=[DataRequired(), EqualTo("employee_id"), Length(min=6, max=6)])
    department = StringField("Employee's Department Name",
        validators=[DataRequired()])
    submit = SubmitField("Add To Database")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                "There is an account in the database associated with that e-mail address.")

class LoginForm(FlaskForm):
    email = StringField("E-mail Address:",
        validators=[DataRequired(), Email()])
    password = PasswordField("Password:",
        validators=[DataRequired()])
    remember = BooleanField("Would you like to use QuickLogon?")
    submit = SubmitField("Sign In")

    def validate_login_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user == None:
            raise ValidationError("Hmm, it appears we do not have a PowellTech account associated with that e-mail address, please check the spelling of your e-mail address or register.")

class RepairForm(FlaskForm):
    first_name = StringField("First Name:",
        validators=[DataRequired(), Length(max=20)])
    last_name = StringField("Last Name:",
        validators=[DataRequired(), Length(max=20)])
    email = StringField("E-mail Address:",
        validators=[DataRequired(), Email()])
    phone_number = IntegerField("What is a contact phone number?",
        validators=[DataRequired()])
    issue = TextField("What issue are you having?",
        validators=[DataRequired(), Length(min=20, max=1800)])
    troubleshooting = TextField("What have you done to resolve this issue? (If applicable)",
        validators=[Length(max=1800)])
    device_manufacturer = StringField("Who made the device?",
        validators=[Length(max=50)])
    device_model = StringField("What is your device's model?",
        validators=[Length(max=50)])
    device_os = StringField("What operating system is your device running?",
        validators=[Length(max=50)])
    otp_troubleshooting = SelectField("Would you like to attempt over the phone troubleshooting first?",
        choices = [('Y', 'Yes (We will have you mail it in if necessary.)'),('N', 'No, just mail it in.')])
    terms_and_conditions = BooleanField("Accept Terms and Conditions:",
        validators=[DataRequired()])
    submit = SubmitField("Submit Repair Request")

class RequestResetForm(FlaskForm):
    email = StringField("E-mail Address:",
        validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset Link")

class ResetPasswordForm(FlaskForm):
    password = PasswordField("New Password:",
        validators=[DataRequired()])
    confirm_password = PasswordField("Confirm New Password:",
        validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Reset Password")

class UpdateAccountForm(FlaskForm):
    first_name = StringField("First Name:",
        validators=[DataRequired(), Length(max=20)])
    last_name = StringField("Last Name:",
        validators=[DataRequired(), Length(max=20)])
    email = StringField("E-mail Address",
        validators=[DataRequired(), Email()])
    password = PasswordField("New Password")
    confirm_password = PasswordField("Confirm New Password",
        validators=[EqualTo('password')])
    phone_number = IntegerField("Phone Number:",
        validators=[DataRequired()])
    submit = SubmitField("Update Account Information")

    def validate_new_email(self, email):
        if form.email.data != current_user.email:
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                raise ValidationError("It appears there's already an account with that email. Please select a different one.")

class SiteEmailTestingForm(FlaskForm):
    test_username = StringField("Administrator or CEO Username",
        validators=[DataRequired()])
    test_password = PasswordField("Admistrator or CEO Password",
        validators=[DataRequired()])
    submit = SubmitField("Run Email Site Test")

class SubscriptionForm(FlaskForm):
    email = StringField("Please enter your e-mail address...",
        validators=[Email()])
    submit = SubmitField("SUBSCRIBE")

class InvoiceForm(FlaskForm):
    order_number = StringField("Customer's Order Number:",
        validators=[DataRequired()])
    first_name = StringField("Customer's First Name:",
        validators=[DataRequired(), Length(max=20)])
    last_name = StringField("Customer's Last Name:",
        validators=[DataRequired(), Length(max=20)])
    email = StringField("Customer's E-mail Address:",
        validators=[DataRequired(), Email()])
    phone_number = StringField("Customer's Phone Number:",
        validators=[DataRequired()])
    issue = TextField("Device issue:",
        validators=[DataRequired(), Length(min=20, max=1800)])
    device_manufacturer = StringField("Device Manufacturer:",
        validators=[Length(max=50)])
    device_model = StringField("Device Model:",
        validators=[Length(max=50)])
    device_os = StringField("Final Repair Operating System:",
        validators=[Length(max=50)])
    parts_price = StringField("Price for part(s) - 0 for software-related issues.",
        validators=[DataRequired()])
    labor = StringField("Price for labor:",
        validators=[DataRequired()])
    promotions = StringField("Total promotion discount(s):",
        validators=[DataRequired()])
    repair_price = StringField("Total repair price:",
        validators=[DataRequired()])
    return_type = StringField("Ship or pick up?",
        validators=[DataRequired()])
    return_address = StringField("Return shipping address")
    submit = SubmitField("Create and Send Invoice")

class DeviceRegistrationForm(FlaskForm):
    device_name = StringField("Name this device:",
        validators=[DataRequired()])
    owner_first_name = StringField("Owner's First Name:",
        validators=[DataRequired()])
    owner_last_name = StringField("Owner's Last Name:",
        validators=[DataRequired()])
    device_manufacturer = StringField("Who made this device?",
        validators=[DataRequired()])
    device_model = StringField("Device's Model:",
        validators=[DataRequired()])
    serial_number = StringField("Device's Serial Number:",
        validators=[DataRequired()])
    submit = SubmitField("Register Device")