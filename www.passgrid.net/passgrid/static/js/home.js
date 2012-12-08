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

    setTimeout(snap, 1000);

};


var fail = function() {
    console.log("BOOM", arguments)
    alert("BOOM");
};

var snap = function() {
    var context = canvas.getContext("2d");
    context.clearRect(0, 0);
    context.drawImage(video, 0, 0);
};

var upload = function(form) {
  var data = canvas.toDataURL('image/png');
  var formData = new FormData( form);
  formData.append('passgrid', data);
  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/', true);
  xhr.onload = function(e) { console.log("onload")};

  xhr.send(formData);  // multipart/form-data
  
}



getStream(win, fail);

document.getElementById("snap").onclick = function(event) {
    event.preventDefault();
    event.stopPropagation();
    snap();
};


