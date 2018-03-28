#!/usr/bin/env python
 
from flask import Flask, json
from collections import OrderedDict
from SPARQLWrapper import SPARQLWrapper, JSON
from collections import OrderedDict

class ConversionEngine(object):

	def __init__(self):
		pass	

	def convertComposition(self, composition):
		data = json.dumps(OrderedDict(composition))
		compo = json.loads(data, object_pairs_hook=OrderedDict)
		compoDesc= OrderedDict()
		operation = []
		inputs = []
		outputs = []

		context =  '''
					{
	"@vocab": "http://www.w3.org/ns/hydra/core#",
	"schema": "http://schema.org/",
	"ifcTC1": "http://www.buildingsmart-tech.org/ifcOWL/IFC2X3_TC1/",
	"ifcFinal": "http://www.buildingsmart-tech.org/ifcOWL/IFC2X3_Final/",
	"h2gBI": "http://hit2gap.eu/h2g/h2gBI/",
	"h2gOcc": "http://hit2gap.eu/h2g/h2gOccupant/",
	"h2gProp": "http://hit2gap.eu/h2g/h2gProperty/",
	"ssn": "https://www.w3.org/TR/vocab-ssn/",
	"qudt": "http://quadt.org/schema/qudt/",
	"measureId": "ssn:SOSAResult",
	"timestamp": "schema:DateTime",
	"initDate": "schema:startDate",
	"endDate": "schema:endDate",
	"updatedDate": "schema:DateTime",
	"frequency": "h2gProp:Frequency",
	"unit": "qudt:Unit",
	"quality": "schema:Float",
	"Workflow": "Collection",
	"services": "Collection",
	"data": "schema:Text",
	"Goal": "schema:Text",
	"id": "schema:identifier",
	"url": "schema:url",
	"acronym": "schema:Text",
	"value": "schema:Float",
	"tabCollVal": {
		"@id": "tabCollVal",
		"@container": "@set",
		"@values": [{
				"@type": "quality"
			},
			{
				"@type": "timestamp"
			},
			{
				"@type": "updatedDate"
			},
			{
				"@type": "value"
			}
		]
	},
	"tabValues": {
		"@id": "tabValues",
		"@container": "@set",
		"@values": [{
				"@type": "timestamp"
			},
			{
				"@type": "value"
			}
		]
	},
	"tabValues2": {
		"@id": "tabValues2",
		"@container": "@set",
		"@values": [{
				"@type": "timestamp"
			},
			{
				"@type": "value"
			}
		]
	},
	"tabTimestamp": {
		"@id": "tabTimestamp",
		"@container": "@set",
		"@values": [{
				"@type": "initDate"
			},
			{
				"@type": "endDate"
			}
		]
	}
}
				'''
		compoDesc['@context'] = json.loads(context)
	
		compoDesc['@id']= "http://localhost:3030/27March18/newcomposition10"
		compoDesc['@type']= "composedService"
		compoDesc['description']= compo["composition"]["description"]
		compoDesc['title']= compo["composition"]["title"]

		d = {}
		d['method'] = "GET"

		expects = []
		returns = []
		paramArr = []
		for k in compo["composition"]["variables"]:
			for l in compo["composition"]["services"]:
				for m in (l['param']):
					if ((k == m.values()[0].encode('ascii')) and (k not in paramArr)):
						paramArr.append(k)
						exp={}
						exp[m.values()[0].encode('ascii')] = ""
						expects.append(exp)
		d['expects']=expects
		for i in compo["composition"]["services"]:
			if (i['output']==compo["composition"]["goal"]):
				sparql = SPARQLWrapper("http://localhost:3030/27March18/query")
				sparql.setQuery("""
  		 				SELECT ?output 
						WHERE
						{<"""+i['url']+"""> <http://www.w3.org/ns/hydra/core#operation> ?op .
						?op <http://www.w3.org/ns/hydra/core#returns> ?returns .
						?returns ?output ?outval}
						""")
				sparql.setReturnFormat(JSON)
				results = sparql.query().convert()
				dumped_data = json.dumps(OrderedDict(results))
				data_result = json.loads(dumped_data, object_pairs_hook=OrderedDict)
				for i in data_result["results"]["bindings"]:
					ret={}
					ret[str(i["output"]["value"])]=""
					returns.append(ret)
		d['returns']=returns		
		operation.append(d)
		compoDesc['operation']=operation

		member = []
		service_id=0
		for l in compo["composition"]["services"]:
			service_id = service_id+1
			dmember= {}
			dmember['url'] = l['url']
			dmember['method'] = l['method']
			dmember['expects'] = l['param']
			dmember['returns'] = l['output']
			member.append(dmember)	

		fmember = {}	
		fmember['Goal'] = compo["composition"]["goal"]
		fmember['member'] = member

		compoDesc['Workflow']= fmember

		jsonld = json.dumps(OrderedDict(compoDesc))
		return jsonld		
