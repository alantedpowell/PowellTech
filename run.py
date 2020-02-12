# PowellTech © -- Powell Industries 2019
# Copyright 2019 (Pending)
# Run.py File

import os

from PT import app
from PT.routes import send_system_status_online_email, send_system_status_failure_email

def displayNotification(message,title=None,subtitle=None,soundname='/Users/Alante/Downloads/beyond-doubt.aiff'):
	"""
		Display an OSX notification with message title an subtitle
		sounds are located in /System/Library/Sounds or ~/Library/Sounds
	"""
	titlePart = ''
	if(not title is None):
		titlePart = 'with title "{0}"'.format(title)
	subtitlePart = ''
	if(not subtitle is None):
		subtitlePart = 'subtitle "{0}"'.format(subtitle)
	soundnamePart = ''
	if(not soundname is None):
		soundnamePart = 'sound name "{0}"'.format(soundname)

	appleScriptNotification = 'display notification "{0}" {1} {2} {3}'.format(message,titlePart,subtitlePart,soundnamePart)
	os.system("osascript -e '{0}'".format(appleScriptNotification))

if __name__ == '__main__':
	displayNotification("PowellTech.com Server Started. SSC has been completed.", "Alert | PowellTech © Server Started")
	mstr = 'Alert | PowellTech © Server has started'
	os.system('notify-send ' + mstr)
	send_system_status_online_email()
	app.run(debug=True)
else:
	displayNotification("PowellTech.com Server Terminated.", "Alert | PowellTech © Server Terminated")
	mstr = 'Alert | PowellTech © Server has been terminated.'
	os.system('notify-send ' + mstr)
	send_system_status_failure_email()
# PowellTech ©
# "Problem? No Problem."