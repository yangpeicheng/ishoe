# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect,JsonResponse,HttpResponse
from models import Person,State,Warning,PersonInfo,Rpi
from django.utils import timezone
import models
import datetime
# Create your views here.
TAG_LIST=[]
FRESH=True
def state_list(requests):
    return render_to_response('sum.html',)

def uploadImg(requests):
    pass

def info_detail(requests):
    return render_to_response('sign-up.html')

def updateTagList():
    global TAG_LIST
    TAG_LIST=[]
    for p in Person.objects.all():
        TAG_LIST.append(p.ble_mac)
    return TAG_LIST


def submit(requests):
    errors=[]
    if requests.method=="POST":
        if not requests.POST.get('name',''):
            errors.append("输入姓名。")
        if not requests.POST.get('address',''):
            errors.append("输入家庭住址。")
        if not requests.POST.get('ble_mac',''):
            errors.append("输入蓝牙地址。")
        if not errors:
            #print(requests.POST['name'])
            p=Person.objects.filter(ble_mac=requests.POST['ble_mac'])
            if len(p)>0 :
                errors.append("该蓝牙已被使用")
            else:
                p=Person(name=requests.POST['name'],address=requests.POST['address'],birth=requests.POST['birthday'],ble_mac=requests.POST['ble_mac'])
                p.save()
                return HttpResponseRedirect('/index/')
    return render_to_response('sign-up.html',{'errors':errors})
                    
def get_head(requests):
    return render_to_response('head.html')

def get_left(requests):
    return render_to_response('left.html')

def get_index(requests):
    start=timezone.now()-datetime.timedelta(minutes=1)
    State.objects.filter(time__lt=start).update(move_flag=4)
    abnormal_state=State.objects.filter(move_flag__gt=0,person__ignore=False)    
    warnings=[]
    for s in abnormal_state:
        warning=Warning(s.person.name,s.rpi.location,s.move_flag,s.person.ble_mac)
        warnings.append(warning)
    return render_to_response('indexajax.html',{'states':State.objects.all(),'warnings':warnings})

def ajax_list(requests):
    start=timezone.now()-datetime.timedelta(minutes=1)
    State.objects.filter(time__lt=start).update(move_flag=4)
    abnormal_state=State.objects.filter(move_flag__gt=0,person__ignore=False)  
    dict={"state":None,"warning":None}
    state_dict={}
    for s in State.objects.all():
        state_dict[s.person.ble_mac]=[s.person.name,s.rpi.location,s.person.ignore,s.move_flag]
    dict["state"]=state_dict
    warnings={}
    for s in abnormal_state:
        warnings[s.person.ble_mac]=[s.person.name,s.rpi.location,s.move_flag,s.person.ble_mac]
    if len(warnings)>0:
        dict["warning"]=warnings
    return JsonResponse(dict)

def handle_person(requests):
    all=[]
    for p in Person.objects.all():
        all.append(PersonInfo(p.ble_mac,p.name,str(p.birth),p.gender,p.address))
    return render_to_response('person.html',{'person_list':all})

def add_person(requests):
    global FRESH
    response={"status":True,"message":None}
    try:
        rname=requests.POST.get('name')
        rbirth=requests.POST.get('birth')
        raddress=requests.POST.get('address')
        if requests.POST.get('gender')=='true':
            rgender=True
        else:
            rgender=False
        rble_mac=requests.POST.get('ble_mac')
        check=Person.objects.filter(ble_mac=rble_mac)
        if check:
            response["status"]=False
            response["message"]="输入了已使用的蓝牙地址！"
        else:
            p=Person.objects.create(name=rname,birth=rbirth,address=raddress,gender=rgender,ble_mac=rble_mac)
            r=Rpi.objects.all()[0]
            State.objects.create(person=p,rpi=r,move_flag=0)
            response.update(PersonInfo(rble_mac,rname,rbirth,rgender,raddress).toJson())
            FRESH=True
            #return PersonInfo(rble_mac,rname,rbirth,rgender,raddress).toJson()
    except Exception as e:
        response["status"]=False
        response["message"]="输入数据错误"
    return JsonResponse(response)

def delete_person(requests):
    global FRESH
    response={'status':False}
    try:
        nid=requests.GET.get('nid')
        Person.objects.filter(ble_mac=nid).delete()
        response['status']=True
        FRESH=True
        #print(nid)
    except Exception as e:
        response={'status':False}
    return JsonResponse(response)

def update_person(requests):
    response={"status":False,"message":None}
    try:
        rname=requests.POST.get('name')
        rbirth=requests.POST.get('birth')
        raddress=requests.POST.get('address')
        if requests.POST.get('gender')=='true':
            rgender=True
        else:
            rgender=False
        rble_mac=requests.POST.get('ble_mac')
        raw=requests.POST.get('raw')
        p=Person.objects.filter(ble_mac=raw)
        if p:
            p.update(ble_mac=rble_mac,birth=rbirth,address=raddress,gender=rgender,name=rname)
            response["status"]=True
        else:
            response["message"]="输入错误的蓝牙地址"
    except Exception as e:
        response["message"]="输入数据错误"
    return JsonResponse(response)
            
def handle_device(requests):
    devices=[]
    for d in Rpi.objects.all():
        t=models.DeviceState(d.ip,d.location,d.time)
        devices.append(t)
    return render_to_response('device.html',{"device":devices})

def add_device(requests):
    response={"status":False,"message":None}
    try:
        rip=requests.POST.get('ip')
        rlocation=requests.POST.get('location')
        check=Rpi.objects.filter(ip=rip)
        if check:
            response["message"]="输入了已使用的IP地址"
        else:
            t=timezone.now()
            Rpi.objects.create(ip=rip,location=rlocation,time=t)
            response["status"]=True            
    except Exception as e:
        print(e)
        response["message"]="输入数据错误"
    return JsonResponse(response)

def del_device(requests):
    response={"status":False,"message":None}
    try:
        rip=requests.GET.get('ip')
        Rpi.objects.filter(ip=rip).delete()
        response["status"]=True
    except Exception as e:
        print(e)
    return JsonResponse(response)

def update_device(requests):
    response={"status":False,"message":None}
    try:
        rip=requests.POST.get('ip')
        rlocation=requests.POST.get('location')
        raw=requests.POST.get('raw')
        p=Rpi.objects.filter(ip=raw)
        if p:
            p.update(ip=rip,location=rlocation)
            response["status"]=True
        else:
            response["message"]="输入错误的蓝牙地址"
    except Exception as e:
        print(e)
        response["message"]="输入数据错误"
    return JsonResponse(response)

def change_status(requests):
    try:
        rid=requests.POST.get('id')
        rstatus=requests.POST.get('status')
        if rstatus=="true":
            p=Person.objects.filter(ble_mac=rid).update(ignore=False)
        else:
            p=Person.objects.filter(ble_mac=rid).update(ignore=True)

    except Exception as e:
        print(e)
    return

def android_person_info(requests):
    start=timezone.now()-datetime.timedelta(minutes=1)
    State.objects.filter(time__lt=start).update(move_flag=4)
    abnormal_state=State.objects.filter(move_flag__gt=0,person__ignore=False)
    rp=[]
    for s in State.objects.all():
        rp.append(s.toJson())
    # print(rp)
    # return JsonResponse(rp) 
    return HttpResponse(json.dumps(rp),content_type="application/json")

def rpi_post(requests):
    global FRESH
    response={"status":False}
    post=requests.POST.keys()[0]
    post=json.loads(post)
    try:
        ip=post['ip']
        id=post['id']
        status=post['status']
        # print(ip,id)
        p=Person.objects.get(ble_mac=id)
	r=Rpi.objects.get(ip=ip)
	#print(p)
        # t=datetime.datetime.now()+datetime.timedelta(hours=8)
        t=timezone.now()
	if len(State.objects.filter(person=p))==0:
	    State.objects.create(person=p,rpi=r,move_flag=status,time=t)
	else:
            State.objects.filter(person=p).update(move_flag=status,time=t,rpi=r)
        response["status"]=True
        if FRESH==True:
            FRESH=False
            updateTagList()
            # response["update"]=True
            # response["data"]=TAG_LIST
    except Exception as e:
        print(e)
    # print(response)
    return HttpResponse(json.dumps(response),content_type="application/json")

def get_taglist(requests):
    global FRESH
    ip=requests.POST.keys()[0]
    try:
    	r=Rpi.objects.filter(ip=ip)
	if r:
	    r.update(time=timezone.now())
    except Exception as e:
	print(e)
#    if len(TAG_LIST)==0 or FRESH==True:
#        updateTagList()
#        FRESH=False
    # print(json.dumps(TAG_LIST))
#    print(TAG_LIST)
    l=updateTagList()
    return HttpResponse(json.dumps(l),content_type="application/json")
