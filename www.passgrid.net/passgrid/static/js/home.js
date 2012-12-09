// http://127.0.0.1:3000/
// http://openetherpad.org/q99V0ujRlP

var video = document.getElementById('video');
var canvas = document.getElementById('canvas');
var link = document.getElementById('control');
var email = document.getElementById('email');

var isWebkit = false;

var getStream = function(win, fail) {
    var getUserMedia;
    if (navigator.getUserMedia) {
        getUserMedia = 'getUserMedia';
    } else if (navigator.webkitGetUserMedia) {
        getUserMedia = 'webkitGetUserMedia';
        isWebkit = true;
    } else {
        return fail();
    };

    navigator[getUserMedia]({video: true}, win, fail);
};

var win = function(stream) {
    var source = isWebkit ? webkitURL.createObjectURL(stream) : stream;
    video.src = source;
    // setTimeout(snap, 1000);
};

var fail = function() {
    console.log("BOOM", arguments)
    alert("BOOM");
};

/**
 * Grab data from the canvas.
 */
var capture = function() {
    var context = canvas.getContext("2d");
    context.clearRect(0, 0);
    context.drawImage(video, 0, 0);
};

/**
 * Get the email and photo then submit them to the server.
 */
var submitLogin = function(form) {
    capture();


    var csrftoken = document.querySelector("input[name=csrfmiddlewaretoken]").value;
    var email = document.querySelector("#email").value;


    console.log('SUBMITING:', csrftoken, email);

    var data = canvas.toDataURL("image/png");
    var formData = new FormData(form);
    formData.append("passgrid", data);
    formData.append("email", email);

    var xhr = new XMLHttpRequest();
    xhr.open("POST", ".", true);
    // CSRF_REQUEST_WITH

    // Make django happy.
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    xhr.onload = function(e) {
    };


    // multipart/form-data
    xhr.send(formData);
    return false;
};

getStream(win, fail);

document.getElementById("verify").onclick = function(event) {
    event.preventDefault();
    event.stopPropagation();
    submitLogin();
};

document.getElementById("send").onclick = function(event) {
    //event.preventDefault();
    //event.stopPropagation();
    //submitLogin();
};