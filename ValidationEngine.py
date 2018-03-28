#!/usr/bin/env python
 
from flask import Flask, json
from flask import abort
from subprocess import call
import subprocess
from SPARQLWrapper import SPARQLWrapper, JSON

class ValidationEngine(object):

	def __init__(self):
		pass	

	def validateComposition(self, outputPlaces, composition):
		Report=""
		Valid = 'True'
		Reachable = self.reachability()
		Liveness = self.liveness(outputPlaces)	
		Interoperability = self.interoperability(composition)	
		if (Reachable == "False"):
			Report= Report+"Final state is not reachable"
		if (Liveness == "False"):
			Report= Report+"\nNot all services are properly linked"
		if (Interoperability == "False"):
			Report= Report+"\nSome services cannot be linked"
		if Report=="":
			print ("Service composition is verified")	
			return Valid				
		else:
			print (Report)
			return Report
	
		
	def reachability(self):
		Reachable = ""
		paramReach = "neco-check --formula=\"F (marking(\'Goal\') = [dot])\""
		subprocess.call(['neco-compile', '--pnml', 'composition.pnml', '-lcython'])
		subprocess.call(['neco-explore', '--dump', 'states'])
		subprocess.call(['neco-explore', '--graph', 'map', 'graph'])
		subprocess.call(paramReach, shell=True, stdout=subprocess.PIPE)
		subprocess.call(['neco-spot', 'neco_formula'])
		fl = open("states")
		notReach = False
		for i, l in enumerate(fl):
			if "'Goal' : [dot]" in l:
				notReach=True
		if (notReach==True):
			Reachable = "True"
		else:
			Reachable = "False"
		return Reachable


	def liveness(self, outputPlaces):
		Liveness = ""
		live = []
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
					else:
						live.append('notlive')
		notLive=False;
		for j in live:
			if (j == 'notlive'):
				notLive=True;
		if (notLive==True):
			Liveness = "False"
		else:
			Liveness = "True"	
		return Liveness

	def interoperability(self, composition):
		Interoperability = 'True'
		sparql = SPARQLWrapper("http://localhost:3030/27March18/query")		
		a = [];
		validation_arr = [];
		validation_report = [];
		data = json.dumps(composition);
		data2 = json.loads(data);
		for item in data2['composition']['services']:
			a.append([item['url'], item['output']])
		for item in data2['composition']['services']:
			for i in item['param']:
				k = list(i.keys())
				mykey = ''.join(k)
				l = list(i.values())
				mystring = ''.join(l)
				for j in range(len(a)):
					if ((mystring == a[j][1]) and (item['url'] != a[j][0])):
						validmatch = 'True' 
						in_arr = [];	
						out_arr = [];	
						sparql.setQuery("""
  						PREFIX h2g: <http://www.hit2gap.eu/hit2gap_onto/>
						PREFIX schema: <http://schema.org/> 
						SELECT ?input  
						WHERE
						{
  						<"""+item['url']+"""> <http://www.w3.org/ns/hydra/core#operation> ?op .
  						?op <http://www.w3.org/ns/hydra/core#expects> ?expects .
    						?expects ?input ?inval
						}
						""")
						sparql.setReturnFormat(JSON)
						input_results = sparql.query().convert()
						data_in = json.dumps(input_results)
						data_input = json.loads(data_in)
						for i in data_input["results"]["bindings"]:
							in_arr.append(str(i["input"]["value"]))
						sparql.setQuery("""
  						PREFIX h2g: <http://www.hit2gap.eu/hit2gap_onto/>
						PREFIX schema: <http://schema.org/> 

						SELECT ?output 
						WHERE
						{
 						<"""+a[j][0]+"""> <http://www.w3.org/ns/hydra/core#operation> ?op .
  						?op <http://www.w3.org/ns/hydra/core#returns> ?returns .
						?returns ?output ?outval
						}
						""")
						sparql.setReturnFormat(JSON)
						output_results = sparql.query().convert()
						data_out = json.dumps(output_results)
						data_output = json.loads(data_out)
						for i in data_output["results"]["bindings"]:
							out_arr.append(str(i["output"]["value"]))
						if ((('http://www.w3.org/ns/hydra/core#tabCollVal' in out_arr) and ('http://www.w3.org/ns/hydra/core#tabValues' in in_arr)) or (('http://www.w3.org/ns/hydra/core#tabValues' in out_arr) and ('http://www.w3.org/ns/hydra/core#tabValues' in in_arr))):
							validmatch = 'True'
						else:				
							validmatch = 'False'
						validation_arr.append([validmatch, a[j][0], item['url']])
		for i in range(len(validation_arr)):
			#if (validation_arr[i][0] == 'True'):
				#print(validation_arr[i][1]+" and "+validation_arr[i][2]+" can be linked.")
			if (validation_arr[i][0] == 'False'):
				Interoperability = 'False'
				#print(validation_arr[i][1]+" and "+validation_arr[i][2]+" cannot be linked.")
		return Interoperability
		

		

