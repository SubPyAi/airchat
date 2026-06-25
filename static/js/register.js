$(document).ready(function() {
			var socket = io.connect("http://127.0.0.1:5000")
			socket.on('message', function(data) {
				if(data=='notValid'){
					swal({
						title: "Error!",
						text: "These credentials have already been taken!",
						icon: "error",
						button: "OK",
					}).then((val) => {
						if(val){
							setTimeout(()=>{$('#id').focus()}, 200)
						}
					})
					$('#id').val() = '';
					$('#uname').val() = '';
				}
				if(data=="hmm"){
					swal({
						title: "INFO",
						text: "You can't have a username with the word 'owner' in it",
						icon: "info",
						button: 'OK',
					});
					$('#id').val() = '';
					$('#uname').val() = '';	
				}
				else {
					swal({
						title: "Successful!",
						text: "Your ID has been created!",
						icon: "success",
						background: "red",
						button: "OK",
					}).then((value) => {
						if(value){
							setTimeout(() => {window.location.href = "/";}, 700)
						}
					});
				}
			});
			var inputFeild = document.getElementById("id");
			inputFeild.addEventListener("keypress", function(event) {
				if (event.key === "Enter") {
					event.preventDefault();
					$('#createID').click();
				};
			});

			$('#createID').on('click', function () {
				if($('#id').val()!=''&&$('#uname').val()!=''){
					socket.emit('request_new_id', $('#id').val()+":"+$('#uname').val());
				}
			});
		})

		function redirectToChat(uname, uid){
			window.location.href='chat?u=' + uname[0].toString() + '&vr=true&ud=' + uid;
		}

		const splash = document.querySelector('.splash');
			document.addEventListener('DOMContentLoaded', (e)=>{
				setTimeout(()=>{
					splash.classList.add('display-none');
				}, 1000);
				setTimeout(()=>{
			document.querySelector('.input').focus()
		}, 1500)
			})