$(document).ready(function () {
    var socket = io.connect("http://127.0.0.1:5000");
    var requestedUname = false;

    socket.on("message", function (data) {
        if (requestedUname === true) {
            if (data.includes($("#id").val()) === true) {
                console.log(data);

                if (data.includes("online", -8) === true) {
                    console.log("done");
                    swal({
                        title: "ID already logged in!",
                        text: "This ID is already logged in!\ncontact the owner at advikdhangarreal@gmail.com if this is a mistake.",
                        icon: "info",
                        button: "OK"
                    }).then((val) => {
                        if (val) {
                            setTimeout($("#id").focus(), 200);
                        }
                    });
                    $("#id").val("");
                }

                if (data.includes("found", -8) === true) {
                    var user = data.split(":");
                    console.log(user);
                    var col = user[1].split("]");
                    var fcol = col[1].split(",");
                    var fccol = fcol[0].split("#");
                    redirectToChat(user, $("#id").val(), fccol[1]);
                }

                if (data.includes("found", -8) === false && data.includes("online", -8) !== true) {
                    $("#id").val("");
                    swal({
                        title: "Error!",
                        text: "These credentials are invalid!",
                        icon: "error",
                        button: "OK"
                    });
                }
            }
        }
    });

    var inputFeild = document.getElementById("id");
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
        if ($("#id").val() !== "") {
            socket.send($("#id").val() + ":" + "thisisaloginconfmsgufksjdhfbcushfadsg");
            requestedUname = true;
        }
    });
});

function redirectToChat(uname, uid, col) {
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
