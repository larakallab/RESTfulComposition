#!/usr/bin/env python

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

from services.predintemperature import predintemperature
from services.predouttemperature import predouttemperature
from services.missingdata import missingdata
from services.outliersdata import outliersdata
from services.corrmissingdata import corrmissingdata
from services.corroutlierdata import corroutlierdata
from services.predheatengcons import predheatengcons
from services.heatengcons import heatengcons
from static import static
from hateoas import hateoas


app = Flask(__name__)

app.register_blueprint(predintemperature, url_prefix='/service/PredInTemperature')
app.register_blueprint(predintemperature, url_prefix='/CollectPredIntTemp')
app.register_blueprint(predouttemperature, url_prefix='/service/PredOutTemperature')
app.register_blueprint(predouttemperature, url_prefix='/CollectPredExtTemp')
app.register_blueprint(missingdata, url_prefix='/service/missingdata')
app.register_blueprint(missingdata, url_prefix='/CorrectMissingData')
app.register_blueprint(outliersdata, url_prefix='/service/outliersdata')
app.register_blueprint(outliersdata, url_prefix='/CorrectOutliersData')
app.register_blueprint(corrmissingdata, url_prefix='/service/CorrMissingData')
app.register_blueprint(corrmissingdata, url_prefix='/GetCorrectedMissingData')
app.register_blueprint(corroutlierdata, url_prefix='/service/corrOutlierData')
app.register_blueprint(corroutlierdata, url_prefix='/GetCorrectedOutliersData')
app.register_blueprint(predheatengcons, url_prefix='/service/PredHeatEngCons')
app.register_blueprint(predheatengcons, url_prefix='/EnergyHeatPrediction')
app.register_blueprint(heatengcons, url_prefix='/service/HeatEngCons')
app.register_blueprint(heatengcons, url_prefix='/EnergyHeatConsumption')

app.register_blueprint(static, url_prefix='')
app.register_blueprint(static, url_prefix='/service')
app.register_blueprint(static, url_prefix='/service/composition')

app.register_blueprint(hateoas, url_prefix='')

	
if __name__ == '__main__':
    app.run(threaded=True)