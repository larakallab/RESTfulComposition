#!/usr/bin/env python
 
from flask import Flask, json
import requests
from collections import OrderedDict
import numpy as np
from SPARQLWrapper import SPARQLWrapper, JSON 

class ExecutionEngine(object):

	def __init__(self):
		pass	

	def executeComposition(self, compositionDesc, var_arr, variables):
		a = [];
		List = [];
		headers = {'dataType': 'json', 'Content-Type' : 'application/json'}
		datacompositionDesc = json.loads(compositionDesc, object_pairs_hook=OrderedDict)
		for item in datacompositionDesc['Workflow']:
			dataIncr = [] # pour ne pas avoir des duplications de la variable data 
			par="";
			for i in item['expects']:
				k = list(i.keys())
				mykey = ''.join(k)							
				l = list(i.values())
				mystring = ''.join(l)
		
				for r in range(len(var_arr)):
					if mystring == var_arr[r]:
						for v in variables:
							if v == var_arr[r]:
								mystring = variables[i]
				if 'Text' in mykey:
					mykey = 'data'
					dataIncr.append([mykey, mystring])
				par = par+","+"\""+mykey+"\":\""+mystring+"\""
			par = par[1:]
			
			if (sum(x.count('data') for x in dataIncr)) > 1:
				parFinal="";
				j = 1
				partest = par.split(",")
				for i in partest:
					if "data" in i:
						i = i.replace("data","data"+str(j))
					j = j+1
					parFinal = parFinal+","+i
				parFinal = parFinal[:-1]
				parFinal = parFinal[1:]
				par = parFinal


			url = item['url']
			returns = item['returns']
			List.append([par, url, returns])
		List2 = []
		index = []
		totalService = 0
		for i in range(len(List)):
			if "data" not in List[i][0]:
				result = requests.get(List[i][1], headers=headers, data = "{"+List[i][0]+"}").text
				totalService = totalService + 1
				a.append([List[i][2], result])
				index.append(i)
		List2 = np.delete(List, index, 0)	
		while totalService <= len(List)-1:
			index2 = []
			for i in range(len(List2)):
				final_param =""
				parameter = str(List2[i][0])
				total_count = parameter.count("data")
				count_data = 0 
				param = parameter.split(',')
				for k in range(len(param)):
					param2 = param[k].rsplit(':', 1)
					if "data" in param2[0]:
						for j in range(len(a)):
							if a[j][0] == param2[1].replace('"', ''):
								count_data = count_data + 1
								var = param2[0]+":"+a[j][1].split(':')[1].replace('}', '')
								final_param = final_param+","+var
					else:
						splitparam2 = str(param2).split(',')
						final_param = final_param+","+str(param2[0])+":"+str(param2[1])
				if final_param.startswith(","):
					final_param = final_param[1:]
				if total_count == count_data:
					result = requests.get(List2[i][1], headers=headers, data = "{"+final_param+"}").text;
					totalService = totalService + 1
					a.append([List2[i][2], result])
					index2.append(i)
			List2 = np.delete(List2, index2, 0)
		goal = datacompositionDesc['Goal']
		for j in range(len(a)):
			if (a[j][0] == goal):
				print (a[j][1])
		return ''


