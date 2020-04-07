import discord
import mysql.connector
import urllib.request
import json 

client = discord.Client()

cnxn = mysql.connector.connect(
  	host="localhost",
  	user="hexagoon",
  	password="hexagoon",
  	database="users",
  	auth_plugin='mysql_native_password'
)

crsr = cnxn.cursor()

org_repos_url = "https://api.github.com/users/hexadoon/repos"

def getGitUser(discordUser):
	crsr.execute("SELECT github_user FROM users WHERE discord_user = '" + discordUser + "'")
	rtrn = []
	for (github_user) in crsr:
		rtrn.append(github_user)
	return rtrn[0][0]

def getJSONfromURL(URL):
	with urllib.request.urlopen(URL) as open_url:
		return json.loads(open_url.read().decode())

@client.event
async def on_message(msg):
	msg_author = msg.author.name + "#" + str(msg.author.discriminator)
	if not msg.author.bot:
	 	if "!issues" in msg.content:
	 		issues_list = []
	 		github_user = getGitUser(msg_author)
	 		repos_json = getJSONfromURL(org_repos_url)
	 		for repo in repos_json:
	 			issues_json = getJSONfromURL((repo["issues_url"])[:-9]) # index may change depending on github api
	 			for issue in issues_json:
	 				if issue["state"] == "open":
	 					for assignee in issue["assignees"]:
	 						if assignee["login"] == github_user:
	 							issues_list.append(issue["title"] + "\n\n" + issue["body"] + "\n\n" + issue["html_url"])
	 		await msg.channel.send(msg.author.mention + ", you have `" + str(len(issues_list)) + "` unresolved issues.")
	 		for issue in issues_list:
	 			await msg.channel.send(issue)
	 	elif "!contributions" in msg.content:
	 		contributions = {}
	 		additions_total = 0
	 		deletions_total = 0
	 		github_user = getGitUser(msg_author)
	 		repos_json = getJSONfromURL(org_repos_url)
	 		for repo in repos_json:
	 			repo_name = repo["name"]
	 			contributions_json = getJSONfromURL(repo["url"] + "/stats/contributors")
	 			for user_contributions in contributions_json:
	 				if user_contributions["author"]["login"] == github_user:
	 					contributions[repo_name] = [0, 0]
	 					for week in user_contributions["weeks"]:
	 						contributions[repo_name][0] += week["a"]
	 						additions_total += week["a"]
	 						contributions[repo_name][1] += week["d"]
	 						deletions_total += week["d"]
	 		await msg.channel.send(msg.author.mention + ", you have made `" + str(additions_total) + "` additions and `" + str(deletions_total) + "` deletions.")
	 		for repo in contributions:
	 			await msg.channel.send(repo + ":(`" + str(contributions[repo][0]) + "`+ ; `" + str(contributions[repo][1]) + "`-)")

client.run('[INSERT DISCORD BOT TOKEN HERE]')