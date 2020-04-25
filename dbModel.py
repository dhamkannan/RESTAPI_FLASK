import json
import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from settings import app

db = SQLAlchemy(app)

class Doctor(db.Model):
    __tablename__ = 'Doctors'
    doctor_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    hospital_name = db.Column(db.String(20))
    hospital_address = db.Column(db.String(50))
    receipt_relation = db.relationship("Receipt")

    def json(self):
        return {'doctor_id' : self.doctor_id, 'first_name' : self.first_name, 'last_name' : self.last_name, 
                'hospital_name' : self.hospital_name, 'hospital_address' : self.hospital_address }

    def add_doctor(_first_name, _last_name, _hospital_name, _hospital_address):
        new_doctor = Doctor(first_name=_first_name, last_name=_last_name, hospital_name=_hospital_name, 
                                hospital_address=_hospital_address)
        db.session.add(new_doctor)
        db.session.commit()

    def get_all_doctors():
        return [Doctor.json(doctor) for doctor in Doctor.query.all()]

class Vendor(db.Model):
    __tablename__ = 'Vendors'
    vendor_id = db.Column(db.Integer, primary_key=True)
    vendor_name = db.Column(db.String(20), nullable=False)
    vendor_address = db.Column(db.String(50))
    receipt_relation = db.relationship("Product")

    def json(self):
        return {'vendor_id' : self.vendor_id, 'vendor_name' : self.vendor_name, 'vendor_address' : self.vendor_address }

    def add_vendor(_vendor_name, _vendor_address):
        new_vendor = Vendor(vendor_name=_vendor_name, vendor_address=_vendor_address)
        db.session.add(new_vendor)
        db.session.commit()

    def get_all_vendors():
        return [Vendor.json(vendor) for vendor in Vendor.query.all()]

class Employee(db.Model):
    __tablename__ = 'Employees'
    employee_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    team = db.Column(db.String(10), nullable=False)
    home_address = db.Column(db.String(50))
    receipt_relation = db.relationship("Receipt")

    def json(self):
        return {'employee_id' : self.employee_id, 'first_name' : self.first_name, 'last_name' : self.last_name, 
                'team' : self.team, 'home_address' : self.home_address }

    def add_employee(_first_name, _last_name, _team, _home_address):
        new_employee = Employee(first_name=_first_name, last_name=_last_name, team=_team, home_address=_home_address)
        db.session.add(new_employee)
        db.session.commit()

    def get_all_employees():
        return [Employee.json(employee) for employee in Employee.query.all()]

class Product(db.Model):
    __tablename__ = 'Products'
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(20), nullable=False)
    product_model = db.Column(db.String(20), nullable=False)
    stocks = db.Column(db.Integer, nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey('Vendors.vendor_id'), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    receipt_relation = db.relationship("Receipt")

    def json(self):
        return {'product_id' : self.product_id, 'product_name' : self.product_name, 'product_model' : self.product_model, 
                'stocks' : self.stocks, 'vendor_id' : self.vendor_id, 'price' : str(self.price) }

    def add_product(_product_name, _product_model, _stocks, _vendor_id, _price):
        new_product = Product(product_name=_product_name, product_model=_product_model, stocks=_stocks, vendor_id=_vendor_id,
                                price=_price)
        db.session.add(new_product)
        db.session.commit()

    def get_all_products():
        return [Product.json(product) for product in Product.query.all()]

class Receipt(db.Model):
    __tablename__ = 'Receipts'
    receipt_id = db.Column(db.Integer, primary_key=True)
    docter_id = db.Column(db.Integer, db.ForeignKey('Doctors.doctor_id'), nullable=False)
    salesman_id = db.Column(db.Integer, db.ForeignKey('Employees.employee_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('Products.product_id'), nullable=False)
    receipt_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    total_price = db.Column(db.Numeric(10,2), nullable=False)

    def json(self):
        return {'receipt_id' : self.receipt_id, 'docter_id' : self.docter_id, 'salesman_id' : self.salesman_id, 
                'product_id' : self.product_id, 'receipt_date' : self.receipt_date, 'total_price' : str(self.total_price) }

    def add_receipt(_docter_id, _salesman_id, _product_id, _total_price):
        new_receipt = Receipt(docter_id=_docter_id, salesman_id=_salesman_id, product_id=_product_id, total_price=_total_price)
        db.session.add(new_receipt)
        db.session.commit()

    def get_all_receipts():
        return [Receipt.json(receipt) for receipt in Receipt.query.all()]