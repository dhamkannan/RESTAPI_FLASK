from flask import Flask, jsonify, request, Response
from settings import app
from dbModel import Doctor, Receipt, Product, Employee, Vendor
from functools import wraps
import datetime, jwt, json
from jsonschema import validate

schema = json.load(open("schema.json"))

#### Validate Object
def validate_object(request_data, object_name):
    try:
        return validate(request_data, schema[object_name])
    except Exception as e:
        return {'error' : e.message, 'expectedSchema' : e.schema}

#####Validate token
def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.args.get('token')
        try:
            jwt.decode(token, app.config['SECRET_KEY'])
            return func(*args, **kwargs)
        except:
            response = Response(jsonify({'error' : 'Need a valid token'}), 401, mimetype='application/json')
            return response
    return wrapper

#GET JWT token
@app.route('/login')
def get_token():
    expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
    token = jwt.encode({'exp' : expiration_date}, app.config['SECRET_KEY'], algorithm='HS256')
    return token

# / GET RECEIPTS
@app.route('/receipts')
# @token_required
def get_receipts():
    return(jsonify({'Receipts': Receipt.get_all_receipts()}))

#POST / Add a RECEIPT
@app.route('/receipts', methods=['POST'])
# @token_required
def add_receipt():
    request_data = request.get_json()
    validated_response = validate_object(request_data, 'receipt')
    if validated_response is None:
        Receipt.add_receipt(request_data['doctor_id'], request_data['salesman_id'], request_data['product_id'], request_data['total_price'])
        response = Response("", 201, mimetype='application/json')
        return response
    else:
        response = Response(json.dumps(validated_response), 400, mimetype='application/json')
        return response
    
# / GET Doctors
@app.route('/doctors')
# @token_required
def get_doctors():
    return(jsonify({'Doctors': Doctor.get_all_doctors()}))

#POST / Add a doctor
@app.route('/doctors', methods=['POST'])
# @token_required
def add_doctor():
    request_data = request.get_json()
    validated_response = validate_object(request_data, 'doctor')
    if validated_response is None:
        Doctor.add_doctor(request_data['first_name'], request_data['last_name'], request_data['hospital_name'], request_data['hospital_address'])
        response = Response("", 201, mimetype='application/json')
        return response
    else:
        response = Response(json.dumps(validated_response), 400, mimetype='application/json')
        return response

# / GET Employees
@app.route('/employees')
# @token_required
def get_employees():
    return(jsonify({'Employees': Employee.get_all_employees()}))

#POST / Add a employee
@app.route('/employees', methods=['POST'])
# @token_required
def add_employee():
    request_data = request.get_json()
    validated_response = validate_object(request_data, 'employee')
    if validated_response is None:
        Employee.add_employee(request_data['first_name'], request_data['last_name'], request_data['team'], request_data['home_address'])
        response = Response("", 201, mimetype='application/json')
        return response
    else:
        response = Response(json.dumps(validated_response), 400, mimetype='application/json')
        return response

# / GET Products
@app.route('/products')
# @token_required
def get_products():
    return(jsonify({'Products': Product.get_all_products()}))

#POST / Add a product
@app.route('/products', methods=['POST'])
# @token_required
def add_product():
    request_data = request.get_json()
    validated_response = validate_object(request_data, 'product')
    if validated_response is None:
        Product.add_product(request_data['product_name'], request_data['product_model'], request_data['stocks'], 
                        request_data['vendor_id'], request_data['price'])
        response = Response("", 201, mimetype='application/json')
        return response
    else:
        response = Response(json.dumps(validated_response), 400, mimetype='application/json')
        return response

# / GET Vendors
@app.route('/vendors')
# @token_required
def get_vendors():
    return(jsonify({'Vendors': Vendor.get_all_vendors()}))

#POST / Add a vendor
@app.route('/vendors', methods=['POST'])
# @token_required
def add_vendor():
    request_data = request.get_json()
    validated_response = validate_object(request_data, 'vendor')
    if validated_response is None:
        Vendor.add_vendor(request_data['vendor_name'], request_data['vendor_address'])
        response = Response("", 201, mimetype='application/json')
        return response
    else:
        response = Response(json.dumps(validated_response), 400, mimetype='application/json')
        return response


app.run(port=5001)