from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session, url_for, render_template
from requests.auth import HTTPBasicAuth
import requests
import json

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'fa85582d5f84f3ccb1023d3d2a1a0f85'

client_id = "5ba593eb4cc1417c"
client_secret = "fa85582d5f84f3ccb1023d3d2a1a0f85"

authorization_base_url = 'https://apm.tp.sandbox.fidor.com/oauth/authorize'
token_url = 'https://apm.tp.sandbox.fidor.com/oauth/token'
redirect_uri = 'http://localhost:5000/callback'

@app.route('/', methods=["GET"])
@app.route('/index', methods=["GET"])
def default():

    fidor = OAuth2Session(client_id,redirect_uri=redirect_uri)
    authorization_url, state = fidor.authorization_url(authorization_base_url)
    session['oauth_state'] = state
    print("authorization URL is =" +authorization_url)
    return redirect(authorization_url)

@app.route("/callback", methods=["GET"])
def callback():
    fidor = OAuth2Session(state=session['oauth_state'])
    authorizationCode = request.args.get('code')
    body = 'grant_type="authorization_code&code=' +authorizationCode + '&redirect_uri=' + redirect_uri+ '&client_id=' +client_id
    auth = HTTPBasicAuth(client_id, client_secret)
    token = fidor.fetch_token(token_url, auth=auth,code=authorizationCode,body=body,method='POST')

    session['oauth_token'] = token
    return  redirect(url_for('.services'))

@app.route("/services", methods=["GET"])
def services():
    try:
        token = session['oauth_token']
        url = "https://api.tp.sandbox.fidor.com/accounts"

        payload =""
        headers = {
            'Accept': "application/vnd.fidor.de;version=1;text/json",
            'Authorization': "Bearer " +token["access_token"],
            'cache-control': "no-cache",
            'Postman-Token': "2beeaf6812fdd3fe3851b6213f9da41a"
        }

        response = requests.request("GET", url, data=payload, headers=headers)
        print("services=" + response.text)
        customersAccount = json.loads(response.text)
        customerDetails = customersAccount['data'][0]
        customerInformation = customerDetails['customers'][0]
        session['fidor_customer'] = customersAccount

        return render_template('services.html', fID=customerInformation["id"],
            fFirstName=customerInformation["first_name"], fLastName=customerInformation["last_name"],
            fAccountNumber=customerDetails["account_number"],fBalance=(customerDetails["balance"]/100))

    except KeyError:    
        print("Key error in services to return back to index")
        return redirect(url_for('default'))

@app.route("/bank_transfer", methods=["GET"])
def transfer():
    try:
        customersAccount = session['fidor_customer']
        customerDetails = customersAccount['data'][0]

        return render_template('internal_transfer.html', fFIDOR=customerDetails["id"],
            fAccountNo=customerDetails["account_number"], fBalance=(customerDetails["balance"]/100))
        
    except KeyError:
        print("Key error in bank_transfer to return back to index")
        return redirect(url_for('.index'))

@app.route("/process", methods=["POST"])
def process():
    if request.method == "POST":
        token = session['oauth_token']
        customersAccount = session['fidor_customer']
        customerDetails = customersAccount['data'][0]

        fidorID = customerDetails['id']
        custEmail = request.form['customerEmailAdd']
        transfersAmt = int(float(request.form['transferAmount'])*100)
        transferRemarks = request.form[ 'transferRemarks']
        transactionID = request.form[ 'transactionID']

        url = "https://api.tp.sandbox.fidor.com/internal_transfers"

        payload = "{\n\t\"account_id\":\""+fidorID+"\",\n\t\"receiver\":\""+custEmail+"\",\n\t\"external_uid\":\""+transactionID+"\",\n\t\"amount\": \""+str(transfersAmt)+"\",\n\t\"subject\":\""+transferRemarks+"\"\n}"
        headers = {
            'Accept': "application/vnd.fidor.de;version=1;text/json",
            'Content-Type': "application/json",
            'Authorization': "Bearer "+token["access_token"],
            'Cache-Control': "no-cache",
            'Postman-Token': "f4a7f0e7-11ff-41cf-ad47-edb1f3a964bb,f9fa99fe-0845-42d6-963b-1b6822503db4"
            }

        response = requests.request("POST", url, data=payload, headers=headers)

        print("process="+response.text)

        transactionDetails = json.loads(response.text)
        return render_template('transfer_result.html', fTransactionID=transactionDetails["id"],
            custEmail=transactionDetails["receiver"], fRemarks=transactionDetails["subject"],
            famount=(float(transactionDetails["amount"])/100),
            fRecipientName=transactionDetails["recipient_name"])



    