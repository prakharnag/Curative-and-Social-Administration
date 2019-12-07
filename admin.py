# -*- coding: utf-8 -*-
from flask import Flask
app=Flask(__name__)

@app.route("/")
def index():
	return"YEs it is working"





if __name__=="__main__":
  app.secret_key = 'super secret key'
  app.config['SESSION_TYPE'] = 'filesystem'
  app.run(debug=True,port=8089)
