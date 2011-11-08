from flask import Flask
app = Flask(__name__)
app.secret_key = '\x1bf\xa2\xf5\x81u;\xfa\xc8\x88?\xc7\x91\x99\x15k\xb4\xc5|Am\xe7\x9f1'

import web.views
