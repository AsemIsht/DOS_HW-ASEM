from flask import Flask,jsonify,request
import requests
import json
import sqlite3

app = Flask(__name__)

id_array = []
url_catalog_replica = 'http://192.168.121.142:5000'
def gath_of_id_requested(item_number):
    index = -1
    exist_ip = False
    for i in range(len(id_array)):
        if(int(id_array[i][0]) == int(item_number)):
            index = i

    if( index != -1):
        for i in range(1,len(id_array[index])):
            if (str(id_array[index][i]) == str(request.remote_addr)):
                exist_ip = True
        if(exist_ip == False):
            id_array[index].append(request.remote_addr)
    else:
        item0 = [int(item_number)]
        id_array.append(item0)
        id_array[len(id_array)-1].append(request.remote_addr)

    return ({"ss":id_array})

def push_invalidate(item_number):
    index = -1

    for i in range(len(id_array)):
        if(int(id_array[i][0]) == int(item_number)):
            index = i

    if(index != -1):
        if (len(id_array[index])!=0):
            for i in range(1,len(id_array[index])):
                requests.delete('http://'+str(id_array[index][i])+':5000/invalidate/' + str(item_number))
            id_array.pop(index)
    return (jsonify({"data":"data"}))

@app.before_first_request
def activate_job():
    print("STARTSTARTSTART")


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
    ###############
    gath_of_id_requested(item_number)
    ##############

    print("query_by_item_number")
    print(id_array)
    db.close()
    return (jsonify({"data":data}))

@app.route('/update/<item_number>', methods=['PUT'])
def update(item_number):
    newPrice = None
    newQuantity = None
    
    if request.method == 'PUT':
        try:
            newPrice = (request.form['newPrice'])#to be sure that input is on right type
        except:
            newPrice = 10
        
        try:
            newQuantity = (request.form['newQuantity'])
        except:
            newQuantity = 10
    

    db = sqlite3.connect('catalogDB.db')
    cursor = db.cursor()

    #cursor.execute('SELECT * FROM BookTable where id = "%s"' %(item_number))
    #data = cursor.fetchall()
    
    cursor.execute('UPDATE BookTable SET quantity = "%s" WHERE id = "%s"' %(str(newQuantity),str(item_number)))#SQLite Query
    db.commit()

    new_data = {'newPrice' : newPrice, 'newQuantity' : newQuantity}
    requests.put(url_catalog_replica+'/sync/' + item_number, data = new_data) #sync to another replica
    push_invalidate(int(item_number))


    print("update")
    print(id_array)
    db.close()
    return (jsonify({'status':'success','newQuantity':newQuantity}))

@app.route('/sync/<item_number>', methods=['PUT'])
def sync(item_number):
    newPrice = None
    newQuantity = None
    
    if request.method == 'PUT':
        try:
            newPrice = (request.form['newPrice'])#to be sure that input is on right type
        except:
            newPrice = 10
        
        try:
            newQuantity = (request.form['newQuantity'])
        except:
            newQuantity = 10
    

    db = sqlite3.connect('catalogDB.db')
    cursor = db.cursor()
    
    cursor.execute('UPDATE BookTable SET quantity = "%s" WHERE id = "%s"' %(str(newQuantity),str(item_number)))#SQLite Query
    db.commit()

    push_invalidate(int(item_number))

    print(id_array)
    db.close()
    return (jsonify({'status':'success','newQuantity':newQuantity}))
