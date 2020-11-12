from flask import Flask,jsonify,request
import requests
import json
import sqlite3

app = Flask(__name__)

def ass():
    return ("ss")

@app.route('/')
def hello_world():

    return "jsonify(a)"

@app.route('/query/<item_number>')
def query(item_number):
    var = None
    try:
        var = int(item_number) + 0
    except TypeError:
        var = str(item_number)
    
    print(type(var) is int)
    return (str(var))

@app.route('/update/<item_number>', methods=['GET', 'POST']) #post
def update(item_number):
    x = ''
    if request.method == 'POST':
        x = request.form['newPrice']
        print (x)
        
    return (jsonify({'ass':item_number + x}))
