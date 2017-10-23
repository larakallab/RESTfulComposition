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

predintemperature = Blueprint('predintemperature', __name__,)

def gen_series(n, min_val, max_val):
	x = []
	for i in range(0, n):
		x.append(randint(min_val, max_val))
	return x

@predintemperature.route('', methods=['GET', 'HEAD'])
def getPredInTemperature():
	parser = reqparse.RequestParser()
	parser.add_argument('startdate')
	parser.add_argument('enddate')
	args = parser.parse_args()
	if request.method == 'GET':
		v = gen_series(10, 18, 24)
		resp = make_response(jsonify(data=v))
		resp.headers['Link'] = 'http://localhost:5000/CollectPredIntTemp/CollectPredIntTemp.md'
		return resp
	if request.method == 'HEAD':
		resp = make_response()
		resp.headers['Link'] = 'http://localhost:5000/CollectPredIntTemp/CollectPredIntTemp.md'
		return resp


@predintemperature.route('/CollectPredIntTemp.md')
def getDescriptorCollectPredIntTemp():
	myjson = """
		{
	"@context": "http://localhost:5000/context.jsonld",
	"@id": "http://localhost:5000/CollectPredIntTemp/CollectPredIntTemp.md",
	"@type": "Descriptor",
	"annotation": "",
	"operations": [{
		"method": "GET",
		"expects": {
			"startdate": "h2g:startdate",
			"enddate": "h2g:enddate"
		},
		"returns": {
			"internalpredictedtemperature": "h2g:internalpredictedtemperature"
		},
		"statusCodes": null,
		"annotation": "http://localhost:5000/h2gontology/predinttemp.owl#getpredictedinternaltemperature"
	}],
	"links": [{
			"supportedOperations": "http-methods:POST",
			"annotation": "http://localhost:5000/resourcerelation.owl#Iscomplementary",
			"key": "EnergyHeatPrediction",
			"value": "http://localhost:5000/service/PredHeatEngCons"
		},
		{
			"supportedOperations": "http-methods:GET",
			"annotation": "http://localhost:5000/resourcerelation.owl#Iscomplementary",
			"key": "getpredictedexternaltemperature",
			"value": "http://localhost:5000/service/PredOutTemperature"
		}
	]
}
		"""
	return myjson
	
