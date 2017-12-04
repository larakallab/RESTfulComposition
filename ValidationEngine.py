#!/usr/bin/env python
 
from flask import Flask, json
from subprocess import call
import subprocess

class ValidationEngine(object):

	def __init__(self):
		pass	

	def validateComposition(self, outputPlaces):
		live = []
		param = "neco-check --formula=\"F (marking(\'Goal\') = [dot])\""
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

