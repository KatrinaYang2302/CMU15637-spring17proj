import urllib;
import urllib2;
import xml.etree.ElementTree as ET;

from django.db import models;
from project.models import *;


key = "EAhYqnqmHrfXvT8rpmSDkgEbP";
baseURL = "http://truetime.portauthority.org/bustime/api/v1/";

def validate_route(route):
	route = process(route);
	rts = rt.objects.filter(rt_no__exact=route);
	if rts and rts.len():
		return 1;
	return 0;

def get_api_response(method, params):
	#method: the action we are querying
	#params: the parametres (except the key) in an dictionary format
	url = baseURL + method + "?key=" + key;
	for param in params:
		url = url + "&" + param + "=" + params[param];
	#print url;
	response = urllib2.urlopen(url);
	#print str(response.read());
	return str(response.read());

#params = {};
#params['vid'] = "6244";
#get_api_response("getvehicles", params);

def get_date_id(year, month, day):
	wholeyear = (year-2016) * 365;
	leap = int((year-2017)/4) + 1;
	if year%4==0 and month > 2:
		leap = leap + 1;
	months = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
	res = leap + wholeyear;
	for i in range(1, 13):
		if i == month:
			res = res + day;
			return res;
		res = res + months[i];
	return res;

def parse_time(time_str):
	#get number of minutes with a specified time
	date, nowtime = time_str.split(' ');
	hour, minute = nowtime.split(':');
	#print date, hour, minute;
	hour = int(hour);
	minute = int(minute);
	year = int(date[0:4]);
	month = int(date[4:6]);
	day = int(date[6:8]);
	return 1440 * get_date_id(year, month, day) + 60 * hour + minute;

def get_predictions(stop_id, route):
	#final target: get the predicted arrival/departure time in minutes
	#if error (e.g. no more buses coming in predicted time), return -1
	params = {};
	params['rt'] = str(route);
	params['stpid'] = str(stop_id);
	raw_str = get_api_response("getpredictions", params);
	#print "string:";
	#print raw_str;
	try:
		root = ET.fromstring(raw_str);
	except:
		return -1;
	#print root;
	for child in root:
		if child.tag == "error":
			return -1;
		#print child;
		try:
			prd_time_str = child.find('prdtm').text;
			#return 0;
			now_time_str = child.find('tmstmp').text;
		except:
			return -1;
		#print prd_time_str;
		#print now_time_str;
		time_diff = parse_time(prd_time_str) - parse_time(now_time_str);
		if time_diff < 0 or time_diff > 1440:
			#if larger than one day
			return -1;
		return time_diff;
		
#print get_predictions(4407, "67");