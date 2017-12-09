from Queue import PriorityQueue;
from math import *;

foot_to_metre = 0.3048;
earth_rad = 6369.925; #earth radius in Pittsburgh, in KM
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
	

a = {};
a['test'] = 1;
print a;
for A in a:
	a[A] = 2;
print a;	

print cal_dist(-79.92293412433798,40.436093683036, -79.94356058465502,40.444671114203);
