#-*- coding: UTF-8 -*-
import socket
import time
import threading
from DataHandle import *
import csv
import os
from DataBaseManager import DataBaseManager
#SERVER_IP = "192.168.1.103"
#SERVER_IP="localhost"
#SERVER_IP=socket.gethostbyname(socket.gethostname())
SERVER_IP="192.168.0.3"
SERVER_PORT = 9999
MAX_LINKS = 5

tag_manager = TagManager()
# server端记录所有tag的mac地址，对应index
tag_dict = {}
alert_on_flag=False


database=DataBaseManager('127.0.0.1','root','111','ishoe')
database2=DataBaseManager('127.0.0.1','root','111','ishoe')
database3=DataBaseManager('127.0.0.1','root','111','ishoe')
def handle_data(sock, addr):
    sock.settimeout(30)
    while True:
        try:
            data = sock.recv(2048)
            if len(data) == 0:
                print("break")
                break
            database3.insert_heartbeat(addr[0])
            if len(data) > 20:
                try:
                    data = eval(data)
                except Exception:
                    continue
                for key in data:
                    if key not in tag_dict:
                        tag_dict[key] = len(tag_dict)
                        tag_manager.add_tags(key)
                        tag_manager.set_address(tag_dict[key],addr[0])
                    if data[key]['lightmeter'] and data[key]['gyroscope']:
                        tag_manager.set_fresh(tag_dict[key],True)
                        tag_manager.add_lux(tag_dict[key], float(data[key]['lightmeter']))
                        gyro = [float(x) for x in data[key]['gyroscope']]
                        acc = [float(x) for x in data[key]['accelerometer']] if data[key]['accelerometer'] else [-10,-10,-10]
                        magn = [float(x) for x in data[key]['magnetometer']] if data[key]['magnetometer'] else [-10,-10,-10]
                        total = [float(data[key]['lightmeter'])]
                        total.extend(acc)
                        total.extend(gyro)
                        total.extend(magn)
                        total.append(key)
                        total.append(addr[0])

                        database.insert_sensordata(total)
                        
                        tag_manager.add_gyro(tag_dict[key], gyro)
            #print(data)
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
        t = threading.Thread(target=handle_data, args=(sock, addr))
        t.start()
    server.close()


def check():
    while True:
        time.sleep(0.4)
        for tag in tag_manager.tags:
            if tag.is_fresh()==False:
                continue
            if len(tag.data_list[0]) > 2 and len(tag.data_list[1]) > 2:
                tag.init_flag = True
            if tag.init_flag:
                tag.delta_present[0] = tag.current_lux - tag.data_list[0][-1]
                tag.mean[0] = tag.get_mean(0)
                tag.variance[0] = tag.get_variance(0)
                for i in range(1, 4):
                    tag.delta_present[i] = tag.current_gyro[i - 1] - tag.data_list[i][-1]
                    tag.mean[i] = tag.get_mean(i)
                    tag.variance[i] = tag.get_variance(i)
            '''move_flag=0
            if tag.get_status()>0:
                move_flag=1'''
            database2.insert_state([tag.get_status(),tag.get_id(),tag.get_address()])
            tag.set_fresh(False)


if __name__ == "__main__":
    t_check = threading.Thread(target=check)
    t_check.start()
    serve()

