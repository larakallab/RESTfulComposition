#!/usr/bin/env python

from flask import Blueprint 
from flask import Flask, url_for, json
from flask import Response
from flask import request
from flask import jsonify, make_response
from flask_restful import reqparse
from subprocess import call

from random import randint

from itertools import cycle
import requests

import snakes.plugins
import snakes.pnml
snakes.plugins.load('gv', 'snakes.nets', 'nets')
from nets import *
import subprocess

static = Blueprint('static', __name__,)

@static.route('/service/composition', methods=["POST"])
def postComposition():
	global composition; 
	composition = request.get_json();
	return 'ok';
	
@static.route('/composition/execute')
def executeComposition():
	print ('in')
	parser = reqparse.RequestParser()
	parser.add_argument('composition_id')
	args = parser.parse_args()
	a = [];
	headers = {'dataType': 'json', 'Content-Type' : 'application/json'}
	data = json.dumps(composition);
	data2 = json.loads(data);
	for item in data2['composition']['services']:
		par="";
		for i in item['param']:
			k = list(i.keys())
			mykey = ''.join(k)
			l = list(i.values())
			mystring = ''.join(l)
			t=0;
			for j in range(len(a)):
				if (mystring in a[j][0]): 
					str = a[j][1].replace(" ", "")
					str2 = str.split("\n",1)[1];
					str3 = str2[:str2.rfind('\n')]
					par = par+","+str3
					par = par[:-1]
					t=1;
			if (t==0):
				par = par+","+"\""+mykey+"\":\""+mystring+"\""
		par = par[1:];
		url = item['url']
		if (item['method']=='GET'):
			y = item['output']
			x = item['output']    
			exec("%s = %s" % (x,2))
			item['output'] = requests.get(url, headers=headers, data = "{"+par+"}").text;
			a.append([y, item['output']])
		if (item['method']=='POST'):
			y = item['output']
			x = item['output']    
			exec("%s = %s" % (x,2))
			item['output'] = requests.post(url, headers=headers, data = "{"+par+"}").text;
			a.append([y, item['output']])
	goal = data2['composition']['goal']
	for j in range(len(a)):
		if (a[j][0] == goal):
			print (a[j][1])
	return "ok"

@static.route('/validate')	
def validateComposition():
	parser = reqparse.RequestParser()
	parser.add_argument('composition_id')
	args = parser.parse_args()
	headers = {'dataType': 'json', 'Content-Type' : 'application/json'}
	net = PetriNet('N')
	a = []
	p = []
	outputPlaces = []
	live = []
	data = json.dumps(composition)
	d = json.loads(data)
	tr_number = len(d['composition']['services'])
	print (tr_number)
	for item in d['composition']['services']:
		name = item['name'] 
		net.add_transition(Transition(name))
		output = item['output'] 
		a.append([name, output])
		for i in item['param']:
			l = list(i.values())
			m = list(i.keys())
			mystring = ''.join(l)
			mykey = ''.join(m)
			t=0
			pp = 0
			for j in range(len(a)):
				if (mystring in a[j][1]):
					p.append([name, mystring])
					for k in range(len(p)):
						if (mystring in p[k][1]):
							pp=pp+1
					if (pp<=1):
						print ('boom')
						net.add_input(a[j][0]+'output', name, Value(dot))
					t=1;
			if (t==0):
				net.add_place(Place(name+""+mykey, [dot], tBlackToken))
				net.add_input(name+""+mykey, name, Value(dot))
			if (pp>1):
				net.add_place(Place(name+""+mykey, [], tBlackToken))
				net.add_input(name+""+mykey, name, Value(dot))
				for l in range(len(a)):
					if (mystring in a[l][1]):
						net.add_output(name+""+mykey, a[l][0], Value(dot))
		if (output == d['composition']['goal']):
			net.add_place(Place('Goal', [], tBlackToken))
			net.add_output('Goal', name, Value(dot))
		if (output != d['composition']['goal']):
			net.add_place(Place(name+'output', [], tBlackToken))
			net.add_output(name+'output', name, Value(dot))
			outputPlaces.append(name+'output')
	
	l = dumps (net)
	
	file = open("composition.pnml","w") 
	file.write (l)
	file.close()	
	print (l)

	param = "neco-check --formula=\"F (marking(\'Goal\') = [dot])\""
	#print "TESTTTTTTTTTTTTTTTTTTTTTTTTTT = ", param
	subprocess.call(['neco-compile', '--pnml', 'composition.pnml', '-lcython'])
	subprocess.call(['neco-explore', '--dump', 'states'])
	subprocess.call(['neco-explore', '--graph', 'map', 'graph'])
	subprocess.call(param, shell=True, stdout=subprocess.PIPE)
	file_out = open("ReachabilityResults.txt","w")
	subprocess.call(['neco-spot', 'neco_formula'], stdout=file_out)
	line = subprocess.check_output(['tail', '-1', 'graph'])
	line1 = subprocess.check_output(['tail', '-1', 'graph'])
	fp = open("ReachabilityResults.txt")
	var=""
	for i, line1 in enumerate(fp):
		if i == 4:
			var = line1.partition(' ')[0]
	if (line.partition(' ')[0] == var):
		print ("Final State is Reachable")
	else:
		print ("Final State is Not Reachable")

	for i in outputPlaces:
		subprocess.call(['neco-compile', '--pnml', 'composition.pnml', '-lcython'])
		placeName = "neco-check --formula=\"F (marking(\'"+i+"\') = [dot])\""
		subprocess.call(param, shell=True, stdout=subprocess.PIPE)
		file_outL = open("livenessResults.txt","w")
		subprocess.call(['neco-spot', 'neco_formula'], stdout=file_outL)
		fpL = open("ReachabilityResults.txt")
		var2=""
		for i, line2 in enumerate(fpL):
			if i == 9:
				var2 = line2.partition(' ')[0]
				if var2 == "no":
					live.append('live')
	
	notLive=False;
	for j in live:
		if (j != 'live'):
			notLive=True;
	if (notLive == False):
		print ("All transitions are live")			
	return "ok"
