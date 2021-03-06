from flask import Flask,jsonify,request
import requests
import json
import sqlite3

app = Flask(__name__)


url_catalog = 'http://192.168.121.142:5000'


# @app.route('/')
# def hello_world():
#     return jsonify({"aa":"jsonify(a)"})


@app.route('/buy/<item_number>', methods=['POST'])
def buy(item_number):
    
    response = json.loads(requests.get(url_catalog+'/query_by_item_number/' + item_number).content) #first get request to catalog to get the qty
    response2 = None

    if (response['data'] == "Not an ID"):#item_number doesnt an exist
        return (jsonify({"status" : "Not an ID"}))
    if (response['data'] == "Error type"):#item_number type error
        return (jsonify({"status" : "Error type"}))


    if (response['data'][0][2] > 0): #if qty > 0
        new_data = {'newPrice' : response['data'][0][3], 'newQuantity' : response['data'][0][2]-1}#repearing data to parse to update request
        response2 = requests.put(url_catalog+'/update/' + item_number, data = new_data)#second request to decrement qty
        if(json.loads(response2.content)['status'] == 'success'):#status of update response is success 
            return (jsonify({"status" : "success", "id" : response['data'][0][0], "name": response['data'][0][1]})) #response to frontend
        else:
            return (jsonify({"status" : "fail", "id" : response['data'][0][0], "name": response['data'][0][1]}))
    else:
        return (jsonify({"status" : "outOfStock", "id" : response['data'][0][0], "name": response['data'][0][1]}))#response to frontend that out of stock

@app.route('/invalidate/<item_number>', methods=['DELETE'])
def invalidate(item_number):
    
    return (jsonify({"data":"data"}))


# @app.route('/query/<item_number>')
# def query(item_number):
#     var = None
#     try:
#         var = int(item_number) + 0
#     except TypeError:
#         var = str(item_number)
    
#     print(type(var) is int)
#     return (str(var))

# @app.route('/update/<item_number>', methods=['GET', 'POST']) #post
# def update(item_number):
#     x = ''
#     if request.method == 'POST':
#         x = request.form['newPrice']
#         print (x)
        
#     return (jsonify({'ass':item_number + x}))
