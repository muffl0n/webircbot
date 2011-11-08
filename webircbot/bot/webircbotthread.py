import threading
from webircbot import *

class WebIRCBotThread(threading.Thread):	
	def __init__(self, channel, nickname, server, port):
		threading.Thread.__init__(self)
		self.bot = WebIRCBot(channel, nickname, server, port)
		
	def run(self):
		self.bot.start()
		
	def shutdown(self):
		self.bot.quit()
