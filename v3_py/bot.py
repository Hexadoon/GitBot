import discord
import sqlite3
import urllib.request
import json 
import sys
from datetime import datetime
import time
from threading import Thread

import util

'''
    Core of the Hexagoon bot.
'''

class Hexagoon(discord.Client):

    async def on_ready(self):
        print("[Hexagoon] Launched successfully.")

    async def on_message(self, msg):
        msg_author = msg.author.name + "#" + str(msg.author.discriminator)
        if not msg.author.bot:

            if "!issues" in msg.content:

                github_user = ""

                if len(msg.mentions) > 0:
                    target = msg.mentions[0].name + "#" + str(msg.mentions[0].discriminator)
                    github_user = util.get_git_user(target)
                else:
                    github_user = util.get_git_user(msg_author)

                issues_list = []
                repos_json = util.get_json_from_url(util.org_repos_url)

                if github_user != None:
                    for repo in repos_json:
                        issues_json = util.get_json_from_url((repo["issues_url"])[:-9]) # index may change depending on github api
                        for issue in issues_json:
                            if issue["state"] == "open":
                                for assignee in issue["assignees"]:
                                    if assignee["login"] == github_user:
                                        issues_list.append(issue["title"] + "\n\n" + issue["body"] + "\n\n" + issue["html_url"])
                    
                    target = ""
                    if len(msg.mentions) > 0:
                        target = msg.mentions[0]
                    else:
                        target = msg.author

                    await msg.channel.send(target.mention + ", you have `" + str(len(issues_list)) + "` unresolved issues.")
                    for issue in issues_list:
                        await msg.channel.send(issue)
                else:
                    await msg.channel.send("User not in database")

            elif "!contributions" in msg.content:

                github_user = ""
                
                if len(msg.mentions) > 0:
                    target = msg.mentions[0].name + "#" + str(msg.mentions[0].discriminator)
                    github_user = util.get_git_user(target)
                else:
                    github_user = util.get_git_user(msg_author)

                contributions = {}
                additions_total = 0
                deletions_total = 0
                repos_json = util.get_json_from_url(util.org_repos_url)

                if github_user != None:
                    for repo in repos_json:
                        repo_name = repo["name"]
                        contributions_json = util.get_json_from_url(repo["url"] + "/stats/contributors")
                        for user_contributions in contributions_json:
                            if user_contributions["author"]["login"] == github_user:
                                contributions[repo_name] = [0, 0]
                                for week in user_contributions["weeks"]:
                                    contributions[repo_name][0] += week["a"]
                                    additions_total += week["a"]
                                    contributions[repo_name][1] += week["d"]
                                    deletions_total += week["d"]

                    target = ""
                    if len(msg.mentions) > 0:
                        target = msg.mentions[0]
                    else:
                        target = msg.author

                    await msg.channel.send(target.mention + ", you have made `" + str(additions_total) + "` additions and `" + str(deletions_total) + "` deletions.")
                    for repo in contributions:
                        await msg.channel.send(repo + ":(`" + str(contributions[repo][0]) + "`+ ; `" + str(contributions[repo][1]) + "`-)")
                else:
                    await msg.channel.send("User not in database")