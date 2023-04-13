import json, base64
import urllib.request
from random import choice
import time



# thử nghiệm

def encode(data):
    data = json.dumps(data)
    message_bytes = data.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message


def decode(base64_message):
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')
    return json.loads(message)


randlist = [i for i in range(0, 100)]
devlist = ['Dec1112','Dec12012','Dec22212']

while 1: #lien tuc detech ngã hay ko
    try:
        mydata = ['JetsonNano', 'Dec12012', choice(randlist), choice(randlist)] #detech ngã hay ko
        a = encode(mydata)
        url = 'http:/{}'.format(a)#                                                                                                  #url = 'http://eigentechltd.com/hcmctransport/api/nguyentrieuphongdotcom/update/{}'.format(a)

        response = urllib.request.urlopen(url)
        print("[data]: "+ str(mydata))
        print("[Encoded Value]: "+ a)
        print("[url]: "+ url)
        html = response.read()
        print("[output]: " + str(html))
        time.sleep(2)
    except:
        print("Website Not online")
        time.sleep(2)