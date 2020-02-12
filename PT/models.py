import sqlalchemy

from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from PT import db, login_manager, app
from flask_login import UserMixin
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    phone_number = db.Column(db.String(12), nullable=False)
    account_type = db.Column(db.String(), nullable=False)
    created_by = db.Column(db.String(), nullable=False)
    employee_id = db.Column(db.String())
    department = db.Column(db.String())

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.first_name}', '{self.email}',)"

class Repair(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    order_number = db.Column(db.String())
    created_date = db.Column(db.String(), nullable=False)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    phone_number = db.Column(db.String(), nullable=False)
    issue = db.Column(db.String(1800), nullable=False)
    troubleshooting = db.Column(db.String(1800))
    device_manufacturer = db.Column(db.String(), nullable=False)
    device_model = db.Column(db.String(), nullable=False)
    device_os = db.Column(db.String(), nullable=False)
    otp_troubleshooting = db.Column(db.Boolean())
    repair_price = db.Column(db.String())
    repair_status = db.Column(db.String())
    invoice_due_date = db.Column(db.String())

    def __repr__(self):
        return f"Repair('{self.first_name}', '{datetime.date}')"

class Subscription(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(), nullable=False)

class AdminAccess(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    phone_number = db.Column(db.String(), nullable=False)
    access_type = db.Column(db.String(), nullable=False)
    accessed_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    department = db.Column(db.String())

class Invoices(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    order_number = db.Column(db.String())
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    phone_number = db.Column(db.String(), nullable=False)
    issue = db.Column(db.String(1800), nullable=False)
    device_manufacturer = db.Column(db.String(), nullable=False)
    device_model = db.Column(db.String(), nullable=False)
    device_os = db.Column(db.String(), nullable=False)
    repair_price = db.Column(db.String(), nullable=False)
    parts_price = db.Column(db.String(), nullable=False)
    labor = db.Column(db.String(), nullable=False)
    promotions = db.Column(db.String(), nullable=False)
    completed_by = db.Column(db.String(), nullable=False)
    completed_on = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    return_address = db.Column(db.String())
    return_type = db.Column(db.String(), nullable=False)
    invoice_due_date = db.Column(db.String())
    repair_status = db.Column(db.String())

class Devices(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(), nullable=False)
    device_name = db.Column(db.String(), nullable=False)
    owner_first_name = db.Column(db.String(), nullable=False)
    owner_last_name = db.Column(db.String(), nullable=False)
    device_manufacturer = db.Column(db.String(), nullable=False)
    device_model = db.Column(db.String(), nullable=False)
    serial_number = db.Column(db.String(), nullable=False)