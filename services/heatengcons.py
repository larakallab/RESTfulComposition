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

heatengcons = Blueprint('heatengcons', __name__,)

def gen_series(n, min_val, max_val):
 	x = []
 	for i in range(0, n):
 		x.append(randint(min_val, max_val))
 	return x

@heatengcons.route('', methods=['HEAD', 'GET'])
def getPredHeatEngCons():
	parser = reqparse.RequestParser()
	parser.add_argument('data_id')
	args = parser.parse_args()
	if request.method == 'GET':
		v = gen_series(10, 2500, 3007)
		resp = make_response(jsonify(data_id=v))
		resp.headers['Link'] = 'http://localhost:5000/EnergyHeatConsumption/EnergyHeatConsumption.md'
		return resp
	if request.method == 'HEAD':
		resp = make_response()
		resp.headers['Link'] = 'http://localhost:5000/EnergyHeatConsumption/EnergyHeatConsumption.md'
		return resp

@heatengcons.route('/EnergyHeatConsumption.md')
def getDescriptorEnergyHeatConsumption():
	myjson = """
 	{
 	"@context": "http://localhost:5000/context.jsonld",
 	"@id": "http://localhost:5000/EnergyHeatConsumption/EnergyHeatConsumption.md",
 	"@type": "Descriptor",
 	"annotation": "",
 	"operations": [{
 		"method": "GET",
 		"expects": {
 			"data_id": "h2g:data_id"
 		},
 		"returns": {
 			"predictedtemperature": "h2g:predictedtemperature"
 		},
 		"statusCodes": "",
 		"annotation": "http://localhost:5000/h2gontology/energyheatcons.owl#getpredictenergyheat"
 	}],
 	"links": [{
 		"supportedOperations": "",
 		"annotation": "",
 		"key": "",
 		"value": ""
 	}]
 }
 	"""
 	return myjson
