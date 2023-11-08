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

#Invoice Model
class InvItem(db.Model):
    __bind_key__ = 'db3'
    id = db.Column(db.Integer, primary_key=True)
    inv_num = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    order_num = db.Column(db.Integer, nullable=False) #may be able to make this foreign key to item
    part_name = db.Column(db.String(100), nullable=False) #may need to change this to part_num
    price_spent = db.Column(db.Float, nullable=False)
    date = db.Column(db.String(100), nullable=True)
    description = db.Column(db.String(200), nullable=True)

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
@app.route('/invoiceInventoryCards')
def invoiceInventoryCards():
    items = InvItem.query.all()
    return render_template('invoice_inventory_bsCard.html', items=items)

@app.route('/invoiceAddTo')
def invoiceAddTo():
    return render_template('invoices_addTo.html')

@app.route('/invoiceInventoy')
def invoiceInventory():
    items = InvItem.query.all()
    return render_template('invoices_inventory.html', items=items)

@app.route('/invoiceUpdate')
def invoiceUpdate():
    return render_template('invoices_update.html')

@app.route('/add_invoice', methods=['POST'])
def add_invoice():
    invItem = InvItem(
        inv_num=int(request.form['inv_num']),
        name=str(request.form['name']),
        order_num=int(request.form['order_num']),
        part_name=str(request.form['part_name']),
        price_spent=float(request.form['price_spent']),
        date=request.form['date'],
        description=request.form['description']
    )
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
    item.inv_num = int(request.form['inv_num'])
    item.name = str(request.form['name'])
    item.order_num = int(request.form['order_num'])
    item.part_name = str(request.form['part_name'])
    item.price_spent = float(request.form['price_spent'])
    item.date = request.form['date']
    item.description = request.form['description']
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