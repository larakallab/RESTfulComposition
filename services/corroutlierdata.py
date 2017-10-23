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

corroutlierdata = Blueprint('corroutlierdata', __name__,)

@corroutlierdata.route('', methods=['HEAD', 'GET'])
def getcorrOutlierData():
	parser = reqparse.RequestParser()
	parser.add_argument('data_id')
	args = parser.parse_args()
	if request.method == 'GET':
		v = '30, 32, 34, 34, 34, 35, 32, 31, 33, 33'
		resp = make_response(jsonify(data_id=v))
		resp.headers['Link'] = 'http://localhost:5000/GetCorrectedOutliersData/GetCorrectedOutliersData.md'
		return resp
	if request.method == 'HEAD':
		resp = make_response()
		resp.headers['Link'] = 'http://localhost:5000/GetCorrectedOutliersData/GetCorrectedOutliersData.md'
		return resp

@corroutlierdata.route('/GetCorrectedOutliersData.md')	
def getDescriptorGetCorrectedOutliersData():
	myjson = """
	{
	"@context": "http://localhost:5000/context.jsonld",
	"@id": "http://localhost:5000/GetCorrectedOutliersData/GetCorrectedOutliersData.md",
	"@type": "Descriptor",
	"annotation": "",
	"operations": [{
		"method": "GET",
		"expects": {
			"data_id": "h2g:data_id"
		},
		"returns": {
			"correctedoutliersdata": "h2g: correctedoutliersdata"
		},
		"statusCodes": null,
		"annotation": "http://localhost:5000/h2gontology/corroutliersdata.owl#getcorrectoutliersdata"
	}],
	"links": [{
		"supportedOperations": "http-methods:POST",
		"annotation": "http://localhost:5000/resourcerelation.owl#Iscomplementary",
		"key": "EnergyHeatPrediction",
		"value": "http://localhost:5000/service/PredHeatEngCons"
	}]
}
	"""
	return myjson
