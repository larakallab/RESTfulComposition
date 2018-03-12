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


getmeasure = Blueprint('getmeasure', __name__,)

def gen_series(n, min_val, max_val):
 	x = []
 	for i in range(0, n):
 		x.append(randint(min_val, max_val))
 	return x

@getmeasure.route('', methods=['GET', 'HEAD'])
def getMeasure():
	startdate = request.args.get('startdate')
	enddate = request.args.get('enddate')
	measure = request.args.get('measure')
	if request.method == 'GET':
		v = gen_series(10, 18, 24)
		resp = make_response(jsonify(data=v))
		return resp
	
	
