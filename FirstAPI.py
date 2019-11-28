from flask import Flask
import requests

url = "https://www.alphavantage.co/query"

querystring = {"function":"TIME_SERIES_INTRADAY","symbol":"MSFT","interval":"5min","apikey":"RA577UAZ4V10HG3S"}

headers = {
    'User-Agent': "PostmanRuntime/7.18.0",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Postman-Token': "6b382022-8518-4137-81f6-95959d72288f,ff09ccdc-5a46-47b3-aa3f-ef91dcdb8a4f",
    'Host': "www.alphavantage.co",
    'Accept-Encoding': "gzip, deflate",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

app = Flask (__name__)
@app.route('/')
def home():
    return response.text