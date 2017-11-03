var A;
function collIntTemp() {
	$.ajax({url: 'http://localhost:5000/service/PredInTemperature', type: 'get', dataType: 'json', crossDomain: true, data: '{"startdate":"22062017", "enddate":"22062017"}', success:function(data){console.log(data);}});}  

function collExtTemp() {
	$.ajax({url: 'http://localhost:5000/service/PredOutTemperature', type: 'get', dataType: 'json', crossDomain: true, data: '{"startdate":"22062017", "enddate":"22062017"}', success:function(data){console.log(data);}});}  

function missDataMan() {
	$.ajax({url: 'http://localhost:5000/service/missingdata', type: 'POST', dataType: 'json', crossDomain: true, data: '{"data":[{"date":"22062017", "val":"12"}, {"date":"23062017", "val":"13"}]}', success:function(data){ console.log(data);}, error: function (xhr, ajaxOptions, thrownError) { console.log(xhr.status); console.log(xhr.responseText); console.log(thrownError);}});}

function outDataMan() {
	$.ajax({url: 'http://localhost:5000/service/outliersdata', type: 'POST', dataType: 'json', crossDomain: true, data: '{"data":[{"date":"22062017", "val":"12"}, {"date":"23062017", "val":"13"}]}', success:function(data){console.log(data);}});}

function corrMissData() {
	$.ajax({url: 'http://localhost:5000/service/CorrMissingData', type: 'get', dataType: 'json', crossDomain: true, data: '{"data_id":"1"}', success:function(data){console.log(data);}});}

function corrOutData() {
	$.ajax({url: 'http://localhost:5000/service/corrOutlierData', type: 'get', dataType: 'json', crossDomain: true, data: '{"data_id":"2"}', success:function(data){console.log(data);}});}

function predEnHeatCons() {
	$.ajax({url: 'http://localhost:5000/service/PredHeatEngCons', type: 'POST', dataType: 'json', crossDomain: true, data: '{"startdate":"22062017", "enddate":"22062017", "data":[{"date":"22062017", "val":"12"}, {"date":"23062017", "val":"13"}], "data":[{"date":"22062017", "val":"12"}, {"date":"23062017", "val":"13"}], "data":[{"date":"22062017", "val":"12"}, {"date":"23062017", "val":"13"}]}', success:function(data){console.log(data);}});}

function enHeatCons() {
	$.ajax({url: 'http://localhost:5000/service/HeatEngCons', type: 'get', dataType: 'json', crossDomain: true, data: '{"data_id":"3"}', success:function(data){console.log(data);}});}

function composition(){	
	var A = $.ajax({url: 'http://localhost:5000/service/PredInTemperature', type: 'get', dataType: 'json', crossDomain: true, global: false, async: false, data: '{"startdate":"22062017", "enddate":"22062017"}', success:function(data){tmp=data;}, error: function (xhr, ajaxOptions, thrownError) { console.log(xhr.status); console.log(xhr.responseText); console.log(thrownError);}}).responseText;
	var B = $.ajax({url: 'http://localhost:5000/service/PredOutTemperature/22062017-22062017', type: 'get', dataType: 'json', crossDomain: true, global: false, async: false, success:function(data){tmp=data;}}).responseText;
	var C = $.ajax({url: 'http://localhost:5000/service/missingdata/'+A, type: 'POST', dataType: 'json', crossDomain: true, global: false, async: false, success:function(data){tmp=data;}}).responseText;
	var D = $.ajax({url: 'http://localhost:5000/service/outliersdata/'+A, type: 'POST', dataType: 'json', crossDomain: true, global: false, async: false, success:function(data){tmp=data;}}).responseText;
	var E = $.ajax({url: 'http://localhost:5000/service/CorrMissingData/'+C, type: 'get', dataType: 'json', crossDomain: true, global: false, async: false, success:function(data){tmp=data;}}).responseText;
	var F = $.ajax({url: 'http://localhost:5000/service/corrOutlierData/'+D, type: 'get', dataType: 'json', crossDomain: true, global: false, async: false, success:function(data){tmp=data;}}).responseText;
	var G = $.ajax({url: 'http://localhost:5000/service/PredHeatEngCons/22062017-22062017-'+C+'-'+D+'-'+A, type: 'post', dataType: 'json', crossDomain: true, global: false, async: false, success:function(data){tmp=data;}}).responseText;
	var H = $.ajax({url: 'http://localhost:5000/service/HeatEngCons/'+G, type: 'get', dataType: 'json', crossDomain: true, global: false, async: false, success:function(data){tmp=data;}}).responseText;
	console.log(H)
	}
	
function JSONtoJS(){

var data = '{"composition":{"services":['+'{ "url": "http://localhost:5000/service/PredInTemperature", "method": "get", "name": "GetPredictedInternalTemperature",  "parameters":[ {"p1": "22062017"}, {"p2": "23062017"}], "output":"A"},'+'{"url": "http://localhost:5000/service/PredOutTemperature", "method": "get", "name": "GetPredictedExternalTemperature","parameters":[{"p1": "22062017"},{"p2": "23062017"}],"output":"B"},'+'{"url": "http://localhost:5000/service/missingdata", "method": "POST", "name": "missingData","parameters":[{"p1": "A"}],"output":"C"}]}}';
var json = JSON.parse(data);
console.log (json.composition.services[0].url);
console.log (json.composition.services[1].url);
console.log (json.composition.services[1].url);

for (var key in json.composition.services) {
var par;
var arr = [];
var a = [];
if (key ==0){
for (var keyp in json.composition.services[key].parameters) {

if (keyp==0){
par=json.composition.services[key].parameters[keyp].p1;
} if (keyp==1){
par+= "-"+json.composition.services[key].parameters[keyp].p2;
} if (keyp==2){
par+= "-"+json.composition.services[key].parameters[keyp].p3;
} if (keyp==3){
par+= "-"+json.composition.services[key].parameters[keyp].p4;
}
}
a.push($.ajax({url: json.composition.services[key].url+'/'+par, type: json.composition.services[key].method, dataType: 'json', crossDomain: true, global: false, async: false, success:function(data){tmp=data;}}).responseText);
}
else {
for (var keyp in json.composition.services[key].parameters) {
for (i=0;i<key;i++){
if ((Object.values(json.composition.services[key].parameters[keyp]) == json.composition.services[i].output) && (keyp==0)){
par = json.composition.services[i].output;
}if ((Object.values(json.composition.services[key].parameters[keyp]) == json.composition.services[i].output) && (keyp!=0)){
par = par+"-"+json.composition.services[i].output;
}
if ((Object.values(json.composition.services[key].parameters[keyp]) != json.composition.services[i].output) && (keyp==0)){
par = Object.values(json.composition.services[key].parameters[keyp]);
}if ((Object.values(json.composition.services[key].parameters[keyp]) != json.composition.services[i].output) && (keyp!=0)){
par = par+"-"+Object.values(json.composition.services[key].parameters[keyp]);
}
}
}
console.log(par);
}
}
}

function sendComposition(){		
var x = document.getElementById("textarea1").value;
var s = JSON.parse(x);
console.log(s);
$.ajax({url: 'http://localhost:5000/service/composition', type: 'POST', dataType: 'json', contentType: 'application/json', data:  JSON.stringify(s), crossDomain: true, success:function(data){console.log(data);}});
}

function runHATEOASComposition(){		
var x = document.getElementById("textarea1").value;
var s = JSON.parse(x);
console.log(s);
$.ajax({url: 'http://localhost:5000/service/hateoascomposition', type: 'POST', dataType: 'json', contentType: 'application/json', data:  JSON.stringify(s), crossDomain: true, success:function(data){console.log(data);}});
}

function executeComposition(){		
$.ajax({url: 'http://localhost:5000/service/composition/execute', type: 'get', dataType: 'json', crossDomain: true, data: '{"composition_id":"4"}', success:function(data){console.log(data);}});
}

function validateComposition(){		
$.ajax({url: 'http://localhost:5000/service/composition/validate', type: 'get', dataType: 'json', crossDomain: true, data: '{"composition_id":"5"}', success:function(data){console.log(data);}});
}
