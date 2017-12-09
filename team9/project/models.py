from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
	
class bus_user(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE);
	phone_number = models.BigIntegerField(default=0);
	
class fav_place(models.Model):
	user = models.ForeignKey(User, default=None);
	place_name = models.CharField(max_length=255);
	place_lat = models.FloatField(default=0.0);
	place_long = models.FloatField(default=0.0);
	
class fav_rt(models.Model):
	user = models.ForeignKey(User, default=None);
	rt_no = models.CharField(max_length=4);
	
class stops(models.Model):
	stop_id = models.IntegerField(default=0, primary_key=True);
	stop_name = models.CharField(max_length=255);
	stop_long = models.FloatField(default=0.0);
	stop_lat = models.FloatField(default=0.0);
	
class rt(models.Model):
	rt_no = models.CharField(max_length=4,primary_key=True);
	rt_name = models.CharField(max_length=255);

class rt_stop(models.Model):
	rt_no = models.ForeignKey(rt, default=None);
	stop_id = models.ForeignKey(stops, default=None);
	dir = models.CharField(max_length=255);
	dist = models.FloatField(default=0);
	