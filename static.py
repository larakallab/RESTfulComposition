#!/usr/bin/env python

from flask import Blueprint 
from flask import Flask, json
from flask import request
import requests

from flask_restful import reqparse
from SPARQLWrapper import SPARQLWrapper, JSON
from collections import OrderedDict
import rdflib  
from rdflib_sparql.processor import processUpdate  

from ModelingEngine import ModelingEngine
from ValidationEngine import ValidationEngine
from ConversionEngine import ConversionEngine
from ExecutionEngine import ExecutionEngine

static = Blueprint('static', __name__,)

@static.route('/services/description', methods=['GET', 'POST'])
def Descriptions(): 
	if request.method == 'GET':
		sparql = SPARQLWrapper("http://localhost:3030/CompoServDesModified/query")
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
		dumped_data = json.dumps(results)
		data = json.loads(dumped_data)
	
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
		return json.dumps(finalData)
		

	if request.method == 'POST': 
		jsonlddata = request.get_json()
		d1 = json.dumps(jsonlddata)
		g=rdflib.Graph()  
		g.parse('http://localhost:3030/CompoServDesModified/data', format="turtle")  
		g.parse(data = d1, format="json-ld") 
		
		qres = g.query(
    		"""
		Select ?member ?method ?url ?returns ?inputs ?inputValues ?goal where
		{
		<http://www.hit2gap.eu/services/description/automatic_id> <http://www.w3.org/ns/hydra/core#Collection> ?coll .
		?coll <http://schema.org/Text> ?goal.
		?coll <http://www.w3.org/ns/hydra/core#member> ?member.
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
		""")
		workflow = {}
		member = []
		compoDesc= OrderedDict()
		for row in qres:
			service = {}
			service['url']= row.url
			service['method']= row.method
			service['returns']= row.returns
			expects = []
			exp={}
			if ('|' in row.inputs):
				inputs = str(row.inputs)
				arr_inputs = inputs.split("|")
				input_val = str(row.inputValues)
				arr_input_val = input_val.split("|")
				for i in range(len(arr_inputs)):
					exp[arr_inputs[i]] = arr_input_val[i]
				expects.append(exp)
				service['expects']= expects
			else:
				exp[row.inputs] = row.inputValues
				expects.append(exp)
			service['expects']= expects
			member.append(service)	
		compoDesc['Workflow']= member
		compoDesc['Goal']= row.goal
		jsonld = json.dumps(compoDesc)
		print (jsonld)
		#execution = ExecutionEngine()
		#execution.executeComposition(jsonld)						
		return '' 
			

@static.route('/services/composition', methods=["POST"])
def postComposition():
	global composition 
	modeling = ModelingEngine()
	composition = modeling.getComposition()		
	global outputPlaces
	outputPlaces = modeling.JSONtoPNML(composition)
	print (outputPlaces)
	validation = ValidationEngine()
	validation.validateComposition(outputPlaces, composition)
	conversion = ConversionEngine()
	global JSONLD
	JSONLD = conversion.convertComposition(composition)
	headers = {'dataType': 'json', 'Content-Type' : 'application/json'}
	requests.post('http://localhost:5000/services/description', headers=headers, data = JSONLD)
	return ''


@static.route('/compositionexec')
def executeComposition():
	'''
	g=rdflib.Graph()  
	g.parse('http://localhost:3030/CompoServDesModified/data', format="turtle") 
	qres = g.query(
    	"""
	Select ?member ?method ?url ?return ?inputs ?inputValues where
	{
	<http://www.hit2gap.eu/services/description/automatic_id> <http://www.w3.org/ns/hydra/core#Collection> ?coll .
	?coll <http://www.w3.org/ns/hydra/core#member> ?member.
   	?member <http://www.w3.org/ns/hydra/core#method> ?method .
  	?member <http://schema.org/url> ?url .
  	?member <http://www.w3.org/ns/hydra/core#returns> ?return .
  
  	{SELECT ?member (GROUP_CONCAT(?input;separator="|") AS ?inputs) (GROUP_CONCAT(?inputValue;separator="|") AS ?inputValues) 
	WHERE {
	{?member <http://www.w3.org/ns/hydra/core#expects> ?expect.
  	?expect ?input ?inputValue}
	}
	group by ?member }
	}
	""")
	print ('passed')
	for row in qres:
    		print(row)
	print ('finish')
	'''
	'''
	There will be a call to the core platform API according to composition id in order to retrieve the composition description
	For the moment we are using the composition description presented in a file on the server 'CompositionDescription.jsonld'
	'''
	#compositionDesc = open("CompositionDescription.jsonld")
	data = """
{
	"Goal": "E",
	"Workflow": [{
		"expects": [{
			"http://schema.org/Text": "C"
		}],
		"method": "GET",
		"returns": "D",
		"url": "http://localhost:5000/conversion"
	}, {
		"expects": [{
			"http://hit2gap.eu/h2g/h2gOccupant/endWorktime": "endDate",
			"http://hit2gap.eu/h2g/h2gOccupant/startWorktime": "initDate",
			"http://hit2gap.eu/h2g/h2gProperty/PhysicalProperty": "internal temperature"
		}],
		"method": "GET",
		"returns": "A",
		"url": "http://localhost:5000/getmeasure"
	}, {
		"expects": [{
			"http://schema.org/Text": "A"
		}],
		"method": "GET",
		"returns": "B",
		"url": "http://localhost:5000/conversion"
	}, {
		"expects": [{
			"http://schema.org/Text": "B"
		}],
		"method": "GET",
		"returns": "E",
		"url": "http://localhost:5000/alignement"
	}, {
		"expects": [{
			"http://hit2gap.eu/h2g/h2gOccupant/endWorktime": "endDate",
			"http://hit2gap.eu/h2g/h2gOccupant/startWorktime": "initDate",
			"http://hit2gap.eu/h2g/h2gProperty/PhysicalProperty": "external temperature"
		}],
		"method": "GET",
		"returns": "C",
		"url": "http://localhost:5000/getmeasure"
	}]
}
"""
	execution = ExecutionEngine()
	execution.executeComposition(data)
	return ''
	
