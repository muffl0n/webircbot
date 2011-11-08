from __future__ import with_statement
from functools import wraps

from flask import Flask, session, redirect, url_for
import logging, logging.config
import os
import ConfigParser
import pprint

app = Flask(__name__)
app.secret_key = '\x1bf\xa2\xf5\x81u;\xfa\xc8\x88?\xc7\x91\x99\x15k\xb4\xc5|Am\xe7\x9f1'

logging.config.fileConfig('webircbot/conf/logging.conf')
log = logging.getLogger(os.path.basename(__file__))

config = ConfigParser.RawConfigParser()
config.read('webircbot/conf/bot.conf')

bot_thread = None

def get_log_file_contents(): 
	lines = []
	with open("webIRCBot.log") as f:
		for line in f:
			lines.append(line)
	del lines[0:len(lines)-20]
	return lines
	
app.jinja_env.globals.update(get_log_file_contents=get_log_file_contents)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'login' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


import views
