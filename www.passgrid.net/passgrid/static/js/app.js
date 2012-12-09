// http://127.0.0.1:3000/
// http://openetherpad.org/q99V0ujRlP

var video = document.getElementById('video');
var canvas = document.getElementById('canvas');
var link = document.getElementById('control');

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



getStream(win, fail);

document.getElementById("snap").onclick = function(event) {
    event.preventDefault();
    event.stopPropagation();
    snap();
};