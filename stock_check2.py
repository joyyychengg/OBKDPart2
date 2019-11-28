from flask import Flask,render_template, redirect, url_for, request
import requests
import json

app = Flask(__name__)
@app.route('/stock',methods=['GET'])
def stock():
    return render_template('stock.html')

@app.route('/result',methods=['GET','POST'])
def result():
    error = None
    if request.method == "POST":
        tickerCode = request.form['stockSymbol']
        api_key = request.form['APIKey']
        url = "https://www.alphavantage.co/query"

        querystring = {"function":"TIME_SERIES_INTRADAY","symbol":tickerCode,"interval":"5min","apikey":"RA577UAZ4V10HG3S"}

        headers = {
            'User-Agent': "PostmanRuntime/7.18.0",
            'Accept': "*/*",
            'Cache-Control': "no-cache",
            'Postman-Token': "6b382022-8518-4137-81f6-95959d72288f,a2fd5838-b6c6-47fd-9662-6005273a32ed",
            'Host': "www.alphavantage.co",
            'Accept-Encoding': "gzip, deflate",
            'Connection': "keep-alive",
            'cache-control': "no-cache"
            }

        response = requests.request("GET", url, headers=headers, params=querystring)

        stockData = json.loads(response.text)
        lastRefreshedDate = stockData["Meta Data"]["3. Last Refreshed"]
        latestStockPrices = stockData["Time Series (5min)"][lastRefreshedDate]
        closingPrice = latestStockPrices["4. close"]
        volume = latestStockPrices["5. volume"]

    return render_template('stock_price.html', tCode=tickerCode, sPrice=closingPrice, cVolume=volume, dTime=lastRefreshedDate)