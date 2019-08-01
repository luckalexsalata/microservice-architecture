from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask, redirect, url_for,request,render_template,jsonify
from redis import Redis
import json




app = Flask(__name__)
r = Redis(host='redis', port=6379)
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app_settings = os.getenv('APP_SETTINGS')  # new
app.config.from_object(app_settings)
db = SQLAlchemy(app)

class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String)
    weight = db.Column(db.Integer, unique = False)

    def __init__(self, product_name, weight):
        self.product_name = product_name
        self.weight = weight


db.create_all()
pn = 'tomato'
w = 50
pr = Product(pn,w)
db.session.add(pr)

pn = 'dough'
w = 100
pr = Product(pn,w)
db.session.add(pr)

pn = 'cheese'
w = 25
pr = Product(pn,w)
db.session.add(pr)

pn = 'sausage'
w = 25
pr = Product(pn,w)
db.session.add(pr)

db.session.commit()

@app.route('/')
def storage():
    products = Product.query.all()
    result = [product for product in products ]
    return render_template('storage.html', items = result)



@app.route('/new_storage', methods = ['POST'])
def red():
    newProduct = request.form['product_name']
    newWeight = request.form['weight']
    item_doc = {
        'Product': str(request.form['product_name']),
        'Weight': str(request.form['weight']),
    }

    update_save = json.dumps(item_doc)

    r.set('update', update_save)
    #product = Product(newProduct,newWeight)
    update = Product.query.filter_by(product_name = newProduct).first()
    update.weight = newWeight
    #db.session.add(product)
    db.session.commit()
    return redirect(url_for('storage'))

@app.route('/add', methods = ['POST'])
def add_product():
    addProduct = request.form['product_name']
    addWeight = request.form['weight']
    item_doc = {
        'Product': str(request.form['product_name']),
        'Weight': str(request.form['weight']),
    }
    if bool(Product.query.filter_by(product_name = addProduct).first()) == True:
        return redirect(url_for('storage'))
    update_save = json.dumps(item_doc)
    r.set('update', update_save)
    product = Product(addProduct,addWeight)
    #update = Product.query.filter_by(product_name = newProduct).first()
    #update.weight = newWeight
    db.session.add(product)
    db.session.commit()

    return redirect(url_for('storage'))

@app.route('/del', methods=['POST'])
def delete():
    delProduct = request.form['product_name']
    product = Product.query.filter_by(product_name = delProduct).first()
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('storage'))

if __name__ == "__main__":
    app.run('0.0.0.0', 8080)