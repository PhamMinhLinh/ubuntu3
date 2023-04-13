import base64
import binascii
import database
import json
import os


from flask import Flask, Response, render_template, jsonify, redirect, request

import person

app = Flask(__name__)

logged_in = {}
api_loggers = {}
mydb = database.db('root', 'localhost', '', 'eigentec_accidec')




@app.route("/login", methods=['GET', 'POST'])
def login():
    error = ""
    if request.method == 'POST':
        user = person.user(request.form['username'], request.form['password'])
        if user.authenticated:
            user.session_id = str(binascii.b2a_hex(os.urandom(15)))
            logged_in[user.username] = {"object": user}
            return redirect('/overview/{}/{}'.format(request.form['username'], user.session_id))#chuyển trang đến route overview
        else:
            error = "invalid Username or Passowrd"

    return render_template('Login.htm', error=error)




# this link is for the main dashboard of the website
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.htm', title='HOME - Landing Page')




@app.route('/overview/<string:username>/<string:session>', methods=['GET', 'POST'])
def overview(username, session):
    global logged_in

    if username in logged_in and (logged_in[username]['object'].session_id == session): # để đảm bảo session trên trinh duyej giống với session dc tạo bởi server
        user = {
            "username": username,
            "image": "/static/images/avatar.jpg",
            #"api": logged_in[username]["object"].api,
            "session": session
        }

        devices = [
            {"Dashboard": "device1",
             "deviceID": "Device1"
             }
        ]

        #lấy dư liệu từ bảng node trong databse mysql và truyền vào overview ở render
        return render_template('overview.htm', title='Overview', user=user, devices=devices) # đẩy user local và devices qua overview.htm

    else:
        return redirect('/login')


@app.route('/logout/<string:username>/<string:session>', methods=['GET', 'POST'])
def logout(username, session):
    global logged_in

    if username in logged_in and (logged_in[username]['object'].session_id == session):
        logged_in.pop(username) #đẩy ra
        return redirect('/')
    else:
        return redirect('/login')





@app.route('/api/<string:apikey>/deviceinfo/<string:deviceID>', methods=['GET', 'POST'])
def device_info(apikey, deviceID):
    global api_loggers
    global mydb
    if not (apikey in api_loggers):
        try:
            query = "select username from users where api_key = '{}'".format(apikey)
            mydb.cursor.execute(query)
            username = mydb.cursor.fetchall()
            username = username[0][0]
            apiuser = person.user(username, "dummy")
            apiuser.authenticated = True
            data = apiuser.dev_info(deviceID)
            api_loggers[apikey] = {"object": apiuser}
            # this part is hard coded so remove after fixing the issue
            data = list(data)
            data[2] = "TP_IOT"
            return jsonify(data)
        except Exception as e:
            print(e)
            return jsonify({"data": "Oops Looks like api is not correct"})

    else:
        data = api_loggers[apikey]["object"].dev_info(deviceID)

        # this part is hard coded so remove after fixing the issue
        data = list(data)
        data[2] = "TP_IOT"
        return jsonify(data)





@app.route('/api/<string:apikey>/update/<string:data>', methods=['GET', 'POST'])               #api ket noi va cap nhap gia tri trong database
def update_values(apikey, data):
    try:
        data = decode(data)
        output = mydb.get_apikeys()
        if apikey in output: #xác thực API key đúng hay sai
            if (len(data) == 4) and (type(data) is list):
                fieldname = data[0]                          #tran database muon dua du lieu vao
                deviceID = data[1]                            # ten thit bi gui len
                temp = data[2]                                 # trang thai
                humidity = data[3]                             #tt
                mydb.update_values(apikey, fieldname, deviceID, temp, humidity)
                return "Values Updated"
            else:
                return "Data Decoding Error!"
        else:
            return "Api key invalid"

    except Exception as e:
        print(e)
        return jsonify({"data": "Oops Looks like api is not correct"})




def encode(data):
    data = json.dumps(data)
    message_bytes = data.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message                                                #mh


def decode(base64_message):
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')
    return json.loads(message)


if __name__ == "__main__":
    app.run(debug=True)
