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

missingdata = Blueprint('missingdata', __name__,)

@missingdata.route('', methods=['POST', 'HEAD'])
def missingData():
	parser = reqparse.RequestParser()
	parser.add_argument('data')
	args = parser.parse_args()
	if request.method == 'POST':
		v = '1'
		resp = make_response(jsonify(data_id=v))
		resp.headers['Link'] = 'http://localhost:5000/CorrectMissingData/CorrectMissingData.md'
		return resp
	if request.method == 'HEAD':
		resp = make_response()
		resp.headers['Link'] = 'http://localhost:5000/CorrectMissingData/CorrectMissingData.md'
		return resp

@missingdata.route('/CorrectMissingData.md')
def getDescriptorCorrectMissingData():
	myjson = """
 	{
 	"@context": "http://localhost:5000/context.jsonld",
 	"@id": "http://localhost:5000/CorrectMissingData/CorrectMissingData.md",
 	"@type": "Descriptor",
 	"annotation": "",
 	"operations": [{
 		"method": "POST",
 		"expects": {
 			"externalpredictedtemperature": "h2g:externalpredictedtemperature"
 		},
 		"returns": {
 			"data_id": "h2g:data_id"
 		},
 		"statusCodes": null,
 		"annotation": "http://localhost:5000/h2gontology/missingdata.owl#correctmissingdata"
 	}],
 	"links": [{
 		"supportedOperations": "http-methods:GET",
 		"annotation": "http://localhost:5000/resourcerelation.owl#Iscomplementary",
 		"key": " CorrectMissingData",
 		"value": "http://localhost:5000/service/CorrMissingData"
 	}]
 }
 	"""
 	return myjson
