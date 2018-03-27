import pymysql
import datetime
import time
from DBUtils.PooledDB import PooledDB

class DataBaseManager:
    def __init__(self):
        self.pool=PooledDB(pymysql,10,host='127.0.0.1',user='root',passwd='111',db='ishoe',charset='utf8')

        # self.db = pymysql.connect(host=host, user=user, password=password, db=database)
        # self.cursor = self.db.cursor()
        # self.user_count = 0
        # self.sensor_count = 0

    def insert_sensordata(self, data_format):
        sql = "INSERT INTO info_sensortag(light,  \
               acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z, magn_x, magn_y, magn_z,person_id,rpi_id,time) VALUES\
               (%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,\'%s\',\'%s\',\'%s\');" % (data_format[0],data_format[1],data_format[2],data_format[3],\
               data_format[4],data_format[5],data_format[6],data_format[7],data_format[8],data_format[9],data_format[10],\
               data_format[11],data_format[12])
        try:
            conn=self.pool.connection()
            cur=conn.cursor()
            cur.execute(sql)
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            #print(e)
            pass
            


    def insert_state(self,data):
        '''sql="insert into info_state(move_flag,person_id,rpi_id,time) values(%d,\'%s\',\'%s\',now()) on duplicate key update move_flag=%d\
        ,rpi_id=\'%s\',time=now();" % (data[0],data[1],data[2],data[0],data[2],data[1]) '''
        #print(sql)
        sql="replace into info_state(move_flag,person_id,rpi_id,time) values(%d,\'%s\',\'%s\',now());" % (data[0],data[1],data[2])
        try:
            conn=self.pool.connection()
            cur=conn.cursor()
            cur.execute(sql)
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(e)
            pass
    
    def insert_heartbeat(self,data):
        sql="update info_rpi set time=now() where ip=\'%s\';" % (data)
        # print(sql)
        try:
            conn=self.pool.connection()
            cur=conn.cursor()
            cur.execute(sql)
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            # print(e)
            pass

    def select_tags(self):
        sql="select ble_mac from info_person;"
        result=None
        try:
            conn=self.pool.connection()
            cur=conn.cursor()
            cur.execute(sql)
            result=cur.fetchall()
            cur.close()
            conn.close()
        except Exception as e:
            pass
        return result

    def select_rpi(self):
        sql="select ip from info_rpi;"
        try:
            conn=self.pool.connection()
            cur=conn.cursor()
            cur.execute(sql)
            result=cur.fetchall()
            cur.close()
            conn.close()
        except Exception as e:
            pass
        r=[]
        if result:
            for i in result:
                r.append(i[0])
        return r
