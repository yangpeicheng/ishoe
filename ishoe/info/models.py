# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import date
import datetime
from django.utils import timezone
from django.http import JsonResponse
import time
import pytz
# Create your models here.
'''用户：
    姓名，地址，
'''
class Person(models.Model):
    name=models.CharField(max_length=30)
    address=models.CharField(max_length=50)
    birth=models.DateField()
    ble_mac=models.CharField(max_length=30,primary_key=True)
    gender=models.BooleanField(default=False)
    ignore=models.BooleanField(default=False)
    def __unicode__(self):
        return self.name


class Rpi(models.Model):
    ip=models.CharField(max_length=30,default="192.1.2.105",primary_key=True)
    location=models.CharField(max_length=20,default="001")
    time=models.DateTimeField(default = timezone.now)

    def __unicode__(self):
        return self.ip

class Sensortag(models.Model):
    person=models.ForeignKey(Person,on_delete=models.CASCADE)

    rpi=models.ForeignKey(Rpi,on_delete=models.CASCADE)

    light=models.FloatField()

    acc_x=models.FloatField()
    acc_y=models.FloatField()
    acc_z=models.FloatField()

    gyro_x=models.FloatField()
    gyro_y=models.FloatField()
    gyro_z=models.FloatField()

    magn_x=models.FloatField()
    magn_y=models.FloatField()
    magn_z=models.FloatField()

    time=models.CharField(max_length=30)

    def __unicode__(self):
        return "adsa"

class State(models.Model):
    person=models.ForeignKey(Person,primary_key=True,on_delete=models.CASCADE)
    rpi=models.ForeignKey(Rpi,on_delete=models.CASCADE)
    #move_flag=models.BooleanField(default=False)
    move_flag=models.PositiveSmallIntegerField()
    time=models.DateTimeField(default = timezone.now)
    def __unicode__(self):
        return unicode(self.time)
    
    def toJson(self):
        dict={}
        dict['name']=self.person.name
        dict['ble']=self.person.ble_mac
        dict['location']=self.rpi.location
        dict['state']=self.move_flag
        return dict

# class Heartbeat(models.Model):
#     rpi=models.ForeignKey(Rpi,primary_key=True,on_delete=models.CASCADE)
#     time=models.DateTimeField()
#     flag=models.BooleanField(default=False)

class Warning:
    def __init__(self,name,location,type,id):
        self.name=name
        self.location=location
        self.type=type
        self.id=id

    

class PersonInfo:
    def __init__(self,id,name,birth,gender,address):
        self.name=name
        self.id=id
        self.gender=gender
        self.address=address
        self.gender="男"
        if gender==False:
            self.gender="女"
        today=date.today()
        t=time.strptime(birth,"%Y-%m-%d")
        birth=date(t[0],t[1],t[2])
        try:
            b=birth.replace(year=today.year)
        except ValueError:
            b=birth.replace(year=today.year,day=birth.day-1)
        if b>today:
            self.age=today.year-birth.year-1
        else:
            self.age=today.year-birth.year
    
    def toJson(self):
        d={'name':self.name,'id':self.id,'gender':self.gender,'address':self.address,'age':self.age}
        return d

class DeviceState:
    def __init__(self,ip,location,time):
        self.ip=ip
        self.location=location
        start=timezone.now()-datetime.timedelta(minutes=1)
        # t=start.replace(tzinfo=pytz.timezone('UTC'))
        self.state=time>start
    