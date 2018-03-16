import pymysql
import datetime

class DataBaseManager:
    def __init__(self, host, user, password, database):
        self.db = pymysql.connect(host=host, user=user, password=password, db=database)
        self.cursor = self.db.cursor()
        self.user_count = 0
        self.sensor_count = 0

    def insert_user(self, name, sex, birthday):
        self.user_count += 1
        sql = "INSERT INTO users(id, user_name, sex, birthday) VALUES (" \
              + str(self.user_count + 1000) + ", '" + name + "' , '" + sex + "' , '" + birthday + "' )"
        self.cursor.execute(sql)
        self.db.commit()

    def insert_sensor(self, mac_addr, host_id, status):
        self.sensor_count += 1
        sql = "INSERT INTO sensors(id, mac_addr, host_id, status) VALUES (" \
              + str(self.user_count + 2000) + ", '" + mac_addr + "'," + host_id + "," + status + ")"
        self.cursor.execute(sql)
        self.db.commit()

    def insert_sensordata(self, data_format):
        sql = "INSERT INTO info_sensortag(light,  \
               acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z, magn_x, magn_y, magn_z,person_id,rpi_id,time) VALUES\
               (%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,\'%s\',\'%s\',now());" % (data_format[0],data_format[1],data_format[2],data_format[3],\
               data_format[4],data_format[5],data_format[6],data_format[7],data_format[8],data_format[9],data_format[10],\
               data_format[11])
        self.cursor.execute(sql)
        self.db.commit()

    def insert_state(self,data):
        '''sql="insert into info_state(move_flag,person_id,rpi_id,time) values(%d,\'%s\',\'%s\',now()) on duplicate key update move_flag=%d\
        ,rpi_id=\'%s\',time=now();" % (data[0],data[1],data[2],data[0],data[2],data[1]) '''
        #print(sql)
        sql="replace into info_state(move_flag,person_id,rpi_id,time) values(%d,\'%s\',\'%s\',now());" % (data[0],data[1],data[2])
        self.cursor.execute(sql)
        self.db.commit()
    
    def insert_heartbeat(self,data):
        sql="replace into info_heartbeat(rpi_id,flag,time) values(\'%s\',0,now());" % (data)
        # print(sql)
        self.cursor.execute(sql)
        self.db.commit()
