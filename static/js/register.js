$(document).ready(function() {
			var socket = io.connect("http://127.0.0.1:5000")
			socket.on('reg_response_success', function(data) {
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
			});

			socket.on('reg_response_failure', function(data) {
				swal({
					title: "Error!",
					text: "These credentials have already been taken!",
					icon: "error",
					button: "OK",
				}).then((val) => {
					if(val){
						setTimeout(()=>{$('#uname').focus()}, 200)
					}
				})
				$('#uname').val() = '';
				$('#passwd').val() = '';
			});
			
			var inputFeild = document.getElementById("passwd");
			inputFeild.addEventListener("keypress", function(event) {
				if (event.key === "Enter") {
					event.preventDefault();
					$('#createID').click();
				};
			});

			$('#createID').on('click', function () {
				if($('#uname').val()!=''&&$('#passwd').val()!=''){
					socket.emit('reg_request', $('#uname').val()+":"+$('#passwd').val());
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