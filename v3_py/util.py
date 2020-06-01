import sqlite3
import urllib.request
import json 
import sys
import time

from datetime import datetime
from threading import Thread

org_repos_url = "https://api.github.com/users/hexadoon/repos"
database_path = "users.db"

#
#	Start the database, exit on failure.
#
try:
	cnxn = sqlite3.connect("users.db")
	print('[Hexagoon] Connected to database.')
except:
	print('[Hexagoon] Cannot find database.')
	sys.exit(1)

crsr = cnxn.cursor()

def get_git_user(discordUser):
	crsr.execute("SELECT github_user FROM users WHERE discord_user = '" + discordUser + "'")
	rtrn = []
	for (github_user) in crsr:
		rtrn.append(github_user)

	if len(rtrn) == 0:
		return None
	return rtrn[0][0]

def get_json_from_url(URL):
	with urllib.request.urlopen(URL) as open_url:
		return json.loads(open_url.read().decode())