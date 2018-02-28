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
		for l in compo["composition"]["services"]:
			dmember= {}
			dmember['@id'] = l['url']
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
