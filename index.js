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

const errmsg = "an error has occurred, please contact admin."

cnxn.connect();

client.on('message', msg => {
	if (!msg.author.bot){
		if(msg.content.toLowerCase().indexOf('!issues') >= 0){
			cnxn.query("SELECT github_user FROM users WHERE discord_user = '" + msg.author.tag + "'", (err, request) => {
					var github_user = JSON.parse(JSON.stringify(request))[0].github_user;
					fetch('https://api.github.com/users/hexadoon/repos')
						.then(repos => repos.json())
						.then(function(repos_json){
							for(var i = 0; i < repos_json.length; i++){
								var issues_url = repos_json[i].issues_url.substring(0, repos_json[i].issues_url.indexOf("{"));
								fetch(issues_url)
									.then(issues => issues.json())
									.then(function(issues_json){
										for(var j = 0; j < issues_json.length; j++){
											for(var k = 0; k < issues_json[j].assignees.length; k++){
												if(issues_json[j].state === "open" && issues_json[j].assignees[k].login === github_user){
													msg.reply(issues_json[j].title + "\n\n" + issues_json[j].body + "\n\n" + issues_json[j].html_url);
												}
											}
										}
									})
									.catch(function(error){
										console.log(error);
										msg.reply(errmsg);
									});
							}
						})
						.catch(function(error){
							console.log(error);
							msg.reply(errmsg);
						});
				});
		}else if(msg.content.toLowerCase().indexOf('!contributions') >= 0){
			cnxn.query("SELECT github_user FROM users WHERE discord_user = '" + msg.author.tag + "'", (err, request) => {
					var github_user = JSON.parse(JSON.stringify(request))[0].github_user;
					var additions = 0;
					var subtractions = 0;
					fetch('https://api.github.com/users/hexadoon/repos')
						.then(repos => repos.json())
						.then(function(repos_json){
							for(var i = 0; i < repos_json.length; i++){
								var contributions_url = repos_json[i].url + "/stats/contributors";
								var repo_name = repos_json[i].name;
								fetch(contributions_url)
									.then(contributions => contributions.json())
									.then(function(contributions_json){
										for(var j = 0; j < contributions_json.length; j++){
											if(contributions_json[j].author.login === github_user){
												for(var k = 0; k < contributions_json[j].weeks.length; k++){
													additions += contributions_json[j].weeks[k].a;
													subtractions += contributions_json[j].weeks[k].d;
												}
											}
										}

										msg.reply(repo_name + ":(" + additions + "+ : " + subtractions + "- )");
									})
									.catch(function(error){
										console.log(error);
										msg.reply(errmsg);
									});
							}
						})
						.catch(function(error){
							console.log(error);
							msg.reply(errmsg);
						});
				});
		}else{
			const mtns = msg.mentions.users.array();
			for (var k in mtns){
				if (mtns[k].bot && mtns[k].username == "Hexagoon"){
					msg.reply('use `!howto` for valid commands');
					break;
				}
			}
		}
	}
});

client.login('[INSERT DISCORD BOT TOKEN HERE]');