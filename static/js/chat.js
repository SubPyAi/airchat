$(document).ready(function () {
	window.onbeforeunload = function () {
		socket.emit('client_disconnect', uname + ":" + uid);
		socket.send(uname + ' left the room');
	};
	if (document.referrer == '') {
		window.location.href = '/'
	};
	const queryString = window.location.search;
	const urlParams = new URLSearchParams(queryString);
	const uname = urlParams.get('u');
	const idver = urlParams.get('vr');
	const uid = urlParams.get('ud');
	if (idver != 'true') {
		window.location.href = "/";
	}
	var socket = io.connect("http://127.0.0.1:5000")

	socket.on('connect', function () {
		socket.send('usrconnected@nxgenServers?' + uname + "?" + uid);
		socket.emit('reqcol', uid)
	});

	socket.on('res_acc_col', function (data) {
		var selfcolo = data;
		var newColo = selfcolo;
		helob(selfcolo, newColo, socket);
	});
})
function helob(selfcol, newCol, socketa) {
	const queryString = window.location.search;
	const urlParams = new URLSearchParams(queryString);
	const uname = urlParams.get('u');
	const uid = urlParams.get('ud');
	var inputFeild = document.getElementById("message");
	inputFeild.addEventListener("keypress", function (event) {
		if (event.key === "Enter") {
			event.preventDefault();
			if ($('#message').val() != "") {
				socketa.send(uname + ": " + $('#message').val() + "<:-:>" + selfcol.toString());
				$('#message').val('');
				var div = $('#messages');
				div.animate({
					scrollTop: div[0].scrollHeight
				}, 1000);
			}
			$('#message').focus();
		};
	});

	var headerl = document.getElementById("headerl");
	socketa.on('message', function (data) {
		if (data.includes('omghadfjkhyabweuirtagjdskgfbdsilagfbewayrnxaklsdjgf') != true) {
			misc = data.split(':');
			ord = data.split("<:-:>");
			if (misc[0] == uname) {
				$('#messages').append($('<div class="msgbox" style="background-color: ' + selfcol + '; float: left; width: fit-content; margin-left: auto; margin-right: auto; max-width: 80%; border-radius: 5px; border-bottom-left-radius: 0px; padding: 4px;"><p style="color: rgba(255, 255, 255, 0.7);"></div><br>').text(ord[0]));
				$('#messages').append($('<div style="height: 5px;"></div><br>'));
				var div = $('#messages');
				div.animate({
					scrollTop: div[0].scrollHeight
				}, 700);
			}
			else {
				$('#messages').append($('<div style="background: ' + ord[1] + '; float: right; width: fit-content; margin-left: auto; margin-right: auto; max-width: 80%; border-radius: 5px; border-bottom-right-radius: 0px; padding: 4px;"><p style="color: rgba(255, 255, 255, 0.7);"></div><br>').text("  " + ord[0] + ""));
				$('#messages').append($('<div style="height: 5px;"></div><br>'));
				headerl.classList.remove("headerActive")
				headerl.classList.add("headerActiveMsgExpand")
				setTimeout(() => {
					headerl.classList.remove("headerActiveMsgExpand")
					headerl.classList.add("headerActive")
				}, 500)
				var div = $('#messages');
				div.animate({
					scrollTop: div[0].scrollHeight
				}, 700);
			}
		}
		else {
			msg = data.split(":");
			in2 = msg[1].split(",");
			if (in2[1] != 'online') {
				setTimeout(() => {
					$('#messages').append($('<div style="width: fit-content; margin-left: auto; margin-right: auto; max-width: 80%; border-radius: 5px; padding: 4px;"><p style="color: rgba(255, 255, 255, 0.7);"></div>').text("  " + msg[0] + ' joined the room' + "  "));
					$('#messages').append($('<div style="height: 5px;"></div>'));
				}, 3000);
			}
		}
	});

	var btnOk = document.getElementById("btnOK");
	var inputFeild = document.getElementById("message");
	setTimeout(() => {
		headerl.classList.remove("headerl");
		headerl.classList.add("headerActive");
		inputFeild.focus();
	}, 2000);

	let colorIndicator = document.getElementById('color-indicator');
	const colorPicker = new iro.ColorPicker("#color-picker", { width: 70, color: newCol.toString() });
	colorIndicator.style.backgroundColor = newCol.toString();
	btnOk.style.backgroundColor = newCol.toString();
	colorPicker.on('color:change', function (color) {
		colorIndicator.style.backgroundColor = color.hexString;
		btnOk.style.backgroundColor = color.hexString;
	});

	$('#btnOK').on('click', function () {
		selfcol = colorPicker.color.hexString;
		document.getElementById("color-indicator").classList.remove("color-indicator-active");
		socketa.emit('changecol', uid + ":" + selfcol);
	});
}
const splash = document.querySelector('.splash');
setTimeout(() => {
	splash.classList.add('display-none');
}, 2000);