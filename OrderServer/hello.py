from flask import Flask,jsonify,request
import requests
import json
import sqlite3

app = Flask(__name__)


url = 'http://192.168.121.134:5000'


# @app.route('/')
# def hello_world():
#     return jsonify({"aa":"jsonify(a)"})


@app.route('/buy/<item_number>', methods=['POST'])
def buy(item_number):
    
    response = json.loads(requests.get(url+'/query_by_item_number/' + item_number).content)
    response2 = None

    if (response['data'] == "Not an ID"):
        return (jsonify({"status" : "Not an ID"}))
    if (response['data'] == "Error type"):
        return (jsonify({"status" : "Error type"}))


    if (response['data'][0][2] > 0):
        new_data = {'newPrice' : response['data'][0][3], 'newQuantity' : response['data'][0][2]-1}
        response2 = requests.put(url+'/update/' + item_number, data = new_data)
        if(json.loads(response2.content)['status'] == 'success'):
            return (jsonify({"status" : "success", "id" : response['data'][0][0], "name": response['data'][0][1]}))
        else:
            return (jsonify({"status" : "fail", "id" : response['data'][0][0], "name": response['data'][0][1]}))
    else:
        return (jsonify({"status" : "outOfStock", "id" : response['data'][0][0], "name": response['data'][0][1]}))



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
