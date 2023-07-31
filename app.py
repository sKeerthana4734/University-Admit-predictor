# Title : University Admit Eligibility Predictor

# Team Members:
# Keerthana S (Team leader)
# Danesha M
# Kesavadevi T
# Akshaya G R

from flask import Flask, render_template, redirect, url_for, request
import requests

app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        arr = []
        for i in request.form:
            val = request.form[i]
            if val == '':
                return redirect(url_for("demo2"))
            arr.append(float(val))

        # deepcode ignore HardcodedNonCryptoSecret: <please specify a reason of ignoring this>
        API_KEY = "zL8s9Db-5JqwcVDby5sc4ZZE6SXlKgkf1ZRlz-ImLl12"
        token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={
            "apikey": API_KEY,
            "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'
        })
        mltoken = token_response.json()["access_token"]
        header = {'Content-Type': 'application/json',
                  'Authorization': 'Bearer ' + mltoken}
        payload_scoring = {
            "input_data": [{"fields": ['GRE Score',
                                       'TOEFL Score',
                                       'University Rating',
                                       'SOP',
                                       'LOR ',
                                       'CGPA',
                                       'Research'],
                            "values": [arr]
                            }]
        }

        response_scoring = requests.post(
            'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/ce2da0c2-843d-425a-8a82-b405b2a899d0/predictions?version=2022-11-18',
            json=payload_scoring,
            headers=header
        ).json()

        result = response_scoring['predictions'][0]['values']
        print(response_scoring['predictions'])
        print(result[0][1][1])

        if result[0][1][1] > 0.5:
            return redirect(url_for('chance', percent=result[0][1][1]*100))
        else:
            return redirect(url_for('no_chance', percent=result[0][1][1]*100))
    else:
        return redirect(url_for("demo2"))


@app.route("/home")
def demo2():
    return render_template("demo2.html")


@app.route("/chance/<percent>")
def chance(percent):
    percent = round(float(percent), 2)
    return render_template("chance.html", content=[percent])


@app.route("/nochance/<percent>")
def no_chance(percent):
    percent = round(float(percent), 2)
    return render_template("noChance.html", content=[percent])


if __name__ == "__main__":
    app.run()
