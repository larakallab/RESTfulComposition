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

predheatengcons = Blueprint('predheatengcons', __name__,)

@predheatengcons.route('', methods=['POST', 'HEAD'])
def PredHeatEngCons():
	parser = reqparse.RequestParser()
	parser.add_argument('startdate')
	parser.add_argument('enddate')
	parser.add_argument('data')
	parser.add_argument('data')
	parser.add_argument('data')
	args = parser.parse_args()
	if request.method == 'POST':
		v = '3'
		resp = make_response(jsonify(data_id=v))
		resp.headers['Link'] = 'http://localhost:5000/EnergyHeatPrediction/EnergyHeatPrediction.md'
		return resp
	if request.method == 'HEAD':
		resp = make_response()
		resp.headers['Link'] = 'http://localhost:5000/EnergyHeatPrediction/EnergyHeatPrediction.md'
		return resp

@predheatengcons.route('/EnergyHeatPrediction.md')
def getDescriptorEnergyHeatPrediction():
	return '{"@context": "http://localhost:5000/context.jsonld","@id": "http://localhost:5000/EnergyHeatPrediction/EnergyHeatPrediction.md","@type": "Descriptor","annotation": "","operations": [{"method": "POST","expects": {"startdate": "h2g:startdate","enddate": "h2g:enddate","correctedmissingdata": "h2g: correctedmissingdata","correctedoutliersdata": "h2g: correctedoutliersdata","internalpredictedtemperature": "h2g:internalpredictedtemperature"},"returns": {"data_id": "h2g:data_id"},"statusCodes": null,"annotation": "http://localhost:5000/h2gontology/energyheatpred.owl#predictenergyheat"}],"links": [{"supportedOperations": "http-methods:GET","annotation": "http://localhost:5000/resourcerelation.owl#Iscomplementary","key": "EnergyHeatPrediction","value": "http://localhost:5000/service/HeatEngCons"}]}';
