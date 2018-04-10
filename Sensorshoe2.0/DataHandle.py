#-*- coding: UTF-8 -*-
import numpy as np

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

    def add_gyro(self, tag_index, data):
        self.tags[tag_index].add_gyro(data)

    def set_address(self,tag_index,address):
        self.tags[tag_index].set_address(address)
    
    def set_fresh(self,tag_index,flag):
        self.tags[tag_index].fresh=flag

    def get_address(self,tag_index):
        return self.tags[tag_index].get_address()

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

        self.data_list = [[] for row in range(4)]
        self.delta_present = [0 for i in range(4)]
        self.mean = [0 for i in range(4)]
        self.variance = [0 for i in range(4)]

        self.status = 0

        # 报警音乐播放标志位
        self.alert_on_flag = False

        self.fresh=False

    def get_id(self):
        return self.tag_mac

    def add_lux(self, data):
        self.current_lux = data
        self.data_list[0].append(data)
        if len(self.data_list[0]) > MAX_WINDOW_SIZE:
            del self.data_list[0][0]

    def add_gyro(self, data):
        self.current_gyro = data
        for i in range(1, 4):
            self.data_list[i].append(data[i-1])
            if len(self.data_list[i]) > MAX_WINDOW_SIZE:
                del self.data_list[i][0]

    def set_fresh(self,flag):
        self.fresh=flag
    
    def is_fresh(self):
        return self.fresh

    def set_address(self,address):
        self.address=address
    
    def get_address(self):
        return self.address

    def get_status(self):
        lux_flag = False
        motion_flag = False
        count = 0
        for i in range(1, 4):
            if self.variance[i] > 20.0:
                count += 1
        if count >= 1:
            motion_flag = True
        print(self.tag_mac + " motion count : " + str(count))
        # print(self.data_list)
        # print(self.mean)
        # print(self.variance)
        if (self.variance[0] > 40.0 and self.delta_present[0] > 20.0) or self.mean[0] > 30.0:
            lux_flag = True
        if self.night_flag:
            if lux_flag:
                if motion_flag:
                    return 3
                else:
                    return 2
            else:
                if motion_flag:
                    return 1
                else:
                    return 0
        else:
            if motion_flag:
                return 1
            else:
                return 0

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


if __name__=="__main__":
    winsound.PlaySound(".\\alert.wav", winsound.SND_ALIAS)