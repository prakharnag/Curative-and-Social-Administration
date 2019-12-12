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
from bson import json_util
import datetime
import ast
A=1
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



@app.route("/hospital_credentials",methods=["POST"])
def hospital_signup():
	action=request.values.get('action')
	if(action=="login"):
		name=request.values.get('name')
		print(type(name))
		password=request.values.get('password')
		query={"Hospital_name":name,"password":password}
		mydoc=table_hospital.find(query)

		for x in mydoc:
			# print x
			table_name=x["Hospital_name"]
			table_pass=x["password"]
			if(name==table_name and password==table_pass):
				return render_template("homepage2.html")
			elif(password!=table_pass):
				flash("Wrong Login credentials")
			x["_id"] = str(x["_id"])
			print x["password"]
			
		
	elif(action=="signup"):
		return render_template("hospital_signup.html")

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


@app.route("/patientmanage",methods=["POST"])
def verify():
	action=request.values.get('action')
	# if(action=="newlogin"):
	# 	return render_template("patient_info.html")
	if(action=="exlogin"):
		diagnostic_report=request.values.get('diagnosis')
		patient_id=request.values.get('pid')
		date = datetime.datetime.now()
		print(type(patient_id))
		# return render_template("home.html")
		query={"hash":int(patient_id)}
		# query={"pid":"2A"}
		print(type(query))
		mydocs=hash_control.find(query)
		print(type(mydocs))
		# return render_template("home.html")

		for x in mydocs:
			x["_id"]=str(x["_id"])
			print x
			# return render_template("home.html")
			table_hash=x["hash"]
			table_pid=x["pid"]
			print x["hash"]
			hashdoc=table_patient.insert({"pid":table_pid,"diagnostic_report":diagnostic_report,"date":date})

			hash1=hash(hashdoc)
			print(hash1)
			hash_control.insert({"pid":table_pid,"hash":hash1})
		
		

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

	elif(action=="newlogin"):	
		return render_template("patient_info.html")

@app.route("/patientlogin",methods=["POST"])
def patientlogin():
	action=request.values.get('action')
	return render_template("patient_view.html")
	# if(action=="signin"):
	# 	name=request.values.get('name')
	# 	pid=request.values.get('pid')
	# 	query={"name":name,"pid":pid}
	# 	mydoc=table_patient.find(query)
	# 	for x in mydoc:

	# 		print x
			# return render_template("patient_view.html")
			# table_name=x["name"]
			# table_email=x["email"]
			# if(name==table_name and email==table_email):
			# 	return render_template("patient_view.html")

@app.route("/viewdata",methods=["POST"])
def insurance_view_record():
	# action=request.values.get('action')
	# if(action=="enter"):
		pid=request.values.get('pid')
		print pid
		unique_pid=request.values.get('unique_pid')
		print unique_pid
		# return render_template("home.html")

		query={"hash":int(unique_pid),"pid":pid}
		newdoc=hash_control.find(query)
		# return render_template("home.html")
		for x in newdoc:
			x["_id"]=str(x["_id"])
			print x
			table_pid=x["pid"]
			table_hash=x["hash"]
			print table_hash
			# return render_template("home.html")
			# if(pid==table_pid and unique_pid==table_hash):
				# print table_hash
				# return render_template("home.html")
			query_new={"pid":pid}
			# patient_doc=[]
			# patient_doc=table_patient.find(query_new)
			patient_doc=list(table_patient.find(query_new))
			print patient_doc
			print type(patient_doc)	
			for y in patient_doc:
				# for y in z:
					# y["_id"]=str(y["_id"])
					# y=json.loads(y)
					# ast.literal_eval(json.dumps(y))
					# print type(y)
					
				
				# return render_template("home.html")
					# table_name=y
				table_name=y['name']
				table_dignostic_report=y['diagnostic_report']
				table_age=y['age']
				table_gender=y['gender']
				table_occup=y['occupation']
				table_email=y['email']
				return render_template("insurance.html",name=table_name,report=table_dignostic_report,age=table_age,gender=table_gender,occupation=table_occup,email=table_email)
					# return render_template("insurance.html",result=patient_doc)
	   	

@app.route("/create_block",methods=["POST"])
def create():
	if request.method == 'POST':
		existing_user=table_patient.find_one({'name': request.form['name']})
	
	if existing_user is None:
		patient_id=request.values.get('pid')
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
		diagnostic_report=request.values.get('report')
		

		hashdoc=table_patient.insert({"pid":patient_id,"name":name,"age":age,"occupation":occupation,"gender":gender,"email":email,"relation":relation,"diagnostic_report":diagnostic_report,"date":date})
		
		
		hash1=hash(hashdoc)
		print(hash1)
		hash_control.insert({"pid":patient_id,"hash":hash1})
		
		
		
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


