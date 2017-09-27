#!/usr/bin/env python
import json
import os
import requests
from flask import Flask
from flask import jsonify
from flask import request
app = Flask(__name__)

def get_stock(symbol):
  url = "http://finance.google.com/finance?q=%s&output=json" % symbol

  r = requests.get(url)
  for line in r.text.split("\n"):
    if "\"l\"" in line:
      last = line
      break

  last = last.split('"')[1::2][1]
  return last


def get_crypto():
  url = "https://api.coinbase.com/v2/prices/spot?currency=USD"

  r = requests.get(url)
  j = json.loads(r.text)
  price = j['data']['amount']
  return price


@app.route('/')
def main():
  return 'Hello World! ' + os.environ.get('TEST_KEY', None)


@app.route('/stock', methods=['POST'])
def stock():
  box = get_stock('BOX')
  msft = get_stock('MSFT')
  btc = get_crypto()
  slack = '0'

  stocks = 'BOX: $' + box + '\nMSFT: $' + msft + '\nBTC: $' + btc + '\nSLACK: $' + slack
  response = jsonify(text=stocks)
  return response

if __name__ == '__main__':
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port)
  #app.debug = True
  #app.run(host='127.0.0.1', port=5000)
