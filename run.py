import sys
from webircbot import app

if (len(sys.argv) != 2):
	print "Usage: python %s <listen-ip>" % (sys.argv[0])
else:
	ip = sys.argv[1]
	app.run(host=ip,debug=True)

