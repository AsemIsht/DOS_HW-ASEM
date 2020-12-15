from flask import Flask, jsonify, request
from flask import render_template

import requests
import json

import time


app = Flask(__name__)
count_catalog = 0
count_order = 0
url_catalog = 'http://192.168.121.148:5000'
url_order = 'http://192.168.121.149:5000'

catche0 = []
url = url_order


def check_catche_available(id):
    for i in range(len(catche0)):
        if( catche0[i][0] == id):
            return i
    return (-1)

def catche_replacement_algo():
    min_index = 0
    min_value = int(catche0[0][5])
    for i in range(int(len(catche0))):
        if(min_value > int(catche0[i][5])):
            min_index = i
            min_value = int(catche0[i][5])
    catche0.pop(min_index)
    
# @app.before_request
# def before_request_func():
#     print("before_request is running!")


# @app.after_request
# def after_request_func(response):
#     print(response)
#     return response



@app.route('/search/<topic>') # search service
def search(topic):
    response = json.loads(requests.get(url_catalog+'/query_by_topic/' + topic).content) #frontend requests from catalog
    row = response['data'] #catalog return json as {'data': data}
    
    return (render_template ('topics_search.html', row = row, len = len(row))) #parsing length of items, and data to html to represent

@app.route('/lookup/<item_number>')
def lookup(item_number):
    start_time = time.time()
    global count_catalog
    
    len0 = None #initialization
    index = check_catche_available(int(item_number))
    if(index != -1):
        # print ("yes")
        len0 = 1
        catche0[index][5] += 1 #inc usage
    else:
        
        # print ("no")
        if(count_catalog == 0):
            print("first")
            response = json.loads(requests.get(url_catalog+'/query_by_item_number/' + item_number).content)
        else:
            print("second")
            response = json.loads(requests.get(url_catalog+'/query_by_item_number/' + item_number).content)

        count_catalog += 1
        count_catalog = count_catalog % 2
        
        row = response['data']
        
        if(row == 'Not an ID' or  row == 'Error type'): #I set the responsability of check the input to catalog server
            len0 = 0
        else:
            len0 = len(row)

            if(len(catche0) >= 2):
                catche_replacement_algo() #pop LRU

            catche0.append(row[0])
            index = len(catche0)-1
            catche0[index].append(1) #usage

    if (len(catche0) == 0): #to prevent out of range array (return row = catche0[index]
        print (str(time.time() - start_time))
        return (render_template ('items_lookup.html', row = [0], len = len0))#if len0 is 0, print error msg
    print (str(time.time() - start_time))
    return (render_template ('items_lookup.html', row = catche0[index], len = len0))#if len0 is 0, print error msg
    
    
@app.route('/buy/<item_number>')
def buy(item_number):
    global count_order
    if(count_order == 0):
        print("first")
        response = json.loads(requests.post(url_order+'/buy/' + item_number).content)#frontend request to buy from order
    else:
        print("second")
        response = json.loads(requests.post(url_order+'/buy/' + item_number).content)#frontend request to buy from order

    count_order += 1
    count_order = count_order % 2
    
    

    # newPrice = {'newPrice' : 50}
    # x = requests.post(url_catalog+'/update/1', data = newPrice)
    # response = json.loads(x.content)
    # print(str(response["ass"]))
    if(response['status'] == "success"):#if is success(item is valid)
        return (render_template ('buy_req_success.html', row = response['name']))
    elif  (response['status'] == "outOfStock"):#item is out of stock
        return (render_template ('buy_req_outOfStock.html', row = response['name']))
    else:
        return (render_template ('buy_req_fail.html'))#error input
# Notes: 
# return jsonify(a)
# json.loads(requests.get(url).content) # --> response["age"]
#

@app.route('/invalidate/<item_number>', methods=['DELETE'])
def invalidate(item_number):
    if(int(item_number) == 0):
        catche0.clear()
    index = check_catche_available(int(item_number))
    if(index!=(-1)):
        catche0.pop(index)
    return (jsonify({"data":"data"}))
    

# @app.route('/loop_for_repl/<item_number>')
# def loop_for_repl(item_number):
#     if (item_number == "1"):
#         while(True):
#             pass
    
#     else:
#         return ("hello")
    
    
#     return ("n")

# @app.route('/loop_for_repl0/<item_number>')
# def loop_for_repl0(item_number):
    if (item_number == "1"):
        while(True):
            pass
    
    else:
        return ("hello")
    
    
    return ("n")

# if __name__ == 'main':
#     app.run(debug=True, threaded=True)
