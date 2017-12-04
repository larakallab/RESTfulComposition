#!/usr/bin/env python
 
from flask import Flask
from flask import request
import json
import snakes.plugins
import snakes.pnml
snakes.plugins.load('gv', 'snakes.nets', 'nets')
from nets import *

class ModelingEngine(object):

	def __init__(self):
		pass	

	def getComposition(self):
		return request.get_json()
		
	def JSONtoPNML(self, composition):
		net = PetriNet('N')
		outArray = []
		p = []
		transitionName = []
		outputPlaces = []
		data = json.dumps(composition)
		print (data)
		d = json.loads(data)
		print (d)
		tr_number = len(d['composition']['services'])
		print (tr_number)
		for item in d['composition']['services']:
			transitionName.append(item['name'])
			numberName = 0
			for n in range(len(transitionName)):
				if ((transitionName[n] == item['name']) and (n != len(transitionName))):
					numberName = numberName + 1 
					name = item['name']+str(numberName)
			numberName = 0
			net.add_transition(Transition(name))
			output = item['output'] 
			outArray.append([name, output])
			for i in item['param']:
				l = list(i.values())
				m = list(i.keys())
				mystring = ''.join(l)
				mykey = ''.join(m)
				t=0
				pp = 0
				for j in range(len(outArray)):
					if (mystring in outArray[j][1]):
						p.append([name, mystring])
						for k in range(len(p)):
							if (mystring in p[k][1]):
								pp=pp+1
						if (pp<=1):
							net.add_input(outArray[j][0]+'output', name, Value(dot))
						t=1;
				if (t==0):
					net.add_place(Place(name+""+mykey, [dot], tBlackToken))
					net.add_input(name+""+mykey, name, Value(dot))
				if (pp>1):
					net.add_place(Place(name+""+mykey, [], tBlackToken))
					net.add_input(name+""+mykey, name, Value(dot))
					for l in range(len(outArray)):
						if (mystring in outArray[l][1]):
							net.add_output(name+""+mykey, outArray[l][0], Value(dot))
			if (output == d['composition']['goal']):
				net.add_place(Place('Goal', [], tBlackToken))
				net.add_output('Goal', name, Value(dot))
			if (output != d['composition']['goal']):
				net.add_place(Place(name+'output', [], tBlackToken))
				net.add_output(name+'output', name, Value(dot))
				outputPlaces.append(name+'output')
	
		pnmlFile = dumps(net)
		file = open("composition.pnml","w") 
		file.write (pnmlFile)
		file.close()	
		print (pnmlFile)
		return outputPlaces
