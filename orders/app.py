#!/usr/bin/env python3
from flask import Flask, redirect, url_for,request,render_template
from pymongo import MongoClient
from redis import Redis
import os
from rq import Queue
import json
app = Flask(__name__)
r = Redis(host='redis', port=6379)
MongoClient('db-1', replicaSet='rs0', serverSelectionTimeoutMS=5000, socketTimeoutMS=5000, connectTimeoutMS=5000)
MongoClient('db-2', replicaSet='rs0', serverSelectionTimeoutMS=5000, socketTimeoutMS=5000, connectTimeoutMS=5000)
MongoClient('db-3', replicaSet='rs0', serverSelectionTimeoutMS=5000, socketTimeoutMS=5000, connectTimeoutMS=5000)

db = MongoClient('db-1', replicaSet='rs0', serverSelectionTimeoutMS=5000, socketTimeoutMS=5000, connectTimeoutMS=5000
).test

#db_1 = client.tododb
@app.route('/')
def orders():
    _items = db.tododb.find()
    items = [item for item in _items ]
    return render_template('orders.html', items=items)


@app.route('/new_order', methods=['POST'])
def new():
    item_doc = {
        'name': request.form['name'],
        'pizza': request.form['pizza']
    }
    item_redis = {
        'pizza': str(request.form['pizza']),
        'address': str(request.form['address'])
    }
    db.tododb.insert_one(item_doc)
    order_save = json.dumps(item_redis)
    r.sadd('orders', order_save)
    return redirect(url_for('orders'))


@app.route('/del_order', methods=['POST'])
def delete():
    item_doc = {
        'name': request.form['name'],
        'pizza': request.form['pizza'],
    }
    db.tododb.delete_one(item_doc)
    return redirect(url_for('orders'))


# @app.route('/rem_order', methods=['POST'])
# def remove():
#     db.tododb.remove()
#     return redirect(url_for('orders'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)