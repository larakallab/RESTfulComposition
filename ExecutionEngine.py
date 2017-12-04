#!/usr/bin/env python
 
from flask import Flask, json
from subprocess import call
import subprocess
import requests

class ExecutionEngine(object):

	def __init__(self):
		pass	

	def executeComposition(self, composition):
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
		return ''

