from flask import Flask,jsonify,request
import requests
import json
import sqlite3

app = Flask(__name__)

def ass():
    return ("ss")

@app.route('/')
def hello_world():
    db = sqlite3.connect('catalogDB.db')
    cursor = db.cursor()
    data = None
    cursor.execute('''CREATE TABLE IF NOT EXISTS BookTable(
                                           id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                           title TEXT,
                                           quantity INTEGER,
                                           price INTEGER,
                                           topic TEXT)''')
    
    # cursor.execute('''INSERT INTO BookTable(
    #     title,quantity,price,topic)
    #     VALUES("How to get a good grade in DOS in 20 minutes a day.",1,20,"Distributed systems")''')

    # cursor.execute('''INSERT INTO BookTable(
    #     title,quantity,price,topic)
    #     VALUES("RPCs for Dummies.",2,30,"Distributed systems")''')
    
    # cursor.execute('''INSERT INTO BookTable(
    #     title,quantity,price,topic)
    #     VALUES("Xen and the Art of Surviving Graduate School.",2,30,"Graduate school")''')
    # cursor.execute('''INSERT INTO BookTable(
    #     title,quantity,price,topic)
    #     VALUES("Cooking for the Impatient Graduate Student.",2,30,"Graduate school")''')

    db.commit()

    cursor.execute('SELECT * FROM BookTable')
    data = cursor.fetchall()

    return jsonify({"aa":data})

@app.route('/query/<item_number>', methods=['GET']) # item_num // or topic
def query(item_number):
    var = None
    data = None
    try:
        var = int(item_number) + 0
    except TypeError:
        var = str(item_number)
    
    if(type(var) is int):
        cursor.execute('SELECT id FROM BookTable')
        data = cursor.fetchall()
        
    return (str(data))

@app.route('/update/<item_number>', methods=['GET', 'POST']) #post
def update(item_number):
    x = ''
    if request.method == 'POST':
        x = request.form['newPrice']
        print (x)
        
    return (jsonify({'ass':item_number + x}))
