from flask import Flask, jsonify, request
import requests
import json

app = Flask(__name__)

url_catalog = 'http://192.168.121.134:5000'
url_order = 'http://192.168.121.135:5000'

url = url_order
@app.route('/')
def hello_world():
    response = json.loads(requests.get(url).content)
    return (str(response["aa"]))

@app.route('/search/<topic>')
def search(topic):
    return (topic)

@app.route('/lookup/<item_number>')
def lookup(item_number):
    return (item_number)
    
@app.route('/buy/<item_number>')
def buy(item_number):
    newPrice = {'newPrice' : 50}
    x = requests.post(url+'/update/1', data = newPrice)
    response = json.loads(x.content)
    print(str(response["ass"]))
    
    return (response)


# Notes: 
# return jsonify(a)
# json.loads(requests.get(url).content) # --> response["age"]
#