$(document).ready(function () {
	window.onbeforeunload = function () {
		socket.emit('client_disconnect', {'uname': uname, 'uid': uid});
	};
	const uname = localStorage.getItem("uname");
	const uid = localStorage.getItem("uid");
	const acc_col = localStorage.getItem("acc_col");
	const sess_id = localStorage.getItem("sess_id");

	console.log("Username: " + uname);
	console.log("User ID: " + uid);
	console.log("Account Color: " + acc_col);
	console.log("Session ID: " + sess_id);

	var socket = io.connect("http://127.0.0.1:5000")

	socket.on('connect', function () {
		console.log('Connected to server');
		socket.emit('validate_session', {'sess_id': sess_id, 'uid': uid}, (data) => {
			console.log('validating')
			if (data['status'] === 0) {
				console.log('session valid')
				socket.emit('reqcol', {'uid': uid}, (response) => {
					var selfcolo = data;
					var newColo = selfcolo;
					socket.emit('get_messages', (response) => {
						var messages = response;
						if (messages.length === 0) {
							$('#messages').empty();
						}
						else {
							for (var i = 0; i < messages.length; i++) {
								var msg = messages[i];
								$('#messages').append($('<div class="msgbox" style="background-color: #' + msg['acc_col'] + '; float: left; width: fit-content; margin-left: auto; margin-right: auto; max-width: 80%; border-radius: 5px; border-bottom-left-radius: 0px; padding: 4px;"><p style="color: rgba(255, 255, 255, 0.7);"></div><br>').text(msg['uname'] + ": " + msg['msg']));
								$('#messages').append($('<div style="height: 5px;"></div><br>'));
							}
						}
					});
					div = $('#messages');
					div.animate({
						scrollTop: div[0].scrollHeight
					}, 1000);
					activate_client(socket);;
				});
			}
			else if (data['status'] === 1) {
				console.log('session invalid')
				localStorage.removeItem("uname");
				localStorage.removeItem("uid");
				localStorage.removeItem("acc_col");
				localStorage.removeItem("sess_id");
				window.location.href = '/';
			};
		});
	})
})

function activate_client(socketa) {
	uid = localStorage.getItem("uid");
	uname = localStorage.getItem("uname");
	acc_col = localStorage.getItem("acc_col");
	var inputFeild = document.getElementById("message");
	inputFeild.addEventListener("keypress", function (event) {
		if (event.key === "Enter") {
			event.preventDefault();
			if ($('#message').val() != "") {
				socketa.emit('send_message', {'uname': uname, 'message': $('#message').val(), 'acc_col': localStorage.getItem("acc_col")});
				$('#message').val('');
				div.animate({
					scrollTop: div[0].scrollHeight
				}, 1000);
			}
			$('#message').focus();
		};
	});

	var headerl = document.getElementById("headerl");
	socketa.on('new_message', function (data) {
		console.log('new message received', data);
		$('#messages').append($('<div class="msgbox" style="background-color: #' + data['acc_col'] + '; float: left; width: fit-content; margin-left: auto; margin-right: auto; max-width: 80%; border-radius: 5px; border-bottom-left-radius: 0px; padding: 4px;"><p style="color: rgba(255, 255, 255, 0.7);"></div><br>').text(data['uname'] + ": " + data['msg']));
		$('#messages').append($('<div style="height: 5px;"></div><br>'));
		var div = $('#messages');
		div.animate({
			scrollTop: div[0].scrollHeight
		}, 700);
	});

	var btnOk = document.getElementById("btnOK");
	var inputFeild = document.getElementById("message");
	setTimeout(() => {
		headerl.classList.remove("headerl");
		headerl.classList.add("headerActive");
		inputFeild.focus();
	}, 2000);

	let colorIndicator = document.getElementById('color-indicator');
	const colorPicker = new iro.ColorPicker("#color-picker", { width: 70, color: acc_col.toString() });
	colorIndicator.style.backgroundColor = acc_col.toString();
	btnOk.style.backgroundColor = acc_col.toString();
	colorPicker.on('color:change', function (color) {
		colorIndicator.style.backgroundColor = color.hexString;
		btnOk.style.backgroundColor = color.hexString;
	});

	$('#btnOK').on('click', function () {
		console.log('color change requested');
		selfcol = colorPicker.color.hexString;
		document.getElementById("color-indicator").classList.remove("color-indicator-active");
		socketa.emit('changecol', {'uid': uid, 'col': selfcol});
		localStorage.setItem("acc_col", selfcol);
	});
}
const splash = document.querySelector('.splash');
setTimeout(() => {
	splash.classList.add('display-none');
}, 2000);