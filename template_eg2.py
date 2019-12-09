# -*- coding: utf-8 -*-

from flask import Flask

import pymongo
from flask import Flask,render_template, request,redirect, url_for,flash,session
from pymongo import MongoClient 
from bson import ObjectId
# from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo
import os, sys
# import bcrypt
import datetime
import hashlib
import json
import cgi
from bson import Binary, Code
from bson.json_util import dumps


client = MongoClient("localhost", 27017)

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
block_serialized = json.dumps(blocks[0], sort_keys=True).encode("utf-8")
abc = hashlib.sha256(block_serialized).hexdigest()
hashes.append(abc)

client = MongoClient("localhost", 27017)
database=client.casa

table_hospital=database.hospital

table_patient=database.patient

hash_control=database.patient_hash


@app.route("/",methods=["GET"])
def index():

	return render_template("home.html")
	

@app.route("/hospital",methods=["GET"])
def hospital():
	return render_template("hospital.html")

@app.route("/patient",methods=["GET"])
def patient():
	return render_template("patient.html")


@app.route("/pharma",methods=["GET"])
def pharma():
	return render_template("pharma.html")	

@app.route("/insurance",methods=["GET"])
def insurance():
	return render_template("insurance.html")

@app.route("/contact",methods=["GET"])
def contact():
	return render_template("contact.html")



@app.route("/hospital_credentials")
def hospital_signup():
	action=request.values.get('action')
	if(action=="signup"):
		return render_template("hospital_signup.html")
	elif(action=="login"):
		if request.method == 'POST':
	   		login_user=hospc.find({'name':request.form['name'], 'password':request.form['password']})
			if login_user and User.validate_login(login_user['password'], request.form['password']):
				return render_template("homepage2.html")
		flash("Wrong Login credentials")

@app.route("/homepage2",methods=["POST"])
def signup():

	if request.method == 'POST':
		# dd.collection('hospital').insert({'hospital_no':"request.values.get('hospital_no')",'name':"request.values.get('hospital_name')",'password':"request.values.get('password')",'landline':"request.values.get('landline')",'accrediation':"request.values.get('accrediation')",'address':"request.values.get('address')"})
		# flash("signup successful")
		hospital_no=request.values.get('hospital_no')
		hospital_name=request.values.get('name')
		password=request.values.get('password')
		landline=request.values.get('landline_no')
		accrediation=request.values.get('accrediation')
		address=request.values.get('address')
		
		print(type(address))
		#record=json.dumps()
		table_hospital.insert({"Hospital_no":hospital_no,"Hospital_name":hospital_name,"password":password,"Landline_no":landline,"Accrediation":accrediation,"address":address})
		#flash(record)
		return render_template("homepage2.html")

		


	# elif
	# 	return render_template("")

	# action=request.values.get('action')
	# if(action=="ARE YOU A HOSPITAL"):
   	#    return render_template("homepage2.html")
	# elif(action=="ARE YOU A PATIENT"):
	#    return render_template("patientlogin.html")

# @app.route("/hospital")
# def login():
# 	action=request.values.get('action')
# 	if(action=="login"):
#   	   return render_template("blockchain.html")
# 	#elif(action=="register"):
 	  # return render_template("registerdb.html")


@app.route("/patientmanage",methods=["POST"])
def verify():
	action=request.values.get('action')
	if(action=="newlogin"):
		return render_template("patient_info.html")
		# flash("Wrong Login credentials")
	# if request.method == 'POST':
	#    login_user=hospc.find_one({'name':request.form['name']})
	   
	#    if login_user:
	#       bcrypt.hashpw(request.form['password'].encode('utf-8'),login_user['password'].encode('utf-8'))==login_user['password'].encode('utf-8')
	     
	#       return render_template("blockchain.html")
	
	#    return render_template("error.html")

@app.route("/error")
def errors():
        return render_template("homepage2.html")
	   	

#@app.route("/logout")
#def logout():
#	session.pop('logged_in', None)
 #  	flash('You were logged out.')
  #  	return render_template("homepage1.html")

	


# @app.route("/block",methods=["POST"])
# def block():
# 	action=request.values.get('action')
# 	if(action=="search"):
#   	   return ''
# 	elif(action=="add"):
#  	   return ''
# 	elif(action=="create"):
#  	   return render_template("patient_info.html")

@app.route("/create_block",methods=["POST"])
def create():
	if request.method == 'POST':
		existing_user=table_patient.find_one({'name': request.form['name']})
	
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
		

		hashdoc=table_patient.insert({"name":name,"age":age,"occupation":occupation,"gender":gender,"email":email,"relation":relation,"date":date})
		
		
		hash1=hash(hashdoc)
		print(hash1)
		hash_control.insert({"hash":hash1})
		
		
		
		blocks.append([])
		global pID
		new_Block= {
			"prev_hash": hashes[pID-1],
			"dataValues": hash1,
			"datetime_object": date_Time()
					}
		block_serialized = json.dumps(new_Block, sort_keys=True).encode("utf-8")
		new_Hash = hashlib.sha256(block_serialized).hexdigest()
		blocks[pID].append(new_Block)
		hashes.append(new_Hash)	
		pID=pID+1
		print hashes
		print pID 
		


		
       	return render_template("homepage2.html")
		




	





if __name__=="__main__":
  app.secret_key = 'super secret key'
  app.config['SESSION_TYPE'] = 'filesystem'
  app.run(debug=True,port=8089)


