from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from jinja2 import Template

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders_inventory.db'
app.config['SQLALCHEMY_BINDS'] = { 'db2': 'sqlite:///parts_inventory.db',
                                   'db3': 'sqlite:///invoice_inventory.db'}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#MODELS FOR DBS------------------------------------------------------------
#TODO Make sure the information in each database makes sense this isnt finalized.
#ORDER MODEL
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    cost_price = db.Column(db.Float, nullable=False)
    selling_price = db.Column(db.Float, nullable=False)
    date = db.Column(db.String(100), nullable=True)
    description = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f'<Item {self.name}>'
    
#PART MODEL
class PartItem(db.Model):
    __bind_key__ = 'db2'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    cost_price = db.Column(db.Float, nullable=False)
    selling_price = db.Column(db.Float, nullable=False)
    date = db.Column(db.String(100), nullable=True)
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
    description = db.Column(db.String(200), nullable=True)
    date = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<InvItem {self.name}>'
#----------------------------------------------------
#APPROUTES FOR ORDERS UNDER THIS SECTION
@app.route('/update_ajax/<int:item_id>', methods=['POST'])
def update_item_ajax(item_id):
    item = Item.query.get(item_id)
    data = request.json
    field = data['field']
    value = data['value']

    if field == 'name':
        item.name = value
    elif field == 'quantity':
        item.quantity = int(value)
    elif field == 'cost_price':
        item.cost_price

@app.route('/ordersAddTo')
def ordersAddTo():
    return render_template('orders_addTo.html')

@app.route('/order_view/<int:item_id>')
def order_view(item_id):
    item = Item.query.get(item_id)
    return render_template('orders_view.html', item=item)

@app.route('/inventoryCards')
def inventoryCards():
    items = Item.query.all()
    return render_template('orders_inventory_bsCard.html', items=items)

@app.route('/inventory')
def inventory():
    items = Item.query.all()
    return render_template('orders_inventory.html', items=items)

@app.route('/add', methods=['POST'])
def add_item():
    item = Item(
        name=request.form['name'],
        quantity=int(request.form['quantity']),
        cost_price=float(request.form['cost_price']),
        selling_price=float(request.form['selling_price']),
        date=request.form['date'],
        description=request.form['description']
    )
    db.session.add(item)
    db.session.commit()
    return redirect(url_for('inventory'))

@app.route('/edit/<int:item_id>')
def edit_item(item_id):
    item = Item.query.get(item_id)
    return render_template('orders_update.html', item=item)

@app.route('/update/<int:item_id>', methods=['POST'])
def update_item(item_id):
    item = Item.query.get(item_id)
    item.name = request.form['name']
    item.quantity = int(request.form['quantity'])
    item.cost_price = float(request.form['cost_price'])
    item.selling_price = float(request.form['selling_price'])
    item.date = request.form['date']
    item.description = request.form['description']
    db.session.commit()
    return redirect(url_for('inventory'))

@app.route('/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    item = Item.query.get(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('inventory'))



#-------------------------------------------------------------------------------------------------------------------------------
#UNDER THIS SECTION HAS TO DO WITH PARTS
@app.route('/partInventoryCards')
def partInventoryCards():
    items = PartItem.query.all()
    return render_template('parts_inventory_bsCard.html', parts=items)

@app.route('/partAddTo')
def partAddTo():
    return render_template('parts_addTo.html')

@app.route('/parts_view/<int:item_id>')
def parts_view(item_id):
    item = PartItem.query.get(item_id)
    return render_template('parts_view.html', item=item)

@app.route('/partInventoy')
def partInventory():
    items = PartItem.query.all()
    return render_template('parts_inventory.html', parts=items)

@app.route('/partUpdate')
def partUpdate():
    return render_template('parts_update.html')

@app.route('/add_part', methods=['POST'])
def add_part():
    partItem = PartItem(
        name=request.form['name'],
        quantity=int(request.form['quantity']),
        cost_price=float(request.form['cost_price']),
        selling_price=float(request.form['selling_price']),
        date=request.form['date'],
        description=request.form['description']
    )
    db.session.add(partItem)
    db.session.commit()
    return redirect(url_for('partInventory'))

@app.route('/deletePart/<int:item_id>', methods=['POST'])
def delete_part(item_id):
    item = PartItem.query.get(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('partInventory'))

@app.route('/update_part/<int:item_id>', methods=['POST'])
def update_part(item_id):
    item = PartItem.query.get(item_id)
    item.name = request.form['name']
    item.quantity = int(request.form['quantity'])
    item.cost_price = float(request.form['cost_price'])
    item.selling_price = float(request.form['selling_price'])
    item.date = request.form['date']
    item.description = request.form['description']
    db.session.commit()
    return redirect(url_for('partInventory'))

@app.route('/editPart/<int:item_id>')
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

@app.route('/invoices')
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

#main-------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)