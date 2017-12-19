#!/usr/bin/env python
 
from flask import Flask, json
from flask import abort
from subprocess import call
import subprocess

class ValidationEngine(object):

	def __init__(self):
		pass	

	def validateComposition(self, composition, outputPlaces):
		Reachable = ""
		Liveness = ""
		singleGoal = ""
		Report = ""
		live = []
		
		paramReach = "neco-check --formula=\"F (marking(\'Goal\') = [dot])\""
		subprocess.call(['neco-compile', '--pnml', 'composition.pnml', '-lcython'])
		subprocess.call(['neco-explore', '--dump', 'states'])
		subprocess.call(['neco-explore', '--graph', 'map', 'graph'])
		subprocess.call(paramReach, shell=True, stdout=subprocess.PIPE)
		subprocess.call(['neco-spot', 'neco_formula'])
		fl = open("states")
		notReach=False;
		for i, l in enumerate(fl):
			if "'Goal' : [dot]" in l:
				notReach=True

		if (notReach==True):
			Reachable = "True"
		else:
			Reachable = "False"
		
		for i in outputPlaces:
			subprocess.call(['neco-compile', '--pnml', 'composition.pnml', '-lcython'])
			paramLive = "neco-check --formula=\"F (marking(\'"+i+"\') = [dot])\""
			subprocess.call(paramLive, shell=True, stdout=subprocess.PIPE)
			file_outL = open("Liveness.txt", "w")
			subprocess.call(['neco-spot', 'neco_formula'], stdout=file_outL)
			fp = open("Liveness.txt")
			var2=""
			for i, l in enumerate(fp):
				if i == 9:
					var2 = l.partition(' ')[0]
					if var2 == "no":
						live.append('live')
		notLive=False;
		for j in live:
			if (j != 'live'):
				notLive=True;
		
		if (notLive==True):
			Liveness = "False"
		else:
			Liveness = "True"
				
		if (Reachable == "True" and Liveness == "True"):
			Report=""
		elif (Reachable == "True" and Liveness == "False"):
			Report="Not all transitions are well linked to each other"
		elif (Reachable == "False" and Liveness == "True"):
			Report="Final state is not reachable"
		else:
			Report="Final state is not reachable \n Not all transitions are well linked to each other"
		if Report=="":
			print ("the composition is verified")	
			return '1'				
		else:
			abort(400, Report)
	
		
	
					
		

