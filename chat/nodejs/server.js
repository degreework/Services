//	Customization

var appPort = 4000;

// Librairies

var express = require('express'), app = express();
var http = require('http')
  , server = http.createServer(app)
  , io = require('socket.io').listen(server);

var _ = require('underscore');


//var redis = require('socket.io/node_modules/redis');
//var sub = redis.createClient();
 
//Subscribe to the Redis chat channel
//sub.subscribe('chat');

//var jade = require('jade');
// var io = require('socket.io').listen(app);
var pseudoArray = []; //block the admin username (you can disable it)

// Views Options
/*
app.set('views', __dirname + '/views');
app.set('view engine', 'jade');
app.set("view options", { layout: false });
*/
app.use(express.static(__dirname + '/public'));

// Render and send the main page
/*
app.get('/', function(req, res){
  res.render('home.jade');
});*/
server.listen(appPort);
// app.listen(appPort);
console.log("Server listening on port " + appPort);

// Handle the socket.io connections

var users = 0; //count the users

io.sockets.on('connection', function (socket) { // First connection
	users += 1; // Add 1 to the count

	

	socket.on('message', function (data) { // Broadcast the message to all
		
		//if(pseudoSet(socket))
		//{

			console.log(socket.codigo)
			var transmit = {date : new Date().toISOString(), pseudo : socket.nickname, message : data.msg};
			//socket.broadcast.emit('message', transmit);
			io.to(data.to).emit('message', transmit);
			console.log("user "+ transmit['pseudo'] +" said \""+data+"\"");
			console.log("user send the msg");
		//}
	});
	socket.on('addUser', function (data) { // Assign a name to the user
			
			console.log('addUser')
			console.log(data)
			pseudoArray.push(data);
			console.log("user connected and add to the list");
			
			socket.codigo = data.codigo
			socket.room = data.id	
			console.log('aqui')	
			socket.join(data.id);
			console.log('alli')	
			reloadUsers();
		
	});
	socket.on('listChatUpdate', function () { // Broadcast the message to all
		console.log('listChat')
		reloadUsers(); // Send the count to all the users
		
	});
	socket.on('leave', function (data) { // Disconnection of the client		
		
			console.log("leave...")

			// elimina al usuario del arreglo 
			_.each(pseudoArray, function(item){
				if (item.codigo === data.codigo) {
					pseudoArray = _.without(pseudoArray, item)
				};
    		});

    		//socket.leave(data.id);

			// renderiza sin el usuario
    		reloadUsers();
	});
});

function reloadUsers() { // Send the count of the users to all
	io.sockets.emit('nbUsers', pseudoArray);
}