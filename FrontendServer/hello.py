from flask import Flask, jsonify, request
from flask import render_template

import requests
import json

app = Flask(__name__)

url_catalog = 'http://192.168.121.134:5000'
url_order = 'http://192.168.121.135:5000'

url = url_order
# @app.route('/') #not needed !
# def hello_world():
#     response = json.loads(requests.get(url_catalog).content)
#     return (str(response[0]))

@app.route('/search/<topic>') # search service
def search(topic):
    response = json.loads(requests.get(url_catalog+'/query_by_topic/' + topic).content) #frontend requests from catalog
    row = response['data'] #catalog return json as {'data': data}
    
    return (render_template ('topics_search.html', row = row, len = len(row))) #parsing length of items, and data to html to represent

@app.route('/lookup/<item_number>')
def lookup(item_number):
    response = json.loads(requests.get(url_catalog+'/query_by_item_number/' + item_number).content)
    row = response['data']
    len0 = None #initialization
    if(row == 'Not an ID' or  row == 'Error type'): #I set the responsability of check the input to catalog server
        len0 = 0
    else:
        len0 = len(row)
    
    
    return (render_template ('items_lookup.html', row = row, len = len0))#if len0 is 0, print error msg
    
@app.route('/buy/<item_number>')
def buy(item_number):

    response = json.loads(requests.post(url_order+'/buy/' + item_number).content)#frontend request to buy from order
    

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