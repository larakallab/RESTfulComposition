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

corrmissingdata = Blueprint('corrmissingdata', __name__,)

@corrmissingdata.route('', methods=['HEAD', 'GET'])
def getcorrMissingData():
	parser = reqparse.RequestParser()
	parser.add_argument('data_id')
	args = parser.parse_args()
	if request.method == 'GET':
		v = '30, 32, 34, 34, 34, 35, 51, 31, 33, 45'
		resp = make_response(jsonify(data=v))
		resp.headers['Link'] = 'http://localhost:5000/GetCorrectedMissingData/GetCorrectedMissingData.md'
		return resp
	if request.method == 'HEAD':
		resp = make_response()
		resp.headers['Link'] = 'http://localhost:5000/GetCorrectedMissingData/GetCorrectedMissingData.md'
		return resp

@corrmissingdata.route('/GetCorrectedMissingData.md')	
def getDescriptorGetCorrectedMissingData():
	return '{"@context": "http://localhost:5000/context.jsonld","@id": "http://localhost:5000/GetCorrectedMissingData/GetCorrectedMissingData.md","@type": "Descriptor","annotation": "","operations": [{"method": "GET","expects": {"data_id": "h2g:data_id"},"returns": {"correctedmissingdata": "h2g: correctedmissingdata"},"statusCodes": null,"annotation": "http://localhost:5000/h2gontology/corrmissingdata.owl#getcorrectmissingdata"}],"links": [{"supportedOperations": "http-methods:POST","annotation": "http://localhost:5000/resourcerelation.owl#Iscomplementary","key": "EnergyHeatPrediction","value": "http://localhost:5000/service/PredHeatEngCons"}]}';
