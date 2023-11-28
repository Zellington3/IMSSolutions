from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from jinja2 import Template
from datetime import datetime, timedelta

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders_inventory.db'
app.config['SQLALCHEMY_BINDS'] = { 'db2': 'sqlite:///parts_inventory.db',
                                   'db3': 'sqlite:///invoice_inventory.db',
                                   'dblogin': 'sqlite:///login_signup.db' }
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#Functions------------------------------------------------------
@app.route('/status_color/<status>')
def status_color(status):
    if status == 'Done':
        return 'Status_Done.png'
    elif status == 'In Progress':
        return 'Status_InProgress.png'
    elif status == 'Waiting':
        return 'Status_Waiting.png'
    else:
        return 'Status_Problem.png'

#MODELS FOR DBS------------------------------------------------------------
#ORDER MODEL
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), nullable = False)
    order_number = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    make = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    mileage = db.Column(db.Integer, nullable=False)
    work_needed = db.Column(db.String(200), nullable=False)
    parts = db.Column(db.String(200), nullable=True)
    total = db.Column(db.Float, nullable=False)
    inv_num = db.Column(db.String(50), nullable=True)
    description = db.Column(db.String(200), nullable=True)
    date = db.Column(db.String(50), nullable=False) 

    def __repr__(self):
        return f'<Item {self.name}>'
    
#PART MODEL
class PartItem(db.Model):
    __bind_key__ = 'db2'
    id = db.Column(db.Integer, primary_key=True)
    part_number = db.Column(db.String(100), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    cost_price = db.Column(db.Float, nullable=False)
    selling_price = db.Column(db.Float, nullable=False)
    dimensions = db.Column(db.String(100), nullable=True)
    warranty_info = db.Column(db.String(100), nullable=True)
    date = db.Column(db.String(50), nullable=False) 
    description = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f'<PartItem {self.name}>'

class InvItem(db.Model):
    __bind_key__ = 'db3'
    id = db.Column(db.Integer, primary_key=True)
    inv_num = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    order_num = db.Column(db.Integer, nullable=False)  
    year = db.Column(db.Integer, nullable=False)  
    make = db.Column(db.String(50), nullable=False) 
    model = db.Column(db.String(50), nullable=False) 
    mileage = db.Column(db.Float, nullable=True) 
    work_done = db.Column(db.String(200), nullable=False)  
    part_numbers = db.Column(db.String(100), nullable=False) 
    parts_used = db.Column(db.String(200), nullable=False)  
    total_price = db.Column(db.Float, nullable=False)  
    price_owed = db.Column(db.Float, nullable=False)  
    payment_method = db.Column(db.String(50), nullable=False)  
    time_worked_on = db.Column(db.String(50), nullable=True)
    date = db.Column(db.String(50), nullable=False)  
    description = db.Column(db.String(200), nullable=True)
    

    def __repr__(self):
        return f'<InvItem {self.name}>'
    
class LoginInfo(db.Model):
    __bind_key__ = 'dblogin'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(320), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<LoginInfo {self.name}>'
#----------------------------------------------------
#APPROUTES FOR ORDERS UNDER THIS SECTIO
def process_order_form(item, form_data):
    # Extract data from the form and assign it to the corresponding fields in the Item object
    item.order_number = int(form_data['order_number'])
    item.status = form_data['status']
    item.year = int(form_data['year'])
    item.make = form_data['make']
    item.model = form_data['model']
    item.mileage = int(form_data['mileage'])
    item.work_needed = form_data['work_needed']
    item.parts = form_data['parts']
    item.total = float(form_data['total'])
    item.inv_num = form_data['inv_num']
    item.date = form_data['date']
    item.description = form_data['description']

@app.route('/orderInventory')
def orderInventory():
    items = Item.query.all()
    return render_template('orders_inventory.html', items=items, status_color=status_color)

@app.route('/orders_addTo')
def ordersAddTo():
    return render_template('orders_addTo.html', status_color=status_color)


@app.route('/edit_order/<int:item_id>')
def edit_order(item_id):
    item = Item.query.get(item_id)
    return render_template('orders_update.html', item=item)

@app.route('/add_order', methods=['POST'])
def add_order():
    form_data = request.form.to_dict()
    item = Item()
    process_order_form(item, form_data)
    db.session.add(item)
    db.session.commit()
    items = Item.query.all() 
    return render_template('orders_inventory.html', items=items, status_color=status_color)

@app.route('/delete_order/<int:item_id>', methods=['POST'])
def delete_order(item_id):
    item = Item.query.get(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('orderInventory'))

@app.route('/update_order/<int:item_id>', methods=['POST'])
def update_order(item_id):
    item = Item.query.get(item_id)
    form_data = request.form.to_dict()
    process_order_form(item, form_data)
    db.session.commit()
    return redirect(url_for('orderInventory'))

#-------------------------------------------------------------------------------------------------------------------------------
#UNDER THIS SECTION HAS TO DO WITH PARTS
def process_part_form(item, form_data):
    # Extract data from the form and assign it to the corresponding fields in the PartItem object
    item.part_number = form_data['part_number']
    item.name = form_data['name']
    item.quantity = int(form_data['quantity'])
    item.cost_price = float(form_data['cost_price'])
    item.selling_price = float(form_data['selling_price'])
    item.dimensions = form_data['dimensions']
    item.warranty_info = form_data['warranty_info']
    item.date = form_data['date']
    item.description = form_data['description']

@app.route('/part_addTo')
def partAddTo():
    return render_template('parts_addTo.html')

@app.route('/part_inventory')
def partInventory():
    items = PartItem.query.all()
    return render_template('parts_inventory.html', parts=items)

@app.route('/add_part', methods=['POST'])
def add_part():
    form_data = request.form.to_dict()
    item = PartItem()
    process_part_form(item, form_data)
    db.session.add(item)
    db.session.commit()
    return redirect(url_for('partInventory'))

@app.route('/delete_part/<int:item_id>', methods=['POST'])
def delete_part(item_id):
    item = PartItem.query.get(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('partInventory'))

@app.route('/update_part/<int:item_id>', methods=['POST'])
def update_part(item_id):
    item = PartItem.query.get(item_id)
    form_data = request.form.to_dict()
    process_part_form(item, form_data)
    db.session.commit()
    return redirect(url_for('partInventory'))

@app.route('/edit_part/<int:item_id>')
def edit_part(item_id):
    item = PartItem.query.get(item_id)
    return render_template('parts_update.html', item=item)

#--------------------------------------------------------------------------------
#UNDER THIS SECTION HAS TO DO WITH INVOICES

def process_invoice_form(item, form_data):
    # Extract data from the form and assign it to the corresponding fields in the InvItem object
    item.inv_num = int(form_data['inv_num'])
    item.name = str(form_data['name'])
    item.order_num = int(form_data['order_num'])
    item.part_numbers = str(form_data['part_numbers'])
    item.year = int(form_data['year']) 
    item.make = str(form_data['make']) 
    item.model = str(form_data['model']) 
    item.mileage = float(form_data['mileage']) if form_data['mileage'] else None 
    item.work_done = str(form_data['work_done']) 
    item.parts_used = str(form_data['parts_used']) 
    item.total_price = float(form_data['total_price'])
    item.price_owed = float(form_data['price_owed']) 
    item.payment_method = str(form_data['payment_method'])   
    item.time_worked_on = str(form_data['time_worked_on']) if form_data['time_worked_on'] else None 
    item.description = str(form_data['description']) if form_data['description'] else None  
    item.date = str(form_data['date']) 

@app.route ('/invoice_addTo')
def invoiceAddTo():
    return render_template('invoices_addTo.html')

@app.route('/invoiceInventory')
def invoiceInventory():
    items = InvItem.query.all()
    return render_template('invoices_inventory.html', items=items)

@app.route('/addInvoice', methods=['POST'])
def add_invoice():
    form_data = request.form.to_dict()
    invItem = InvItem()
    process_invoice_form(invItem, form_data)
    db.session.add(invItem)
    db.session.commit()
    return redirect(url_for('invoiceInventory'))

@app.route('/deleteInvoice/<int:item_id>', methods=['POST'])
def delete_invoice(item_id):
    item = InvItem.query.get(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('invoiceInventory'))

@app.route('/update_invoice/<int:item_id>', methods=['POST'])
def update_invoice(item_id):
    item = InvItem.query.get(item_id)
    form_data = request.form.to_dict()
    process_invoice_form(item, form_data)
    db.session.commit()
    return redirect(url_for('invoiceInventory'))

@app.route('/editInvoice/<int:item_id>')
def edit_invoice(item_id):
    item = InvItem.query.get(item_id)
    return render_template('invoices_update.html', item=item)

#---------------------------------------------------------------
#under this section is login and signup

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('index.html')

@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

#LOGIN AND SIGNUP--------------------------------------------------------
@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/login_route', methods=['POST'])
def login_route():
    # Get user input from the form
    email = request.form.get('email')
    password = request.form.get('pswd')
    # Check if it's an admin login
    if email == 'admin@gmail.com' and password == 'password':
        # Redirect to the admin page on successful admin login
        return redirect(url_for('admin_dashboard'))
    # Query the database for user authentication
    if is_valid_user(email, password):
        # Redirect to the homepage on successful login
        return redirect(url_for('homepage'))
    else:
        # Redirect back to the login page with an error message
        return render_template('index.html', error="Invalid credentials")

@app.route('/signup_route', methods=['POST'])
def signup_route():
    # Get user input from the form
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    # Check if both email and username are unique
    if not is_email_unique(email, username):
        return render_template('index.html', error="Email or username is already in use")
    # Hash the password before storing it in the database
    hashed_password = hash_password(password)
    # Create a new user
    new_user = LoginInfo(username=username, email=email, password=hashed_password)
    # Add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    # Redirect to the login page on successful signup
    return redirect(url_for('homepage'))

# Update the function to query the database for user authentication
def is_valid_user(email, password):
    user = LoginInfo.query.filter_by(email=email).first()
    return user is not None and check_password(password, user.password)

# Function to check if the email is unique (replace this with your own logic)
# Update the method to check if both email and username are unique
def is_email_unique(email, username):
    email_exists = LoginInfo.query.filter_by(email=email).first() is not None
    username_exists = LoginInfo.query.filter_by(username=username).first() is not None
    return not (email_exists or username_exists)

def hash_password(password):
    # Hash the password
    hashed_password = generate_password_hash(password)
    return hashed_password

def check_password(input_password, hashed_password):
    # Check if the input password matches the hashed password
    return check_password_hash(hashed_password, input_password)

#main-------------------------------------------------------------
from flask import url_for

if __name__ == '__main__':
    app.run(debug=True)
