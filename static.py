#!/usr/bin/env python

from flask import Blueprint 
from flask import Flask, json
from flask import request

from flask_restful import reqparse
from SPARQLWrapper import SPARQLWrapper, JSON
from collections import OrderedDict

from ModelingEngine import ModelingEngine
from ValidationEngine import ValidationEngine
from ConversionEngine import ConversionEngine
from ExecutionEngine import ExecutionEngine

static = Blueprint('static', __name__,)

@static.route('/services/description', methods=["GET"])
def getDescriptions():
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

@static.route('/services/composition', methods=["POST"])
def postComposition():
	global composition; 
	modeling = ModelingEngine()
	composition = modeling.getComposition()		
	global outputPlaces;
	outputPlaces = modeling.JSONtoPNML(composition)
	print (outputPlaces)
	validation = ValidationEngine()
	validation.validateComposition(outputPlaces, composition)
	conversion = ConversionEngine()
	conversion.convertComposition(composition)
	return ''

@static.route('/composition/<compositionid>')
def executeComposition(compositionid):
	'''
	There will be a call to the core platform API according to composition id in order to retrieve the composition description
	For the moment we are using the composition description presented in a file on the server 'CompositionDescription.jsonld'
	'''
	compositionDesc = open("CompositionDescription.jsonld")
	execution = ExecutionEngine()
	execution.executeComposition(compositionDesc)
	return ''
	
