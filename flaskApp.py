from __future__ import with_statement

from functools import wraps
from flask import Flask, render_template, redirect, url_for, request, flash, session
from webircbotthread import *

import logging, logging.config
import os
import ConfigParser

app = Flask(__name__)
app.secret_key = '\x1bf\xa2\xf5\x81u;\xfa\xc8\x88?\xc7\x91\x99\x15k\xb4\xc5|Am\xe7\x9f1'

bot_thread = None

logging.config.fileConfig('conf/logging.conf')
log = logging.getLogger(os.path.basename(__file__))

config = ConfigParser.RawConfigParser()
config.read('conf/bot.conf')

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


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		session['login'] = request.form['login']
		app.logger.info('login for %s', session['login'])
		return redirect(url_for('index'))
	return render_template('login.html')

@app.route('/logout')
def logout():
	session.pop('login', None)
	return redirect(url_for('index'))

@app.route('/')
@login_required
def index():
	bot_running = bot_thread != None
	channels = []
	if bot_running:
		channels = bot_thread.bot.channels
	return render_template('index.html', bot_thread=bot_thread, channels=channels)

@app.route('/start')
@login_required
def start():
	global bot_thread
	home_channel = config.get('IRC', 'home_channel')
	nickname = config.get('IRC', 'nickname')
	server = config.get('IRC', 'server')
	port = config.getint('IRC', 'port')
	bot_thread = WebIRCBotThread(home_channel, nickname, server, port)
	bot_thread.start()
	flash("Bot started with config: %s" % config.items('IRC'))
	app.logger.info("Bot started with config: %s" % config.items('IRC'))
	return redirect(url_for('index'))
    
@app.route('/stop')
@login_required
def stop():
	global bot_thread
	bot_thread.shutdown()
	bot_thread = None
	flash("Bot stopped")
	app.logger.info("Bot stopped")
	return redirect(url_for('index'))

@app.route('/privmsg', methods=['GET', 'POST'])
@login_required
def privmsg():
	global bot_thread
	if request.method == 'POST':
		target = request.form['target']
		msg = request.form['msg']
	else:
		target = request.args.get('target', '')
		msg = request.args.get('msg', '')
	bot_thread.bot.privmsg(target, msg)
	flash("Sent message '%s' to '%s'" % (msg, target))
	app.logger.info("Sent message '%s' to '%s'" % (msg, target))
	return redirect(url_for('index'))

@app.route('/join', methods=['GET', 'POST'])
@login_required
def join():
	global bot_thread
	channel = request.form['channel']
	key = request.form['key']
	if key:
		bot_thread.bot.join(channel, key)
		flash("Joined channel '%s' with key '%s'" % (channel, key))
		app.logger.info("Joined channel '%s' with key '%s'" % (channel, key))
	else:
		bot_thread.bot.join(channel)
		flash("Joined channel '%s'" % (channel))
		app.logger.info("Joined channel '%s'" % (channel))
	return redirect(url_for('index'))
	
@app.route('/part')
@login_required
def part():
	global bot_thread
	channel = request.args.get('channel', '')
	bot_thread.bot.part(channel)
	flash("Parted channel '%s'" % (channel))
	app.logger.info("Parted channel '%s'" % (channel))
	return redirect(url_for('index'))

if __name__ == '__main__':
	app.run(debug=True)