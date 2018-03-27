#-*- coding: UTF-8 -*-
import numpy as np
import GaitDetection as GD

DATA_LENGTH = 60
MAX_WINDOW_SIZE = 10


class TagManager:
    def __init__(self):
        self.num_of_PI = 0
        self.num_of_tag = 0
        # Wonder if needed, sum the tags_of_each_PI up, should equal to num_of_tag
        self.tags_of_each_PI = []
        # The list of TagHandlers
        self.tags = []

    def add_tags(self, mac_address):
        self.num_of_PI += 1
        self.tags.append(TagHandler(mac_address))

    def add_lux(self, tag_index, data):
        self.tags[tag_index].add_lux(data)

    def add_acc(self, tag_index, data):
        self.tags[tag_index].add_acc(data)

    def add_gyro(self, tag_index, data):
        self.tags[tag_index].add_gyro(data)

    def set_address(self, tag_index, address):
        self.tags[tag_index].set_address(address)

    def set_fresh(self, tag_index, flag):
        self.tags[tag_index].fresh = flag

    def gait_detect(self, tag_index):
        self.tags[tag_index].gait_detect()

    def set_night_flag(self, flag):
        # print("flag", flag)
        for tag in self.tags:
            tag.night_flag = flag
        #self.tags[tag_index].night_flag = flag


class TagHandler:
    def __init__(self, mac_address):
        self.tag_mac = mac_address
        self.init_flag = False
        # 白天黑夜标志位
        self.night_flag = False
        self.lux_flag = True
        self.motion_flag = False

        self.current_lux = None
        self.current_acc = None
        self.current_gyro = None
        self.current_mag = None

        self.acc_data = np.zeros((DATA_LENGTH, 3))
        self.gyro_data = np.zeros((DATA_LENGTH, 3))
        self.lux_data = np.zeros(DATA_LENGTH)

        # self.data_list = [[] for row in range(4)]

        self.delta_present = [0 for i in range(7)]

        self.mean = [0 for i in range(7)]
        self.variance = [0 for i in range(7)]

        self.status = 0

        # 报警音乐播放标志位
        self.alert_on_flag = False

        self.fresh = False

        # 步态
        self.gait_detection = GD.GaitDetection(DATA_LENGTH, 3, 100)

    def set_address(self,data):
        self.address=data

    def get_address(self):
        return self.address

    def get_mac_address(self):
        return self.tag_mac

    def get_id(self):
        return self.tag_mac

    def set_fresh(self, flag):
        self.fresh = flag

    def is_fresh(self):
        return self.fresh

    def add_lux(self, data):
        if self.current_lux is not None:
            self.delta_present[0] = data - self.current_lux
        self.current_lux = data

        self.lux_data = np.delete(self.lux_data, 0, axis=0)
        self.lux_data = np.append(self.lux_data, self.current_lux)
        

    def add_acc(self, data):
        if self.current_acc is not None:
            for i in range(1, 4):
                self.delta_present[i] = data[i - 1] - self.current_acc[i - 1]
        self.current_acc = data
        self.gait_detection.add_acc(data)
        self.acc_data = np.delete(self.acc_data, 0, axis=0)
        self.acc_data = np.row_stack((self.acc_data, data))
        

    def add_gyro(self, data):
        if self.current_gyro is not None:
            for i in range(1, 4):
                self.delta_present[i] = data[i - 1] - self.current_gyro[i - 1]
        self.current_gyro = data
        self.gait_detection.add_gyro(data)
        self.gyro_data = np.delete(self.gyro_data, 0, axis=0)
        self.gyro_data = np.row_stack((self.gyro_data, data))

    def get_status(self):
        lux_flag = False
        motion_flag = False
        count = 0
        for i in range(4, 7):
            if self.variance[i] > 25.0 or self.delta_present[i] > 30:
                count += 1
        if count >= 1:
            motion_flag = True

        if (self.variance[0] > 40.0 and self.delta_present[0] > 20.0) or self.mean[0] > 30.0:
            lux_flag = True

        gait_flag = self.gait_detection.get_gait_flag()

        print(self.tag_mac + " motion count : " + str(count))
        print("mean:" + str(self.mean))
        print("variance:" + str(self.variance))
        print('gait_flag:' + str(gait_flag))
        print('\n')

        if self.night_flag:
            if lux_flag:
                if motion_flag and gait_flag:
                    return 3
                else:
                    return 2
            else:
                if motion_flag and gait_flag:
                    return 1
                else:
                    return 0
        else:
            if motion_flag and gait_flag:
                return 1
            else:
                return 0

    def calculate_mean_variance(self):
        self.mean[0] = np.mean(self.lux_data)
        self.mean[1: 4] = np.mean(self.acc_data, axis=0)
        self.mean[4: 7] = np.mean(self.gyro_data, axis=0)
        self.variance[0] = np.var(self.lux_data)
        self.variance[1: 4] = np.var(self.acc_data, axis=0)
        self.variance[4: 7] = np.var(self.gyro_data, axis=0)

    def gait_detect(self):
        self.gait_detection.gait_detect()

    def get_mean(self, index):
        m = 0.0
        count = 0
        for i in range(len(self.data_list[index])):
            m += self.data_list[index][i]
            count += 1
        if count > 0:
            m = m / count
        return m

    def get_variance(self, index):
        v = 0.0
        size = len(self.data_list[index])
        for i in range(size):
            v += (self.data_list[index][i] - self.mean[index]) * (self.data_list[index][i] - self.mean[index])
        return v / size
