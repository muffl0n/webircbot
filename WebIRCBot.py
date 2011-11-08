#! /usr/bin/env python
#
# Example program using ircbot.py.
#
# Joel Rosdahl <joel@rosdahl.net>

"""A simple example bot.

This is an example bot that uses the SingleServerIRCBot class from
ircbot.py.  The bot enters a channel and listens for commands in
private messages and channel traffic.  Commands in channel messages
are given by prefixing the text by the bot name followed by a colon.
It also responds to DCC CHAT invitations and echos data sent in such
sessions.

The known commands are:

    stats -- Prints some channel information.

    disconnect -- Disconnect the bot.  The bot will try to reconnect
                  after 60 seconds.

    die -- Let the bot cease to exist.

    dcc -- Let the bot invite you to a DCC CHAT connection.
"""

from ircbot import SingleServerIRCBot
from irclib import nm_to_n, nm_to_h, irc_lower, ip_numstr_to_quad, ip_quad_to_numstr

class WebIRCBot(SingleServerIRCBot):
	def __init__(self, channel, nickname, server, port=6667):
		SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
		self.channel = channel

	def on_nicknameinuse(self, c, e):
		c.nick(c.get_nickname() + "_")

	def on_welcome(self, c, e):
		c.join(self.channel)

	def on_privmsg(self, c, e):
		#self.do_command(e, e.arguments()[0])
		pass

	def on_pubmsg(self, c, e):
		#a = e.arguments()[0].split(":", 1)
		#if len(a) > 1 and irc_lower(a[0]) == irc_lower(self.connection.get_nickname()):
		#    self.do_command(e, a[1].strip())
		#return
		pass

	def quit(self):
		self.connection.quit("Using irclib.py")
		self.connection.disconnect("Using irclib.py")

	def privmsg(self, target, msg):
		self.connection.privmsg(target, msg)

	def join(self, channel, key = None):
		if key is not None:
			self.connection.join(channel, key)
		else:
			self.connection.join(channel)

	def part(self, channel):
		channel = channel.encode("utf-8")
		self.connection.part(channel)