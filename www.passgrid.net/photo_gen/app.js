var express = require('express');
var http = require('http');
var fs = require('fs');
var child_process = require('child_process');
var crypto = require('crypto');
var app = express();


app.get('/:url', function(req, res){

	getPic(req.params.url, function(path){
		var img = fs.readFileSync(path);
		res.writeHead(200, {'Content-Type':'image/png'});
		res.end(img, 'binary');
	});

});

// Spawns a phantomjs process to take screenshot of the given url
function getPic(url, callback){

	filename = crypto.createHash('sha1').update(url).digest('hex');

	ps = child_process.spawn('lib/phantomjs/bin/phantomjs', ['lib/capture.js', url, filename]);

	var blob = '';
	ps.stdout.on('data', function(data){
		blob += data;
	});

	ps.stdout.on('end', function(){
		console.log(blob);
	});

	ps.stderr.on('data', function(data){
		console.log('stderr: ' + data);
	});


	// Once screenshot is taken, crop it using imageMagick
	ps.on('exit', function(code){
	});
}

app.listen(3000);
console.log("Listening at localhost:3000");