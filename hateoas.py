#!/usr/bin/env python

from flask import Blueprint
from flask import Flask, url_for, json
from flask import Response
from flask import request
from flask import jsonify, make_response
from flask_restful import reqparse

from random import randint

from itertools import cycle
import requests

import snakes.plugins
import snakes.pnml
snakes.plugins.load('gv', 'snakes.nets', 'nets')
from nets import *

hateoas = Blueprint('hateoas', __name__,)
	
@hateoas.route('/service/hateoascomposition', methods=["POST"])
def postHATEOASComposition():
	global hateoascomposition; 
	hateoascomposition = request.get_json();
	bfs();
	return 'ok';
	
def bfs():
	headers = {'dataType': 'json', 'Content-Type' : 'application/json'}
	data = json.dumps(hateoascomposition);
	d = json.loads(data);
	result = [];
	visited = []
	covered_functions = []
	concepts_array = [];
	nextlink_array = [];
	
	for item in d['functionnalities']:
		concepts_array.append(item);
		
	in_value = 0
	currentlink = d['url'];
	length = len(concepts_array)
	while (length > 0):
		if (in_value==0):
			if (currentlink not in visited):
				visited.append(currentlink)
				resp = requests.head(currentlink)
				descriptor = requests.get(resp.headers['Link'], headers=headers).text
				js = json.loads(descriptor)
				for k in js['operations']:
					for j in range(len(concepts_array)):
						if (concepts_array[j] in k['annotation']) and (concepts_array[j] not in covered_functions):
							result.append([concepts_array[j], currentlink])
							covered_functions.append(concepts_array[j])
				for l in js['links']:
					in_value = 1
					if "Iscomplementary" in l['annotation']:
						nextlink_array.append(l['value']);
		else:
			for o in range(len(nextlink_array)):
				currentlink = nextlink_array[o];
				if (currentlink not in visited):
					visited.append(currentlink)
					resp = requests.head(currentlink)
					descriptor = requests.get(resp.headers['Link'], headers=headers).text
					js = json.loads(descriptor)
					for k in js['operations']:
						for j in range(len(concepts_array)):
							if (concepts_array[j] in k['annotation']) and (concepts_array[j] not in covered_functions):
								result.append([concepts_array[j], currentlink])
								covered_functions.append(concepts_array[j])
					for l in js['links']:
						in_value = 1
						if "Iscomplementary" in l['annotation']:
							nextlink_array.append(l['value']);
				
		length=length-1;
	print (result)
