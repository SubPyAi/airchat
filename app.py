import os
import random
import uuid
import hashlib
import dbmanager
import dotenv
import mysql.connector
import datetime
import flask
import flask_socketio
from flask import Flask, render_template, redirect
from flask_socketio import SocketIO, send, emit
from time import sleep

dotenv.load_dotenv()

#connect to mysql db
dbcon = mysql.connector.connect(
	host=os.getenv("MYSQL_HOST"),
	port=os.getenv("MYSQL_PORT"),
	user=os.getenv("MYSQL_USER"),
	password=os.getenv("MYSQL_PWD"),
	database=os.getenv("MYSQL_DB")
)

#initialise mysql db controllers
user_control = dbmanager.UserControl(dbcon)
session_control = dbmanager.SessionControl(dbcon)

app = Flask(__name__)
app.config['SECRET'] = 'secret@nxgen8'
app.config['TEMPLATES_AUTO_RELOAD'] = True
socketio = SocketIO(app, cors_allowed_origins="*")

global logfile
logfile = "static/air.log"

with open(logfile, "w+") as f:
	pass

def log(txt):
	with open(logfile, "a") as f:
		f.write(f"[{datetime.datetime.now()}] {txt}\n")

@socketio.on('message')
def handle_message(message):
	if 'usrconnected@nxgenServers' in message:
		try:
			misc, uname, uid = message.split('?')
			print(f"{uname} connected")
			log(f"{uname} connected")
			with open('user.cfg', 'r') as f:
				usrdata = f.readlines()
				f.close()
			for i in range(0, len(usrdata)):
				a, b, c, d = usrdata[i].split(":")
				d = d.replace("\n", '')
				if uid == a:
					c = "online"
					newData = a + ":" + b + ":" + c + ":" + d + "\n"
					usrdata[i] = newData
					with open('user.cfg', 'w') as f:
						f.write("")
						f.writelines(usrdata)
						f.close()
				else:
					pass
		except:
			pass
	elif 'thisisaloginconfmsgufksjdhfbcushfadsg' in message:
		uid, misc = message.split(':')
		with open('user.cfg', 'r') as f:
			usrdata = f.readlines()
			f.close()
		for i in usrdata:
			data = []
			data = i.split(':')
			uid0 = data[0]
			uname = data[1]
			status = data[2]
			col = data[3]
			if uid == uid0:
				status = status.replace('\n', '')
				if status=='online':
					send(uname + ':omghadfjkhyabweuirtagjdskgfbdsilagfbewayrnxaklsdjgf' + uid + ",online", broadcast=True)
					break
				else:
					send(uname + ':omghadfjkhyabweuirtagjdskgfbdsilagfbewayrnxaklsdjgf' + uid + "]" + col + ",found", broadcast=True)
					break
			else:
				uname = ''
		if uname == '':
			send(uname + ':omghadfjkhyabweuirtagjdskgfbdsilagfbewayrnxaklsdjgf' + uid + ",notfnd")
		else:
			pass
	else:
		print(message)
		log(message.split("<:-:>")[0])
		send(message, broadcast=True)

@socketio.on('req_login')
def handle_login(data):
	print('ha')
	uname, pwd = data.split(':')
	pwd = hashlib.sha256(pwd.encode()).hexdigest()
	uid = user_control.db_get_uid(uname)
	print(f"UID: {uid}")
	if uid is not None:
		db_pwd = user_control.db_get_data(uid, 'pwd')
		print(db_pwd, pwd, sep="\n")
		if pwd == db_pwd:
			print(f"{uname} logged in successfully")
			sess_id = session_control.create_session(uid)
			emit('req_login_res', {'status': 0, 'data': {'uname': uname, 'acc_col': user_control.db_get_data(uid, 'acc_col'), 'uid': uid, 'sess_id': sess_id}})
		else:
			emit('req_login_res', {'status': 2, 'data': {}})
	else:
		emit('req_login_res', {'status': 1, 'data': {}})

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/chat')
def chat():
	return render_template("chat.html")

@app.route('/register')
def register():
	return render_template("register.html")

@socketio.on('client_disconnect')
def disconnect_user(data):
	uname, uid = data.split(':')
	print(f"{uname} disconnected")
	session_control.discard_session(session_control.get_sess_id(uid))

@socketio.on('reqcol')
def getcol(data):
	emit('res_acc_col', user_control.db_get_data(user_control.db_get_uid(data), 'acc_col'))

@socketio.on('changecol')
def changecolor(data):
	uname, col = data.split(":")
	user_control.db_update_data(user_control.db_get_uid(uname), col, 'acc_col')

@socketio.on('reg_request')
def register_user(data):
	nuname, npwd = data.split(':')
	uid = str(uuid.uuid4())
	npwd = hashlib.sha256(npwd.encode()).hexdigest()
	if user_control.db_create_user({
		'uname': nuname,
		'pwd': npwd,
		'acc_col': '#1b2c3a',
		'status': 0,
		'u_id': uid
	}):
		emit('reg_response_success')
	else:
		emit('reg_response_failure')

@socketio.on('req_data')
def get_data(data):
	uid = session_control.get_uid(data[0])
	if uid is not None:
		emit('res_data', {'status': 0, 'data': user_control.db_get_data(uid, data[1])})
	else:
		emit('res_data', {'status': 1, 'data': {}})

if __name__ == "__main__":
	socketio.run(app, debug=False, allow_unsafe_werkzeug=True, host='127.0.0.1', port=5000)
