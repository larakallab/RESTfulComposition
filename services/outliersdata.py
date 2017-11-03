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

outliersdata = Blueprint('outliersdata', __name__,)

@outliersdata.route('', methods=['POST', 'HEAD'])
def outlierData():
	parser = reqparse.RequestParser()
	parser.add_argument('data')
	args = parser.parse_args()
	if request.method == 'POST':
		v = '2'
		resp = make_response(jsonify(data_id=v))
		resp.headers['Link'] = 'http://localhost:5000/CorrectOutliersData/CorrectOutliersData.md'
		return resp
	if request.method == 'HEAD':
		resp = make_response()
		resp.headers['Link'] = 'http://localhost:5000/CorrectOutliersData/CorrectOutliersData.md'
		return resp

@outliersdata.route('/CorrectOutliersData.md')
def getDescriptorCorrectOutliersData():
	return '{"@context": "http://localhost:5000/context.jsonld","@id": "http://localhost:5000/CorrectOutliersData/CorrectOutliersData.md","@type": "Descriptor","annotation": "","operations": [{"method": "POST","expects": {"externalpredictedtemperature": "h2g:externalpredictedtemperature"},"returns": {"data_id": "h2g:data_id"},"statusCodes": null,"annotation": "http://localhost:5000/h2gontology/outliersdata.owl#correctoutliersdata"}],"links": [{"supportedOperations": "http-methods:GET","annotation": "http://localhost:5000/resourcerelation.owl#Iscomplementary","key": " CorrectOutliersData","value": "http://localhost:5000/service/corrOutlierData"}]}';
