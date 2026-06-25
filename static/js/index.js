$(document).ready(function () {
    var socket = io.connect("http://127.0.0.1:5000");
    var requestedUname = false;

    socket.on("req_login_res", function (data) {
        console.log("Received login response:", data);
        console.log(data['status']);
        console.log(data['data']['uname']);
        console.log(data['data']['uid']);
        if (data['status'] === 0) {
            localStorage.setItem("uname", data['data']['uname']);
            localStorage.setItem("uid", data['data']['uid']);
            localStorage.setItem("acc_col", data['data']['acc_col']);
            localStorage.setItem("sess_id", data['data']['sess_id']);
            redirectToChat(data['data']['uid'], data['data']['uname']);
        }
        else if (data['status'] === 1) {
            swal({
                title: "Error!",
                text: "User does not exist!",
                icon: "error",
                button: "OK"
            }).then((val) => {
                if (val) {
                    setTimeout(() => { $("#uname").focus(); }, 200);
                }
            })
            $("#uname").val("");
            $("#pwd").val("");
        }
        else if (data['status'] === 2) {
            swal({
                title: "Error!",
                text: "Incorrect password!",
                icon: "error",
                button: "OK"
            }).then((val) => {
                if (val) {
                    setTimeout(() => { $("#pwd").focus(); }, 200);
                }
            })
            $("#pwd").val("");
            $("#uname").val("");
        }
    });

    var inputFeild = document.getElementById("pwd");
    inputFeild.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            $("#btnLogin").click();
        }
    });

    $("#createID").on("click", function () {
        window.location.href = "register";
    });

    $("#btnLogin").on("click", function () {
        if ($("#uname").val() !== "") {
            socket.emit('req_login', $("#uname").val() + ":" + $("#pwd").val());
        }
    });
});

function redirectToChat(uname, uid) {
    window.location.href = "chat?u=" + uname[0].toString() + "&vr=true&ud=" + uid;
}

const splash = document.querySelector(".splash");
document.addEventListener("DOMContentLoaded", () => {
    setTimeout(() => {
        splash.classList.add("display-none");
    }, 1000);

    setTimeout(() => {
        document.querySelector(".input").focus();
    }, 1500);
});
