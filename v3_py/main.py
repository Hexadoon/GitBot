import bot
import util

# def check_minutely():
# 	while True:
# 		crsr.execute("SELECT * FROM reminders")

# 		all_rem = crsr.fetchall()

# 		for rem in all_rem:
# 			if rem[0] - time.time() < 3600:
# 				notifs = rem[1].split(",")
# 				crsr.execute("DELETE FROM reminders WHERE remtime = " + rem[0] + ";")
# 				crsr.commit()

# 				for u in notifs:
# 					m = bot.get_user(u)
# 					m.dm_channel.send(m.mention + " - Reminder for " + time.strftime('%m/%d/%Y %H:%M', time.localtime(rem[0])))


# reminders_thread = Thread(target = check_minutely)
hexagoon = bot.Hexagoon()
hexagoon.run('[INSERT DISCORD BOT TOKEN HERE]')