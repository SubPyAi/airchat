import os
import flask
import flask_socketio
from flask import Flask, render_template, redirect
from flask_socketio import SocketIO, send
from time import sleep

app = Flask(__name__)
app.config['SECRET'] = 'secret@nxgen8'
app.config['TEMPLATES_AUTO_RELOAD'] = True
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('message')
def handle_message(message):
	if 'usrconnected@nxgenServers' in message:
		try:
			misc, uname, uid = message.split('?')
			print(f"{uname} connected")
			with open('user.cfg', 'r') as f:
				usrdata = f.readlines()
				f.close()
			for i in range(0, len(usrdata)):
				if uid in usrdata[i]:
					a, b, c = usrdata[i].split(":")
					c = "online"
					newData = a + ":" + b + ":" + c + "\n"
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
			uid0, uname, status = i.split(':')
			if uid == uid0:
				status = status.replace('\n', '')
				if status=='online':
					send(uname + ':omghadfjkhyabweuirtagjdskgfbdsilagfbewayrnxaklsdjgf' + uid + ",online", broadcast=True)
					break
				else:
					send(uname + ':omghadfjkhyabweuirtagjdskgfbdsilagfbewayrnxaklsdjgf' + uid + ",found", broadcast=True)
					break
			else:
				uname = ''
		if uname == '':
			send(uname + ':omghadfjkhyabweuirtagjdskgfbdsilagfbewayrnxaklsdjgf' + uid + ",notfnd")
		else:
			pass
	else:
		send(message, broadcast=True)


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
	#socketio.send(f"{uname} left the room", broadcast=True)
	with open('user.cfg', 'r') as f:
		usrdata = f.readlines()
		f.close()
	for i in range(0, len(usrdata)):
		if uid in usrdata[i]:
			a, b, c = usrdata[i].split(":")
			c = "offline"
			newData = a + ":" + b + ":" + c + "\n"
			usrdata[i] = newData
			with open('user.cfg', 'w') as f:
				f.write("")
				f.writelines(usrdata)
				f.close()
		else:
			pass

@socketio.on('request_new_id')
def provide_id(data):
	nuid, nuname = data.split(':')
	with open('user.cfg', 'r') as f:
		usrdata = f.readlines()
		f.close()
	for i in range(0, len(usrdata)):
		a, b, c = usrdata[i].split(":")
		if nuid == a:
			send('notValid')
			fnd = True
			break
		elif "Owner" in nuname or "owner" in nuname:
			send("hmm")
			fnd = True
			break
		elif nuname == b:
			send('notValid')
			fnd = True
			break
		else:
			fnd = False
	if fnd == False:
		usrdata.append(f'{nuid}:{nuname}:offline\n')
		with open('user.cfg', 'w') as f:
			f.write('')
			f.writelines(usrdata)
			f.close()
		send('Done')
	else:
		pass


if __name__ == "__main__":
	socketio.run(app, debug=False, host='localhost', port=5000)