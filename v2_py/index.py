import discord
import mysql.connector
import urllib.request
import json 

client = discord.Client()

cnxn = mysql.connector.connect(
  	host="localhost",
  	user="hexagoon",
  	password="hexagoon",
  	database="users"
)

crsr = cnxn.cursor()

org_repos_url = "https://api.github.com/users/hexadoon/repos"

def getGitUser(discordUser):
	cursor.execute("SELECT github_user FROM users WHERE discord_user = '" + discordUser + "'")
	return cursor[0][0]

def getJSONfromURL(URL):
	with urllib.request.urlopen(URL) as open_url:
		return json.loads(open_url.read().decode())

@client.event
async def on_message(msg):
    if !msg.author.bot:
    	if "!issues" in msg.content:
    		github_user = getGitUser(msg.author.tag)
    		repos_json = getJSONfromURL(org_repos_url)
    		print(repos_json)
    		# for repo in repos_json:
    		# 	issues_json = getJSONfromURL(repo.issues_url[:-9]) # index may change depending on github api
    		# 	for issue in issues_json:
    		# 		if issue.state == "open"
    		# 			for assignee in issue.assignees:
    		# 				if assignee.login == github_user:
    		# 					msg.reply(issue.title + "\n\n" + issue.body + "\n\n" + issue.html_url)


client.run('[INSERT DISCORD BOT TOKEN HERE]')