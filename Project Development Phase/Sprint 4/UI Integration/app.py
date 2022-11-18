from flask import Flask, request, render_template, flash
import numpy as np
import pandas as pd
from sklearn import metrics
import warnings
import pickle
import os
import scipy.io as sio
import joblib
warnings.filterwarnings('ignore')
from features import FeatureExtraction
import requests


app = Flask(__name__)
app.secret_key = "123abc$#@!"


API_KEY = "zlMpO3s-HVl2y64bgG00kmKBRH9SuJ_x5mCqgjF0sqYa"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}




@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")
@app.route("/result",methods=['POST','GET'])
def result():
    if request.method == "POST":

        url = request.form["url"]
        obj = FeatureExtraction(url)
        x = np.array(obj.getFeaturesList()).reshape(1,30)
        y=x.tolist()
        payload_scoring = {"input_data": [{"field": [[ 'having_IPhaving_IP_Address', 'URLURL_Length',
       'Shortining_Service', 'having_At_Symbol', 'double_slash_redirecting',
       'Prefix_Suffix', 'having_Sub_Domain', 'SSLfinal_State',
       'Domain_registeration_length', 'Favicon', 'port', 'HTTPS_token',
       'Request_URL', 'URL_of_Anchor', 'Links_in_tags', 'SFH',
       'Submitting_to_email', 'Abnormal_URL', 'Redirect', 'on_mouseover',
       'RightClick', 'popUpWidnow', 'Iframe', 'age_of_domain', 'DNSRecord',
       'web_traffic', 'Page_Rank', 'Google_Index', 'Links_pointing_to_page',
       'Statistical_report']], "values": y}]}



        response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/f6e86133-3fbb-484f-bfba-d43e02ac57ad/predictions?version=2022-11-17', json=payload_scoring,
        headers={'Authorization': 'Bearer ' + mltoken})
        print('scoring response')
        predictions=response_scoring.json()
        pred=predictions['predictions'][0]['values'][0][0]
        print(pred)

        if pred == -1:
            pred="faileure"
            cond="UnSafe"
            color="danger"
        else:
            pred="success"
            cond="Safe"
            color="info"

        output = f"{pred} ! The entered URL/Link is {cond} to use"
        return render_template('index.html', output=output,color=color)

if __name__ == "__main__":
    app.debug = True
    app.run()