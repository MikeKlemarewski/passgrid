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


getStream(win, fail);

/**
 * Signup, send the email link.
 */
var $signup = $("#signup").on("click", function(event) {
    event.preventDefault();
    event.stopPropagation();

    var $xhr = $.ajax({
        type: "POST",
        url: "/signup/",
        data: $("#signup-form").serialize(),
        success: function() {
            $signup.text("Sent");
        }
    });

    return false;
});

/**
 * Get the email and photo then submit them to the server.
 */
var $login = $("#login").on("click", function() {
    capture();

    var form = $("#login-form")[0];
    var email = $("#email").val();
    var data = canvas.toDataURL("image/png");
    var formData = new FormData(form);
    formData.append("passgrid", data);
    formData.append("email", email);

    var xhr = new XMLHttpRequest();
    xhr.open("POST", ".", true);
    // Make django happy!
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    xhr.send(formData);
    return false;
});

/**
 * Get AJAX ready for Django.
 */
var csrftoken = $("input[name=csrfmiddlewaretoken]").val();

$.ajaxSetup({
    crossDomain: false,
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
});
