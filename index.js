const Discord = require('discord.js');
const fetch = require('node-fetch');
const mysql = require('mysql');

const client = new Discord.Client();

const cnxn = mysql.createConnection({
  	host: "localhost",
  	user: "hexagoon",
  	password: "hexagoon",
  	database: "users"
});

cnxn.connect();

var getGit = (discord_user) => {
	cnxn.query(("SELECT github_user FROM users WHERE discord_user = '" + discord_user + "'"), function (err, result, fields) {
		if (err) throw err;
		return result[0].github_user;
	});
}

client.on('message', msg => {
	if (!msg.author.bot){
		if(msg.content.toLowerCase().indexOf('!issues') >= 0){
			var github_user = getGit(msg.author.username);
			fetch('https://api.github.com/users/hexadoon/repos')
				.then(resp => resp.json())
				.then(function(data){
					for(var i = 0; i < data.length; i++){
						console.log(data[i].subscribers_url);
					}
				})
		}else{
			const mtns = msg.mentions.users.array();
			for (var k in mtns){
				if (mtns[k].bot){
					msg.reply('Use `!howto` for valid commands');
					break;
				}
			}
		}
	}
});

client.login('[INSERT DISCORD BOT TOKEN HERE]');