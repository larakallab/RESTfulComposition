#!/usr/bin/env python
 
from flask import Flask
from flask import request
from flask import abort
import json
import snakes.plugins
import snakes.pnml
snakes.plugins.load('gv', 'snakes.nets', 'nets')
from nets import *

class ModelingEngine(object):

	def __init__(self):
		pass	

	def getComposition(self):
		try:
			composition = request.get_json()
		except:
         		abort(400, "The syntax of the JSON model is wrong. Possible mistakes: \n  Errors in the brackets|braces|commas|quotes \n Duplicated keys")
		try:	
			var = composition['composition']['goal']
		except:
			abort(400, "Please specify a 'goal' for the composition")
		return composition
		
	
	def JSONtoPNML(self, composition):
		net = PetriNet('N')
		outArray = []
		p = []
		transitionName = []
		outputPlaces = []
		data = json.dumps(composition)
		d = json.loads(data)
		tr_number = len(d['composition']['services'])
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
				for j in range(len(outArray)):
					if (mystring in outArray[j][1]):
						net.add_input(outArray[j][0]+'output', name, Value(dot))
						t=1;
				if (t==0 and mykey!= 'data'):
					net.add_place(Place(name+""+mykey, [dot], tBlackToken))
					net.add_input(name+""+mykey, name, Value(dot))
				if (t==0 and mykey== 'data'):
					net.add_place(Place(name+""+mykey, [], tBlackToken))
					net.add_input(name+""+mykey, name, Value(dot))
			if (output == d['composition']['goal']):
				net.add_place(Place('Goal', [], tBlackToken))
				net.add_output('Goal', name, Value(dot))
				outputPlaces.append('Goal')
			if (output != d['composition']['goal']):
				net.add_place(Place(name+'output', [], tBlackToken))
				net.add_output(name+'output', name, Value(dot))
				outputPlaces.append(name+'output')
		pnmlFile = dumps(net)
		file = open("composition.pnml","w") 
		file.write (pnmlFile)
		file.close()	
		return outputPlaces
