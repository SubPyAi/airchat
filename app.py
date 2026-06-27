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

global logfile
logfile = "static/air.log"

with open(logfile, "w+") as f:
	pass

def log(event, data):
	with open(logfile, "a") as f:
		f.write(f"[{datetime.datetime.now()}] {'[' + event + ']'}: {data}\n")

log("SERVER_INITIATION", "server deployment started")

dotenv.load_dotenv()

log("SERVER_INITIATION", "connecting to mysql")
#connect to mysql db
dbcon = mysql.connector.connect(
	host=os.getenv("MYSQL_HOST"),
	port=os.getenv("MYSQL_PORT"),
	user=os.getenv("MYSQL_USER"),
	password=os.getenv("MYSQL_PWD"),
	database=os.getenv("MYSQL_DB")
)

log("SERVER_INITIATION", "connected to mysqldb")

#initialise mysql db controllers
user_control = dbmanager.UserControl(dbcon)
session_control = dbmanager.SessionControl(dbcon)
message_control = dbmanager.MessageControl(dbcon)

log("SERVER_INITIATION", "deployed mysqldb controllers")

app = Flask(__name__)
app.config['SECRET'] = os.getenv("FLASK_APP_SECRET")
app.config['TEMPLATES_AUTO_RELOAD'] = True

socketio = SocketIO(app, cors_allowed_origins="*")

log("SERVER_INITIATION", "deployed flask app and socketio")


@app.route('/')
def index():
	return render_template("index.html")

@app.route('/chat')
def chat():
	return render_template("chat.html")

@app.route('/register')
def register():
	return render_template("register.html")

log("SERVER_INITIATION", "deployed flask app routes")

@socketio.on('get_messages')
def handle_get_messages():
	messages = message_control.get_all_messages()
	log("MESSAGE_FETCH_REQUEST", messages)
	return messages

@socketio.on('send_message')
def handle_message(message):
	log("MESSAGE_RECEIVED", message)
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
				emit('req_login_res', {'status': 3, 'data': {'uid': uid, 'uname': uname, 'acc_col': user_control.db_get_data(uid, 'acc_col')}})
				log("SESSION_CONFLICT", uname)
			else:
				emit('req_login_res', {'status': 0, 'data': {'uname': uname, 'acc_col': user_control.db_get_data(uid, 'acc_col'), 'uid': uid, 'sess_id': sess_id}})
				log("USER_LOGGED_IN", uname)
		else:
			emit('req_login_res', {'status': 2, 'data': {}})
			log("LOGIN_PASSWORD_CONFLICT", uname)
	else:
		emit('req_login_res', {'status': 1, 'data': {}})

@socketio.on('change_session')
def change_session(data):
	uid = data['uid']
	session_control.discard_session(session_control.get_sess_id(uid))
	log("SESSION_TRANSFERRED", data['uid'])
	sess_id = session_control.create_session(uid)
	return {'status': 0, 'data': {'sess_id': sess_id}}

@socketio.on('validate_session')
def validate_session(data):
	sess_id, uid = data['sess_id'], data['uid']
	log("SESSION_VALIDATION_REQUESTED", data['uid'])
	if session_control.is_session_valid(sess_id) and session_control.get_uid(sess_id) == uid:
		return {'status': 0}
		log("SESSION_VALIDATION_SUCCESS", data['uid'])
	else:
		return {'status': 1}
		log("SESSION_VALIDATION_FAILURE", data['uid'])

@socketio.on('logout')
def disconnect_user(data):
	print(f"{user_control.db_get_data(data['uid'], 'uname')} logged out")
	session_control.discard_session(session_control.get_sess_id(data['uid']))
	log("USER_LOGOUT", data['uid'])

@socketio.on('reqcol')
def getcol(data):
	emit('res_acc_col', user_control.db_get_data(user_control.db_get_uid(data['uid']), 'acc_col'))

@socketio.on('changecol')
def changecolor(data):
	user_control.db_update_data(data['uid'], data['col'], 'acc_col')

@socketio.on('reg_request')
def register_user(data):
	log("NEW_REGISTRATION_REQUEST", data['uname'])
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
		log("REGISTER_REQUEST_SUCCESS", data['uname'])
	else:
		emit('reg_response_failure')
		log("REGISTER_REQUEST_FAILURE", data['uname'])

@socketio.on('req_data')
def get_data(data):
	uid = session_control.get_uid(data[0])
	log("DB_DATA_REQUEST", uid + ": " + data[1])
	if uid is not None:
		emit('res_data', {'status': 0, 'data': user_control.db_get_data(uid, data[1])})
	else:
		emit('res_data', {'status': 1, 'data': {}})

log("SERVER_INITIATION", "deployed socketio handlers")

if __name__ == "__main__":
	log("SERVER_INITIATION", f"server going live @ {os.getenv("SOCKETIO_HOST")}:{os.getenv("SOCKETIO_PORT")}")
	socketio.run(app, debug=False, allow_unsafe_werkzeug=True, host=os.getenv("SOCKETIO_HOST"), port=int(os.getenv("SOCKETIO_PORT")))
