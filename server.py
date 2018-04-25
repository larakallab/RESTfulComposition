#!/usr/bin/env python

from flask import Flask, url_for, json, render_template
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


from services.getmeasure import getmeasure
from services.conversion import conversion
from services.alignement import alignement
from services.predintemperature import predintemperature
from services.predouttemperature import predouttemperature
from services.missingdata import missingdata
from services.outliersdata import outliersdata
from services.corrmissingdata import corrmissingdata
from services.corroutlierdata import corroutlierdata
from services.predheatengcons import predheatengcons
from services.heatengcons import heatengcons

from servicesDesc.ATC1 import getairtemp
from servicesDesc.ATC2 import collectairtemp
from servicesDesc.ATC3 import collairtemp
from servicesDesc.CTC1 import getclimtemp
from servicesDesc.CTC2 import collectclimtemp
from servicesDesc.CTC3 import collclimtemp
from servicesDesc.MVD1 import missvaldetection
from servicesDesc.MVD2 import missvaldet
from servicesDesc.MVD3 import missdet
from servicesDesc.MVI1 import missvalinterpolation
from servicesDesc.MVI2 import missvalint
from servicesDesc.MVI3 import missint
from servicesDesc.OVD1 import outvaldetection
from servicesDesc.OVD2 import outvaldet
from servicesDesc.OVD3 import outdet
from servicesDesc.OVI1 import outvalinterpolation
from servicesDesc.OVI2 import outvalint
from servicesDesc.OVI3 import outint
from servicesDesc.BEDP1 import predheatengcons
from servicesDesc.BEDP2 import predheateng
from servicesDesc.BEDP3 import predheat

from static import static
from hateoas import hateoas
from discovery_enhanced import discovery


app = Flask(__name__)

app.register_blueprint(getmeasure, url_prefix='/getmeasure')
app.register_blueprint(conversion, url_prefix='/conversion')
app.register_blueprint(alignement, url_prefix='/alignment')
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
#app.register_blueprint(predheatengcons, url_prefix='/service/PredHeatEngCons')
#app.register_blueprint(predheatengcons, url_prefix='/EnergyHeatPrediction')
app.register_blueprint(heatengcons, url_prefix='/service/HeatEngCons')
app.register_blueprint(heatengcons, url_prefix='/EnergyHeatConsumption')

app.register_blueprint(getairtemp, url_prefix='/resource/getairtemperature')
app.register_blueprint(getairtemp, url_prefix='/resourceDescription')
app.register_blueprint(collectairtemp, url_prefix='/resource/collectairtemperature')
app.register_blueprint(collectairtemp, url_prefix='/resourceDescription')
app.register_blueprint(collairtemp, url_prefix='/resource/collairtemp')
app.register_blueprint(collairtemp, url_prefix='/resourceDescription')

app.register_blueprint(getclimtemp, url_prefix='/resource/getclimtemperature')
app.register_blueprint(getclimtemp, url_prefix='/resourceDescription')
app.register_blueprint(collectclimtemp, url_prefix='/resource/collectclimtemperature')
app.register_blueprint(collectclimtemp, url_prefix='/resourceDescription')
app.register_blueprint(collclimtemp, url_prefix='/resource/collclimtemp')
app.register_blueprint(collclimtemp, url_prefix='/resourceDescription')

app.register_blueprint(missvaldetection, url_prefix='/resource/missvaldetection')
app.register_blueprint(missvaldetection, url_prefix='/resourceDescription')
app.register_blueprint(missvaldet, url_prefix='/resource/missvaldet')
app.register_blueprint(missvaldet, url_prefix='/resourceDescription')
app.register_blueprint(missdet, url_prefix='/resource/missdet')
app.register_blueprint(missdet, url_prefix='/resourceDescription')

app.register_blueprint(outvaldetection, url_prefix='/resource/outvaldetection')
app.register_blueprint(outvaldetection, url_prefix='/resourceDescription')
app.register_blueprint(outvaldet, url_prefix='/resource/outvaldet')
app.register_blueprint(outvaldet, url_prefix='/resourceDescription')
app.register_blueprint(outdet, url_prefix='/resource/outdet')
app.register_blueprint(outdet, url_prefix='/resourceDescription')

app.register_blueprint(missvalinterpolation, url_prefix='/resource/missvalinterpolation')
app.register_blueprint(missvalinterpolation, url_prefix='/resourceDescription')
app.register_blueprint(missvalint, url_prefix='/resource/missvalint')
app.register_blueprint(missvalint, url_prefix='/resourceDescription')
app.register_blueprint(missint, url_prefix='/resource/missint')
app.register_blueprint(missint, url_prefix='/resourceDescription')

app.register_blueprint(outvalinterpolation, url_prefix='/resource/outvalinterpolation')
app.register_blueprint(outvalinterpolation, url_prefix='/resourceDescription')
app.register_blueprint(outvalint, url_prefix='/resource/outvalint')
app.register_blueprint(outvalint, url_prefix='/resourceDescription')
app.register_blueprint(outint, url_prefix='/resource/outint')
app.register_blueprint(outint, url_prefix='/resourceDescription')

app.register_blueprint(predheatengcons, url_prefix='/resource/predheatengcons')
app.register_blueprint(predheatengcons, url_prefix='/resourceDescription')
app.register_blueprint(predheateng, url_prefix='/resource/predheateng')
app.register_blueprint(predheateng, url_prefix='/resourceDescription')
app.register_blueprint(predheat, url_prefix='/resource/predheat')
app.register_blueprint(predheat, url_prefix='/resourceDescription')

app.register_blueprint(static, url_prefix='')
app.register_blueprint(static, url_prefix='')
app.register_blueprint(static, url_prefix='/services')

app.register_blueprint(hateoas, url_prefix='')

app.register_blueprint(discovery, url_prefix='')

@app.route('/')
def homePage():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(threaded=True)
    app.run(debug=True)
