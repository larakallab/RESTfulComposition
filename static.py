#!/usr/bin/env python

from flask import Blueprint 
from flask import Flask, json
from flask import request
import requests

from SPARQLWrapper import SPARQLWrapper, JSON
from collections import OrderedDict 
from rdflib import Graph

from ModelingEngine import ModelingEngine
from ValidationEngine import ValidationEngine
from ConversionEngine import ConversionEngine
from ExecutionEngine import ExecutionEngine

static = Blueprint('static', __name__,)

@static.route('/services/description', methods=['GET', 'POST'])
def Descriptions(): 
	if request.method == 'GET':
		sparql = SPARQLWrapper("http://localhost:3030/03Ap08/query")
		sparql.setQuery("""
  					Select ?service ?description ?method ?inputs ?outputs
					{
  						{?service <http://www.w3.org/ns/hydra/core#description> ?description}
						{?service <http://www.w3.org/ns/hydra/core#operation> ?op .
   						?op <http://www.w3.org/ns/hydra/core#method> ?method}
						{?service <http://www.w3.org/ns/hydra/core#operation> ?op .
						?op <http://www.w3.org/ns/hydra/core#method> ?method} 
  
						{SELECT ?service (GROUP_CONCAT(?input;separator="|") AS ?inputs) 
  							WHERE {
  							{?service <http://www.w3.org/ns/hydra/core#operation> ?op .
 							?op <http://www.w3.org/ns/hydra/core#expects> ?expects .
							?expects ?input ?inval}}
							group by ?service }
						{SELECT ?service (GROUP_CONCAT(?output;separator="|") AS ?outputs) 
 							WHERE {
  							{?service <http://www.w3.org/ns/hydra/core#operation> ?op .
							?op <http://www.w3.org/ns/hydra/core#returns> ?returns .
							?returns ?output ?outval}}
							group by ?service }
							}
					""")
		sparql.setReturnFormat(JSON)
		results = sparql.query().convert()
		dumped_data = json.dumps(OrderedDict(results))
		data = json.loads(dumped_data, object_pairs_hook=OrderedDict)
	
		finalData = OrderedDict()
		services = []

		for i in data["results"]["bindings"]:
			service = {}
			service['service']= i["service"]["value"]
			service['description']= i["description"]["value"]
			service['method']= i["method"]["value"]
			service['inputs']= i["inputs"]["value"]
			service['outputs']= i["outputs"]["value"]
			services.append(service)
	
		finalData['services']=services
		return json.dumps(OrderedDict(finalData))
		

	if request.method == 'POST': 
		jsonlddata = request.get_json()
		d1 = json.dumps(OrderedDict(jsonlddata))
		g = Graph()
		g.parse(data=d1, format='json-ld')

		queryString = "INSERT DATA { "+g.serialize(format='nt')+"}" 
		sparql = SPARQLWrapper("http://localhost:3030/03Ap08/update")

		sparql.setQuery(queryString) 
		sparql.method = 'POST'
		sparql.query()		
		return '' 
			

@static.route('/services/composition', methods=["POST"])
def postComposition():
	global composition 
	modeling = ModelingEngine()
	composition = modeling.getComposition()		
	global outputPlaces
	outputPlaces = modeling.JSONtoPNML(composition)
	validation = ValidationEngine()
	valid = validation.validateComposition(outputPlaces, composition)
	if valid == 'True':
		conversion = ConversionEngine()
		global JSONLD
		JSONLD = conversion.convertComposition(composition)
		headers = {'dataType': 'json', 'Content-Type' : 'application/json'}
		requests.post('http://localhost:5000/services/description', headers=headers, data = JSONLD)
	return ''


@static.route('/compositionexec/<compositionId>')
def executeComposition(compositionId):
	variables = request.get_json()
	sparql = SPARQLWrapper("http://localhost:3030/03Ap08")
	sparql.setQuery("""
		Select  ?url ?method ?returns ?inputs ?inputValues where
		{
 		{
    		<http://localhost:5000/"""+compositionId+"""> <http://www.w3.org/ns/hydra/core#Collection> ?c .
		?c <http://www.w3.org/ns/hydra/core#member> ?member.
   		?member <http://www.w3.org/ns/hydra/core#method> ?method .
  		?member <http://schema.org/url> ?url .
  		?member <http://www.w3.org/ns/hydra/core#returns> ?returns .
  		{SELECT ?member (GROUP_CONCAT(?input;separator="|") AS ?inputs) (GROUP_CONCAT(?inputValue;separator="|") AS ?inputValues) 
		WHERE {
		{?member <http://www.w3.org/ns/hydra/core#expects> ?expect.
  		?expect ?input ?inputValue}
		}
		group by ?member }
		}
		}
		""")
	sparql.method = 'GET'
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	dumpedresults = json.dumps(OrderedDict(results))
	jsonresults = json.loads(dumpedresults, object_pairs_hook=OrderedDict)

	workflow = {}
	member = []
	compoDesc= OrderedDict()

	for i in jsonresults["results"]["bindings"]:
		service = {}
		service['url']= i["url"]["value"]
		service['method']= i["method"]["value"]
		service['returns']= i["returns"]["value"]
		expects = []
		if ('|' in i["inputs"]["value"]):
				inputs = str(i["inputs"]["value"])
				arr_inputs = inputs.split("|")
				input_val = str(i["inputValues"]["value"])
				arr_input_val = input_val.split("|")
				for i in range(len(arr_inputs)):
					exp={}
					exp[arr_inputs[i]] = arr_input_val[i]
					expects.append(exp)
				service['expects']= expects
		else:
			exp={}
			exp[i["inputs"]["value"]] = i["inputValues"]["value"]
			expects.append(exp)
		service['expects']= expects
		member.append(service)	
	compoDesc['Workflow']= member
	sparql2 = SPARQLWrapper("http://localhost:3030/03Ap08")
	sparql2.setQuery("""
	Select  ?goal where
		{
    		<http://localhost:5000/"""+compositionId+"""> <http://www.w3.org/ns/hydra/core#Collection> ?coll .
  		?coll <http://schema.org/Text> ?goal
		}
	""")
	sparql2.method = 'GET'
	sparql2.setReturnFormat(JSON)
	results2 = sparql2.query().convert()
	dumpedresults2 = json.dumps(OrderedDict(results2))
	jsonresults2 = json.loads(dumpedresults2, object_pairs_hook=OrderedDict)
	compoDesc['Goal']= jsonresults2["results"]["bindings"][0]["goal"]["value"]
	jsonldexec = json.dumps(OrderedDict(compoDesc))
	
	var_arr=[]
	sparql = SPARQLWrapper("http://localhost:3030/03Ap08")
	sparql.setQuery("""
	SELECT ?input  
	WHERE
	{<http://localhost:5000/"""+compositionId+"""> <http://www.w3.org/ns/hydra/core#operation> ?op .
	?op <http://www.w3.org/ns/hydra/core#expects> ?expects .
	?expects ?input ?inval
	}
	""")
	sparql.method = 'GET'
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	dumpedresults = json.dumps(OrderedDict(results))
	jsonresults = json.loads(dumpedresults)
	print (jsonresults)
	for i in jsonresults["results"]["bindings"]:
		#var = i["input"]["value"].split('#')
		var = i["input"]["value"].rsplit('/', 1)[-1]
		var_arr.append(var[1])
	execution = ExecutionEngine()
	#variables = [["var_initDate", "26-03-2018 12:00:00"], ["var_endDate", "27-03-2018 12:00:00"]]
	execution.executeComposition(jsonldexec, var_arr, variables)
	return ''
	
