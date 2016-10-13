var fs = require('fs'),
	socket = require('socket.io'),
	http = require('http'),
	async = require('async');
	simple_cli = fs.readFileSync(__dirname + '/simple_cli.htm');

var deviceName = process.argv[2];
var bufferSize = parseInt(process.argv[3]);
var port = parseInt(process.argv[4]);
var deviceType = process.argv[5];
var inFD = 3;

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
		clients.push(socket);
	
		socket.on('getInfo', function() {
			socket.emit('info', {'deviceName' : deviceName, 'bufferSize' : bufferSize, 'type' : deviceType});
		});

		socket.on('write', function(data) {
			process.stdout.write(data);
		});
	});

	function emitToClients(data) {
		clients.forEach(function(client){
			client.emit('data', data);
		});
	};

	app.listen(port);
	async.forever(
		//Main Loop
		function(next){
			if(clients.length > 0){
				var buffer = new Buffer(bufferSize);
				fs.read(inFD, buffer, 0, bufferSize, null, function(err, bytesRead, buffer){
					if(bytesRead > 0){
						emitToClients(buffer.slice(0, bytesRead).toJSON());
					}
				});
			}
			setTimeout(next, 50);

		},
	        function (err) {
	    		console.log('end ' + err);
	        }
	);

})();



