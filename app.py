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
message_control = dbmanager.MessageControl(dbcon)

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

@socketio.on('get_messages')
def handle_get_messages():
	messages = message_control.get_all_messages()
	print(messages)
	return messages

@socketio.on('send_message')
def handle_message(message):
	print(message)
	message_control.add_message(message)
	emit('new_message', message, broadcast=True)

@socketio.on('req_login')
def handle_login(data):
	uname, pwd = data['uname'], data['passwd']
	pwd = hashlib.sha256(pwd.encode()).hexdigest()
	uid = user_control.db_get_uid(uname)
	if uid is not None:
		db_pwd = user_control.db_get_data(uid, 'pwd')
		if pwd == db_pwd:
			print(f"{uname} logged in successfully")
			sess_id = session_control.create_session(uid)
			if sess_id is None:
				emit('req_login_res', {'status': 3, 'data': {'uid': uid}})
			else:
				emit('req_login_res', {'status': 0, 'data': {'uname': uname, 'acc_col': user_control.db_get_data(uid, 'acc_col'), 'uid': uid, 'sess_id': sess_id}})
		else:
			emit('req_login_res', {'status': 2, 'data': {}})
	else:
		emit('req_login_res', {'status': 1, 'data': {}})

@socketio.on('change_session')
def change_session(data):
	uid = data['uid']
	session_control.discard_session(session_control.get_sess_id(uid))
	sess_id = session_control.create_session(uid)
	return {'status': 0, 'data': {'sess_id': sess_id}}

@socketio.on('validate_session')
def validate_session(data):
	sess_id, uid = data['sess_id'], data['uid']
	if session_control.is_session_valid(sess_id) and session_control.get_uid(sess_id) == uid:
		return {'status': 0}
	else:
		return {'status': 1}

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
	uname, uid = data['uname'], data['uid']
	print(f"{uname} disconnected")
	session_control.discard_session(session_control.get_sess_id(uid))

@socketio.on('reqcol')
def getcol(data):
	emit('res_acc_col', user_control.db_get_data(user_control.db_get_uid(data['uid']), 'acc_col'))

@socketio.on('changecol')
def changecolor(data):
	user_control.db_update_data(data['uid'], data['col'], 'acc_col')

@socketio.on('reg_request')
def register_user(data):
	nuname, npwd = data['uname'], data['passwd']
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
