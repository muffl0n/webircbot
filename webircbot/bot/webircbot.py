# Based on example program by Joel Rosdahl <joel@rosdahl.net>

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
		self.connection.part(channel)