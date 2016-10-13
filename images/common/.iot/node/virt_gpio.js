var fs = require('fs'),
	socket = require('socket.io'),
	http = require('http'),
	async = require('async');
	simple_cli = fs.readFileSync(__dirname + '/simple_cli.htm');

var deviceName = process.argv[2];
var path = process.argv[3];
var port = parseInt(process.argv[4]);
var deviceType = process.argv[5];


(function(){
	var app = http.createServer(function(req, res) {
	    res.setHeader('Access-Control-Allow-Origin', 'http://localhost:' + port);
	    res.writeHead(200, {'Content-Type': 'text/html'});
	    res.end(simple_cli);
	});

	var io = socket.listen(app);
	io.set("origins", "*:*");

	var clients = [];

	io.on('connection', function(socket) {
		socket.on('getInfo', function() {
			socket.emit('info', {'deviceName' : deviceName, 'path' : path, 'type' : deviceType});
		});

		socket.on('write', function(data) {
			fs.writeFile(path, data, function(err) {
			    if(err) {
				return console.log(err);
			    }
			}); 
		});
		socket.on('read', function() {
			fs.open(path, 'r', function(status, fd) {
			    if (status) {
				console.log(status.message);
				return;
			    }
			    var buffer = new Buffer(1);
			    fs.read(fd, buffer, 0, 1, 0, function(err, num) {
				socket.emit('data', buffer.toString('utf8', 0, num));
			    });
			});
		});
	});
	app.listen(port);
})();



