from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'ACe060c1c4da2bec3b9a641416e8b018ac'
auth_token = 'f4bea2596471370d71c1544c1b6351f6'
client = Client(account_sid, auth_token)

import time

s = time.time()

message = client.messages \
                .create(
                     ##body = "hi there2",
                     from_='+12019322527',
                     media_url=['http://35.245.241.8:5000/static/html.png'],
                     to='7329564059'
                 )

print(time.time()-s)
print(message.sid)