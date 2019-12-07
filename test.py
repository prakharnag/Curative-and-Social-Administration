# -*- coding: utf-8 -*-
from flask import Flask,render_template, request,redirect, url_for,flash,session
from pymongo import MongoClient 
from bson import ObjectId
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo
#from flask.ext.pymongo import PyMongo
#from pymongo import PyMongo 
#from flash_pymongo import PyMongo
import os, sys
import bcrypt
import datetime
import hashlib
import json

def date_Time():
 obj_Date_Time=datetime.datetime.now()
 return obj_Date_Time.__str__()
app=Flask(__name__)

blocks= []
blocks.append([])
Genesis = {
 		"prev_hash": None,
 		"dataValues": "Just Initialising",
 		"datetime_object": date_Time()
	}
blocks[0].append(Genesis)
hashes=[]
pID=1
PID=1
block_serialized = json.dumps(blocks[0], sort_keys=True).encode("utf-8")
abc = hashlib.sha256(block_serialized).hexdigest()
hashes.append(abc)


client = MongoClient("localhost", 27017)

hospd = client.hospital_db		#database for hospital
hospc=hospd.hospital_info		#collection(table) to store documents of hospital 

pat_info=hospd.patient_info		#collection(table) to store documents of patient 

hash_control=hospd.hash_info		#collection to store hash values of patient's document

			


			
@app.route("/",methods=["GET"])
def index():

	return render_template("homepage1.html")


@app.route("/homepage2")
def homepage2():
	action=request.values.get('action')
	if(action=="ARE YOU A HOSPITAL"):
   	   return render_template("homepage2.html")
	elif(action=="ARE YOU A PATIENT"):
	   return render_template("patientlogin.html")

@app.route("/hospital")
def login():
	action=request.values.get('action')
	if(action=="login"):
  	   return render_template("blockchain.html")
	#elif(action=="register"):
 	  # return render_template("registerdb.html")


@app.route("/hospitalloginverify",methods=["POST"])
def verify():
	if request.method == 'POST':
	   login_user=hospc.find_one({'name':request.form['name']})
	   
	   if login_user:
	      bcrypt.hashpw(request.form['password'].encode('utf-8'),login_user['password'].encode('utf-8'))==login_user['password'].encode('utf-8')
	     
	      action=request.values.get('action')
	      if(action=="exlogin"):
	         return render_template("blockchain.html")
	      elif(action=="newlogin"):
	       return render_template("patient_info.html")
	   return render_template("error.html")

@app.route("/error")
def errors():
        return render_template("homepage2.html")
	   	

#@app.route("/logout")
#def logout():
#	session.pop('logged_in', None)
 #  	flash('You were logged out.')
  #  	return render_template("homepage1.html")

	


@app.route("/block",methods=["POST"])
def block():
	action=request.values.get('action')
	if(action=="search"):
 	   return render_template("patient_info.html")

@app.route("/create_block",methods=["POST"])
def create():
	if request.method == 'POST':
		existing_user=pat_info.find_one({'name': request.form['name']})
	
	if existing_user is None:
		
		name=request.values.get('name')
		age=request.values.get('age')
		
		occupation=request.values.get('occupation')
		gen=request.values.get('gender')
		if(gen=="male"):
			gender="Male"
		elif(gen=="female"):
			gender="Female"
		elif(gen=="other"):
			gender="Other"
		address=request.values.get('address')
		contact=request.values.get('contact')
		email=request.values.get('email')
		relation=request.values.get('relation')
		date = datetime.datetime.now()
		print (pID)

		hashdoc=pat_info.insert({"pID": pID,"name":name,"age":age,"occupation":occupation,"gender":gender,"email":email,"relation":relation,"date":date})
		
		
		hash1=hash(hashdoc)
		print(hash1)
		hash_control.insert({"hash":hash1})

		blocks.append([])
		global PID
		new_Block= {
			"prev_hash": hashes[PID-1],
			"dataValues": hash1,
			"datetime_object": date_Time()
					}
		block_serialized = json.dumps(new_Block, sort_keys=True).encode("utf-8")
		new_Hash = hashlib.sha256(block_serialized).hexdigest()
		blocks[PID].append(new_Block)
		hashes.append(new_Hash)	
		PID=PID+1
		pID=pID+1
		print (hashes)
		print (PID 
		#return render_template("homepage2.html")
		#flash("Your are successfully registered login to procced")
    		#return render_template("homepage2.html")


@app.route("/searchblock",methods=["POST"])
def search():
	
	#if request.method == 'POST':
		enter_pidd=request.values.get('pID')	
		print enter_pidd	
		enter_pid=int(enter_pidd)
		print type(enter_pid)
		sid=enter_pid
		if(sid==enter_pid):
			myquery = { "pID": enter_pid }
			mydoc =pat_info.find(myquery)
			
			for x in mydoc:
			   print(x)
		  # flash(x)
		
		searched_pID=1
		print type(searched_pID)
		#enter_pID=1
		#if(searched_pID==enter_pID):
		#	myquery = { "pID": enter_pID }
		#	mydoc =pat_info.find(myquery)
			
		#	for x in mydoc:
	  	#		 print(x)
       
				
		return render_template("blockchain.html")

				
			



	





if __name__=="__main__":
  app.secret_key = 'super secret key'
  app.config['SESSION_TYPE'] = 'filesystem'
  app.run(debug=True,port=8089)


