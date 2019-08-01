#!/usr/bin/env python3
from flask import Flask, redirect, url_for,request,render_template,jsonify
from redis import Redis
import json

app = Flask(__name__)

r = Redis(host='redis', port=6379)
@app.route('/')
def update():
    no_update = 0
    try:
        get_update = r.get('update')
    except:
        return "Oh no"
    try:
        result = json.loads(get_update)
    except:
        no_update = 1
        return render_template('update.html', no_update = no_update)
    return render_template('update.html', Product = result['Product'], weight = result['Weight'], no_update = no_update)


@app.route('/del', methods=['POST'])
def new():
    r.delete('update')
    return redirect(url_for('update'))
if __name__ == "__main__":
    app.run('0.0.0.0', 8081)