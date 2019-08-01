#!/usr/bin/env python3
from flask import Flask, redirect, url_for,request,render_template
#import os
from redis import Redis
#from rq import Queue
import json
app = Flask(__name__)

r = Redis(host='redis', port=6379)
@app.route('/')
def address():
    get_order = r.smembers('orders')
    _items = []
    for item in get_order:
        try:
            result = json.loads(item)
        except:
            return "Oh no"
        _items.append(result)
    items = [item for item in _items]
    return render_template('address.html', items=items)


@app.route('/delete_all', methods=['POST'])
def new():
    r.delete('orders')
    return redirect(url_for('address'))
if __name__ == "__main__":
    app.run('0.0.0.0', 8082)