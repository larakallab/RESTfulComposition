#!/usr/bin/env python

from flask import Blueprint 
from flask import Flask, url_for, json
from flask import Response
from flask import request
from flask import jsonify, make_response
from flask_restful import reqparse

from random import randint

from itertools import cycle
import requests

import snakes.plugins
import snakes.pnml
snakes.plugins.load('gv', 'snakes.nets', 'nets')
from nets import *

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
					t=1;
			if (t==0):
				par = par+","+"\""+mykey+"\":\""+mystring+"\""
		par = par[1:];
		print (par)
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
	n = PetriNet('N')
	a = [];
	p = [];
	headers = {'dataType': 'json', 'Content-Type' : 'application/json'}
	data = json.dumps(composition);
	d = json.loads(data);
	for item in d['composition']['services']:
		print ('service')
		name = item['name'] 
		n.add_transition(Transition(name))
		output = item['output'] 
		a.append([name, output])
		for i in item['param']:
			l = list(i.values())
			m = list(i.keys())
			mystring = ''.join(l)
			mykey = ''.join(m)
			t=0;
			pp = 0;
			for j in range(len(a)):
				if (mystring in a[j][1]):
					p.append([name, mystring])
					for k in range(len(p)):
						if (mystring in p[k][1]):
							pp=pp+1
					if (pp<=1):
						print ('boom')
						n.add_input(a[j][0]+'-output', name, Value(dot))
					t=1;
			if (t==0):
				print ('ok0')
				n.add_place(Place(name+"-"+mykey, [dot]))
				n.add_input(name+"-"+mykey, name, Value(dot))
			if (pp>1):
				print ('ok1')
				n.add_place(Place(name+"-"+mykey))
				print ('ok2')
				n.add_input(name+"-"+mykey, name, Value(dot))
				print ('ok3')
				for l in range(len(a)):
					if (mystring in a[l][1]):
						print ('ok4')
						n.add_output(name+"-"+mykey, a[l][0], Value(dot))
		print ('ok5')
		n.add_place(Place(name+'-output'))
		n.add_output(name+'-output', name, Value(dot))
		print ('ok6')
	for engine in ('neato', 'dot', 'circo', 'twopi', 'fdp') :
		n.draw(',compo-%s.png' % engine, engine=engine)
	s = StateGraph(n)
	s.build()
	s.draw(',compo-graph.png')
	l = dumps (n)
	
	file = open("composition.pnml","w") 
	file.write (l)
	file.close()	
	print (l)
	return "ok"