$(document).ready(function () {
    var socket = io.connect("http://127.0.0.1:5000");
    var requestedUname = false;

    if (localStorage.getItem("uname") && localStorage.getItem("uid") && localStorage.getItem("sess_id")) {
        requestedUname = true;
        socket.emit('validate_session', {'sess_id': localStorage.getItem("sess_id"), 'uid': localStorage.getItem("uid")}, (response) => {
        if (response['status'] === 0) {
            swal({
                title: "Active Session!",
                text: "The previous session of this device with the username " + localStorage.getItem("uname") + " is still active. Do you want to continue with the existing session or discard it?",
                icon: "warning",
                buttons: {
                    continue: {
                        text: "Continue",
                        value: "continue"
                    },
                    discard: {
                        text: "Discard",
                        value: "discard"
                    }
                }
            }).then((value) => {
                if (value === "continue") {
                    window.location.href = "chat";
                } else {
                    localStorage.removeItem("uname");
                    localStorage.removeItem("uid");
                    localStorage.removeItem("acc_col");
                    localStorage.removeItem("sess_id");
                }
            });
        }
        else {
            localStorage.removeItem("uname");
            localStorage.removeItem("uid");
            localStorage.removeItem("acc_col");
            localStorage.removeItem("sess_id");
        }
    });
    }

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
        else if (data['status'] === 3) {
            swal({
                title: "Error!",
                text: "An active session already exists for this user. Do you want to shift it to this browser?",
                icon: "error",
                buttons: {
                    yes: {
                        text: "Yes",
                        value: "Yes"
                    },
                    no: {
                        text: "No",
                        value: "No"
                    }
                }
            }).then((val) => {
                if (val == "No") {
                    setTimeout(() => { $("#uname").focus(); }, 200);
                }
                else {
                    socket.emit('change_session', {'uid': data['data']['uid']}, (response) => {
                        if (response['status'] === 0) {
                            localStorage.setItem("uname", data['data']['uname']);
                            localStorage.setItem("uid", data['data']['uid']);
                            localStorage.setItem("acc_col", data['data']['acc_col']);
                            localStorage.setItem("sess_id", response['data']['sess_id']);
                            redirectToChat(data['data']['uid'], data['data']['uname']);
                        }
                    });
                }
            });
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
            socket.emit('req_login', {'uname': $("#uname").val(), 'passwd': $("#pwd").val()});
        }
    });
});

function redirectToChat(uname, uid) {
    window.location.href = "chat";
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
