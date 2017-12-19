#!/usr/bin/env python

from flask import Blueprint 
from flask import Flask
from flask import request
from flask_restful import reqparse


from ModelingEngine import ModelingEngine
from ValidationEngine import ValidationEngine
from ExecutionEngine import ExecutionEngine

static = Blueprint('static', __name__,)

@static.route('/services/composition', methods=["POST"])
def postComposition():
	global composition; 
	modeling = ModelingEngine()
	composition = modeling.getComposition()		
	global outputPlaces;
	outputPlaces = modeling.JSONtoPNML(composition)
	print (outputPlaces)
	validation = ValidationEngine()
	validation.validateComposition(composition, outputPlaces)
	return ''

@static.route('/composition/execute')
def executeComposition():
	#parser = reqparse.RequestParser()
	#parser.add_argument('composition_id')
	#for item in data2['composition']['variables']:
		#variables.append(item)
		#parser.add_argument(item)
	#print (variables)
	print (request.args.get('startDate'))
	print (request.args)
	#args = parser.parse_args()
	
	execution = ExecutionEngine()
	execution.executeComposition(composition)
	return ''
	
