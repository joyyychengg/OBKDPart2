from flask import Flask
import requests

url = "https://www.quandl.com/api/v3/datasets/LBMA/GOLD.json?api_key=w-zmuZcjFD5yEtgr8MCC"

querystring = {"api_key":"w-zmuZcjFD5yEtgr8MCC"}

headers = {
    'User-Agent': "PostmanRuntime/7.18.0",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Postman-Token': "06fa71cb-7b82-4e0d-8b5a-6d53da6b726f,77399bef-4e83-4cdf-b010-035ed007ea57",
    'Host': "www.quandl.com",
    'Accept-Encoding': "gzip, deflate",
    'Cookie': "__cfduid=dcca43b36a9a05114b2d8f059a96c86511571755026",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

app = Flask (__name__)
@app.route('/')
def home():
    return response.text