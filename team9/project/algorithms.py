from __future__ import unicode_literals

from django.db import models
#from django.contrib.auth.models import User

from project.models import *;
from Queue import PriorityQueue;
from math import *;
foot_to_metre = 0.3048;
earth_rad = 6369.925; #earth radius in Pittsburgh, in KM
thres = 0.01;

class Astop(object):
	def __init__(self, stopid, dist):
		self.stopid = stopid;
		self.dist = dist;
		return;
		
	def __cmp__(self, other):
		return cmp(other.dist, self.dist);
		

def to_rad(deg):
	return deg * (3.1415926535897932/180);

def cal_dist(long1, lat1, long2, lat2):
	#calculate the distance of pairs of positions represented by longitude and lattitude, using "Haversine formula" (in metres)
	long0 = to_rad(long2-long1);
	lat0 = to_rad(lat2-lat1);
	sin0 = sin(lat0*0.5);
	sin1 = sin(0.5*long0);
	tVal = sin0*sin0 + sin1*sin1*cos(to_rad(lat1)*cos(to_rad(lat2)));
	return 2000.0 * earth_rad * atan2(sqrt(tVal), sqrt(1-tVal));
	
def nearestK(long, lat, k):
	#use fetch-on-query here. Can it be converted to pre caching?
	#returns nearest k stop ids
	#assume k < 100 (we have a lot of stops)
	allstops = stops.objects.all();
	cnt = 0;
	pq = PriorityQueue();
	for stop in allstops:
		dist = cal_dist(long, lat, stop.stop_long, stop.stop_lat);
		if cnt < k:
			pq.put(Astop(stop.stop_id, dist));
			cnt = cnt + 1;
		else:
			pq.put(Astop(stop.stop_id, dist));
			fei = pq.get();
	result = [];
	while not pq.empty():
		result = [pq.get().stopid,] + result;
	
	return result;

def nearestStop(long, lat):
	#return the stop id of the nearest stop to (long, lat).
	#can be in future used to query predictions.
	#if no stops are within long/lat difference $thres$ (default: 0.01), return -1.
	longL = long - thres;
	longU = long + thres;
	latL = lat - thres;
	latU = lat + thres;
	stopset = stops.objects.filter(stop_long__lte = longU, stop_long__gte = longL, stop_lat__lte = latU, stop_lat__gte = latL);
	if not stopset or not stopset.len():
		return -1;
	minDist = 1e5;
	minId = -1;
	for stop in stopset:
		thislong = stop.stop_long;
		thislat = stop.stop_lat;
		thisDist = cal_dist(thislong, thislat, long, lat);
		if thisDist < minDist:
			minDist = thisDist;
			minId = stop.stop_id;
	return minId;
	
def nearThanK(long, lat, k):
	#finds all stops nearer or equal to distance k
	#do not except for k>1024 in metre
	if k > 1024:
		k = 1024;
	allstops = stops.objects.all();
	pq = PriorityQueue();
	for stop in allstops:
		dist = cal_dist(long, lat, stop.stop_long, stop.stop_lat);
		if dist <= k:
			pq.put(Astop(stop.stop_id, dist));
	result = [];
	while not pq.empty():
		result = [pq.get().stopid,] + result;
	
	return result;
	
def match(str, k):
	#find k relevant stops according to stop name matching.
	allstops = stops.objects.all();
	result = [];
	for stop in allstops:
		if stop.stop_name.lower().find(str.lower()) != -1:
			result = result + [stop.stop_id,];
	return result;
	
