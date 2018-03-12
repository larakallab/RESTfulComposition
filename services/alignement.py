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


alignement = Blueprint('alignement', __name__,)

def gen_series(n, min_val, max_val):
 	x = []
 	for i in range(0, n):
 		x.append(randint(min_val, max_val))
 	return x

@alignement.route('', methods=['GET', 'HEAD'])
def alignement():
	datavalues1 = request.args.get('data1')
	datavalues2 = request.args.get('data2')
	dataaligned=[]
	if request.method == 'GET':
		for j in range(len(datavalues)):
			dataaligned[j]= [int(datavalues1)+1, int(datavalues2)+1]
		resp = make_response(jsonify(data=dataaligned))
		return resp
	
	
