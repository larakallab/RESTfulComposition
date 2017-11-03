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

predouttemperature = Blueprint('predouttemperature', __name__,)

@predouttemperature.route('', methods=['GET', 'HEAD'])
def getPredOutTemperature():
	parser = reqparse.RequestParser()
	parser.add_argument('startdate')
	parser.add_argument('enddate')
	args = parser.parse_args()
	if request.method == 'GET':
		v = '30, 0, 34, 0, 34, 35, 51, 31, 33, 45'
		resp = make_response(jsonify(data=v))
		resp.headers['Link'] = 'http://localhost:5000/CollectPredExtTemp/CollectPredExtTemp.md'
		return resp
	if request.method == 'HEAD':
		resp = make_response()
		resp.headers['Link'] = 'http://localhost:5000/CollectPredExtTemp/CollectPredExtTemp.md'
		return resp


@predouttemperature.route('/CollectPredExtTemp.md')	
def getDescriptorCollectPredExtTemp():
	return '{"@context": "http://localhost:5000/context.jsonld","@id": "http://localhost:5000/CollectPredExtTemp/CollectPredExtTemp.md","@type": "Descriptor","annotation": "","operations": [{"method": "GET","expects": {"startdate": "h2g:startdate","enddate": "h2g:enddate"},"returns": {"externalpredictedtemperature": "h2g:externalpredictedtemperature"},"statusCodes": null,"annotation": "http://localhost:5000/h2gontology/predouttemp.owl#getpredictedexternaltemperature"}],"links": [{"supportedOperations": "http-methods:POST","annotation": "http://localhost:5000/resourcerelation.owl#Iscomplementary","key": "CorrectMissingData","value": "http://localhost:5000/service/missingdata"},{"supportedOperations": "http-methods:POST","annotation": "http://localhost/resourcerelation.owl#Iscomplementary","key": "CorrectOutliersData","value": "http://localhost:5000/service/outliersdata"}]}';
