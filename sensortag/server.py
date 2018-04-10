#-*- coding: UTF-8 -*-



# select * from test_info   

# into outfile '/tmp/test.csv'   

# fields terminated by ','　


import socket
import time
import threading
from DataHandle import *
import csv
import os
from DataBaseManager import DataBaseManager
import json
#SERVER_IP = "192.168.1.103"
#SERVER_IP="localhost"
#SERVER_IP=socket.gethostbyname(socket.gethostname())
SERVER_IP="172.16.252.248"
SERVER_PORT = 9999
MAX_LINKS = 5

tag_manager = TagManager()
# server端记录所有tag的mac地址，对应index
tag_dict = {}
alert_on_flag=False

database=DataBaseManager()
def handle_data(sock, addr):
    sock.settimeout(60)
    threading.Thread(target=getTags,args=[sock]).start()
    while True:
        try:
            data = sock.recv(1024)
            #print(time.time()-current)   
            if len(data) == 0:
                print("break")
                break
            #database.insert_heartbeat(addr[0])
            if len(data) > 20:
                try:
                    data = json.loads(data)
                    # print(data)
                except Exception:
                    continue
                if data['id']==None or len(data['magnet'])==0 or len(data['gyro'])==0 or len(data['accel'])==0 or len(data['lux'])==0:
                    # print(data)
                    continue
                key=data['id'] 
                if key not in tag_dict:
                    tag_dict[key] = len(tag_dict)
                    tag_manager.add_tags(key)
                    tag_manager.set_address(tag_dict[key],addr[0])
                tag_manager.set_fresh(tag_dict[key], True)
                lux = data['lux']['v']
                gyro = [data['gyro']['x'], data['gyro']['y'], data['gyro']['z']]
                acc = [data['accel']['x'], data['accel']['y'], data['accel']['z']]
                magn = [data['magnet']['x'], data['magnet']['y'], data['magnet']['z']]
                total = [lux]
                total.extend(acc)
                total.extend(gyro)
                total.extend(magn)
                total.append(key)
                total.append(addr[0])
                total.append(str(data['time']))
                # database.insert_sensordata(total)
                threading.Thread(target=database.insert_sensordata, args=[total]).start()
                tag_manager.add_lux(tag_dict[key], lux)                
                tag_manager.add_acc(tag_dict[key], acc)
                tag_manager.add_gyro(tag_dict[key], gyro)
                tag_manager.gait_detect(tag_dict[key])

            else:
                threading.Thread(target=database.insert_heartbeat,args=[addr[0]]).start()
                # print(data)
        except socket.timeout as e:
            print("break")
            break
    sock.close()


def serve():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_IP, SERVER_PORT))
    server.listen(MAX_LINKS)
    print(SERVER_IP, SERVER_PORT)
    while True:
        sock, addr = server.accept()
	print(addr)
        list=database.select_rpi()
        sock.send("ssss")
	# print(list)
        if addr[0] in list:
            t = threading.Thread(target=handle_data, args=(sock, addr))
            t.start()
        else:
            sock.close()
    server.close()

def getTags(sock):
    while True:
        tags=database.select_tags()
        # print(tags)
        if tags:
            try:
                sock.send(json.dumps(tags))
            except:
                pass
        time.sleep(30)
        

def check():
    time.sleep(5)
    while True:
        time.sleep(0.5)
        for tag in tag_manager.tags:
            if tag.is_fresh() == False:
                continue
            # if len(tag.data_list[0]) > 2 and len(tag.data_list[1]) > 2:
            #     tag.init_flag = True
            # if tag.init_flag:
            tag.calculate_mean_variance()

            '''move_flag=0
            if tag.get_status()>0:
                move_flag=1'''
            # database.insert_state([tag.get_status(),tag.get_id(),tag.get_address()])
            print('check')
            threading.Thread(target=database.insert_state,args=[[tag.get_status(),tag.get_id(),tag.get_address()]]).start()
            tag.set_fresh(False)


if __name__ == "__main__":
    t_check = threading.Thread(target=check)
    t_check.start()
    serve()

