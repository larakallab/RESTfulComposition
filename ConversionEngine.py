#!/usr/bin/env python
 
from flask import Flask, json
from flask import abort
from collections import OrderedDict
from SPARQLWrapper import SPARQLWrapper, JSON

class ConversionEngine(object):

	def __init__(self):
		pass	


	def convertComposition(self, composition):
		data = json.dumps(composition)
		compo = json.loads(data)
		compoDesc= OrderedDict()
		operation = []
		inputs = []
		outputs = []

		context =  '''
					{"@vocab": "http://www.w3.org/ns/hydra/core#",
					"schema": "http://schema.org/",
					"ifcTC1": "http://www.buildingsmart-tech.org/ifcOWL/IFC2X3_TC1/",
					"ifcFinal": "http://www.buildingsmart-tech.org/ifcOWL/IFC2X3_Final/",
					"h2gBI": "http://hit2gap.eu/h2g/h2gBI/",
					"h2gOcc": "http://hit2gap.eu/h2g/h2gOccupant/",
					"h2gProp": "http://hit2gap.eu/h2g/h2gProperty/",
					"ssn": "https://www.w3.org/TR/vocab-ssn/",
					"qudt": "http://quadt.org/schema/qudt/",
					"siteId": "ifcTC1:globalId_IfcRoot",
					"buildingId": "ifcTC1:globalId_IfcRoot",
					"floorId": "h2gBI:Floor",
					"spaceId": "ifcTC1:globalId_IfcRoot",
					"measureId": "ssn:SOSAResult",
					"systemType": "ifcFinal:IfcEnergyConversionDevice",
					"relationToSystem": "h2gBI:transports",
					"measureType": "h2gProp:PhysicalProperty",
					"initDate": "h2gOcc:startWorktime",
					"endDate": "h2gOcc:endWorktime",
					"frequency": "h2gProp:Frequency",
					"quality": "schema:Float",
					"Workflow": "Collection",
					"services": "Collection",
					"data": "schema:Text",
					"Goal": "schema:Text",
					"id": "schema:identifier",
					"url": "schema:url"}
				'''
		compoDesc['@context'] = json.loads(context)
	
		compoDesc['@id']= "http://www.hit2gap.eu/services/description/automatic_id"
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
				sparql = SPARQLWrapper("http://localhost:3030/CompoServDesModified/query")
				sparql.setQuery("""
  		 				SELECT ?output 
						WHERE
						{<"""+i['url']+"""> <http://www.w3.org/ns/hydra/core#operation> ?op .
						?op <http://www.w3.org/ns/hydra/core#returns> ?returns .
						?returns ?output ?outval}
						""")
				sparql.setReturnFormat(JSON)
				results = sparql.query().convert()
				dumped_data = json.dumps(results)
				data_result = json.loads(dumped_data)
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
			dmember['@id'] = 'S'+str(service_id)
			dmember['url'] = l['url']
			dmember['method'] = l['method']
			dmember['expects'] = l['param']
			dmember['returns'] = l['output']
			member.append(dmember)	

		fmember = {}	
		fmember['Goal'] = compo["composition"]["goal"]
		fmember['member'] = member

		compoDesc['Workflow']= fmember

		jsonld = json.dumps(compoDesc)
		print (jsonld)
		return jsonld		
