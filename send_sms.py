from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'AC64f69383da98b45caaa820591059da00'
auth_token = '66fdb1eb56bba520a7499e950fddc91b'
client = Client(account_sid, auth_token)

import time

s = time.time()

message = client.messages \
                .create(
                     from_='+13344413651',
                     media_url=['https://i.imgur.com/1dxJxGs.png'],
                     to='7329564059'
                 )

print(time.time()-s)
print(message.sid)