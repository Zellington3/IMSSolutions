# IMS Solutions

## Technological Stack:

* Python 3
* Flask v 2.2.3
* Flask_sqlalchemy v 3.0.3
* SQLAlchemy v 2.0.10
* Jinja2 v 3.1.2

## Project Installation:

Assuming that you already have python3 and pip installed, you have to install all the libraries by using following commands:

```
pip install flask==2.2.3
pip install jinja2==3.1.2
pip install SQLAlchemy==2.0.10
pip install flask_sqlalchemy==3.0.3
```

After installing all the libraries, in order to run this app you should use following command:

```
python3 init_db.py
python3 app.py
```

After running the python scripts there will be a popup that shows that the website should be running at http://127.0.0.1:5000

Click on this link to run on your local port!

## Project Description:

This is an inventory web application that allows small buisness owners to keep track of their orders, parts, and invoices. They can add items to their respective tables by providing details about them, like:

#ORDERS TABLE
* Name
* Quantity
* Cost Price
* Selling Price
* Date (optional)
* Description (optional)
  

#PARTS TABLE
* Name
* Quantity
* Cost Price
* Selling Price
* Date (Optional)
* Description ( optional)
  

#INVOICES TABLE
* Invoice Number
* Name
* Order Number
* Part Name
* Price Spent 
* Date (Optional)
* Description ( optional)

Also, users can search for items in the table by their name, update, delete or add information about the order, part, or invoice, from the inventory.

## Contributors:

*Zach Ellington
