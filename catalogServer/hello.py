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
    data = None#next line is creation of booktable
    cursor.execute('''CREATE TABLE IF NOT EXISTS BookTable(
                                           id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                           title TEXT,
                                           quantity INTEGER,
                                           price INTEGER,
                                           topic TEXT)''')
    #next lines is to insert the initial values of booktable
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

    #db.commit()

    cursor.execute('UPDATE BookTable SET quantity = "%s"' %(str(5)))#this line I use it for recharge the stock
    db.commit()

    cursor.execute('SELECT * FROM BookTable') #to debuging only -> represent all table entries
    data = cursor.fetchall()

    db.close()
    return jsonify(data)

#I can put these lines (service) insted of two next services 
# @app.route('/query/<item_number>', methods=['GET']) # item_num // or topic
# def query(item_number):
#     var = None
#     data = None
#     try:
#         var = int(item_number) + 0
#     except TypeError:
#         var = str(item_number)
    
#     if(type(var) is int):
#         cursor.execute('SELECT id FROM BookTable')
#         data = cursor.fetchall()
        
#     return (str(data))

@app.route('/query_by_topic/<topic>', methods=['GET']) # query by topic
def query_by_topic(topic):
    db = sqlite3.connect('catalogDB.db') #connect to sqlite DB
    cursor = db.cursor() #cursor pointing to DB

    var = None
    data = None
    var = str(topic)

    cursor.execute('SELECT * FROM BookTable where topic = "%s"' %(var)) #var contain topic string
    data = cursor.fetchall()
    
    db.close() #close DB
    return (jsonify({"data":data}))

@app.route('/query_by_item_number/<item_number>', methods=['GET']) # item_num // or topic
def query_by_item_number(item_number):
    db = sqlite3.connect('catalogDB.db')
    cursor = db.cursor()
    var = None
    data = None
    try:#to check if input is another else than int --> wrong
        var = int(item_number) + 0
    except:
        return (jsonify({"data":"Error type"}))
    
    if(type(var) is int): #integer --> ok
        cursor.execute('SELECT * FROM BookTable where id = "%s"' %(item_number))
        data = cursor.fetchall()
    
    if(len(data) == 0): #didnt find this id on DB
        return (jsonify({"data":"Not an ID"}))

    db.close()
    return (jsonify({"data":data}))

@app.route('/update/<item_number>', methods=['PUT'])
def update(item_number):
    newPrice = None
    newQuantity = None
    if request.method == 'PUT':
        try:
            newPrice = int(request.form['newPrice'])#to be sure that input is on right type
        except:
            newPrice = None
        
        try:
            newQuantity = int(request.form['newQuantity'])
        except:
            newQuantity = None
    

    db = sqlite3.connect('catalogDB.db')
    cursor = db.cursor()

    #cursor.execute('SELECT * FROM BookTable where id = "%s"' %(item_number))
    #data = cursor.fetchall()
    
    
    cursor.execute('UPDATE BookTable SET quantity = "%s" WHERE id = "%s"' %(newQuantity,int(item_number)))#SQLite Query
    db.commit()

    db.close()
    return (jsonify({'status':'success'}))