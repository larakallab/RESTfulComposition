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


conversion = Blueprint('conversion', __name__,)

def gen_series(n, min_val, max_val):
 	x = []
 	for i in range(0, n):
 		x.append(randint(min_val, max_val))
 	return x

@conversion.route('', methods=['GET', 'HEAD'])
def conversion0():
	data = request.get_json()
	print (data)
	if request.method == 'GET':
		v = gen_series (5, 25, 30) 
		resp = make_response(jsonify(data=v))
		return resp
	
	
