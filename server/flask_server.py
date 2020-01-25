from flask import Flask, render_template
import os
from twilio.rest import Client

app = Flask(__name__)

account_sid = 'ACe060c1c4da2bec3b9a641416e8b018ac'
auth_token = 'f4bea2596471370d71c1544c1b6351f6'
client = Client(account_sid, auth_token)

@app.route('/')
def show_index():
    return render_template("index.html")

@app.route("/sms", methods=['GET','POST'])
def sms_reply():
    message = client.messages \
            .create(
                from_='+12019322527',
                media_url=['http://35.245.241.8:5000/static/html.png'],
                to='7329564059'
            )
    return("test")

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
