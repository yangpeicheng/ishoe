#-*- coding: UTF-8 -*-
import numpy as np
from scipy.fftpack import fft
from scipy.signal import savgol_filter
from scipy import signal


class GaitDetection:
    def __init__(self, length, width, correlation_length):
        self.frequency = 10
        self.data_length = length
        self.data_width = width
        self.acc = np.zeros((self.data_length, self.data_width))
        self.gyro = np.zeros((self.data_length, self.data_width))
        self.acc_diff = np.zeros((self.data_length, self.data_width))
        self.gyro_diff = np.zeros((self.data_length, self.data_width))
        self.slope = np.zeros((self.data_length, self.data_width))
        self.step_mark = np.zeros(self.data_length)

        self.acc_correlation = np.zeros((correlation_length, width))
        self.gyro_correlation = np.zeros((correlation_length, width))
        self.correlation_length = correlation_length

        # Gait Detect
        self.gait_status = 0
        self.gait_count = 0

        self.gait_flag = False

    def add_acc(self, d):
        self.acc = np.delete(self.acc, 0, axis=0)
        self.acc = np.row_stack((self.acc, d))

    def add_gyro(self, d):
        self.gyro = np.delete(self.gyro, 0, axis=0)
        self.gyro = np.row_stack((self.gyro, d))

    def set_frequency(self, f):
        self.frequency = f

    def get_gait_flag(self):
        print('\n')
        print(self.acc_diff[:,0])
        print(self.slope)
        return self.gait_flag

    @staticmethod
    def butter_bandpass(low_cut, high_cut, fs, order=5):
        nyq = 0.5 * fs
        low = low_cut / nyq
        high = high_cut / nyq
        b, a = signal.butter(order, [low, high], btype='bandpass')
        return b, a

    @staticmethod
    def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
        b, a = GaitDetection.butter_bandpass(lowcut, highcut, fs, order=order)
        y = signal.lfilter(b, a, data)
        return y

    def derivative_operator(self):
        for i in range(4, self.data_length):
            self.acc_diff[i, :] = 0.125 * (2 * self.acc[i, :] + self.acc[i - 1, :]
                                           - self.acc[i - 3, :] - 2 * self.acc[i - 4, :])
            self.gyro_diff[i, :] = 0.125 * (2 * self.gyro[i, :] + self.gyro[i - 1, :]
                                            - self.gyro[i - 3, :] - 2 * self.gyro[i - 4, :])

    def derivative_current(self):
        temp = 0.125 * (2 * self.acc[-1, :] + self.acc[-2, :] - self.acc[-4, :] - 2 * self.acc[-5, :])
        self.acc_diff = np.delete(self.acc_diff, 0, axis=0)
        self.acc_diff = np.row_stack((self.acc_diff, temp))
        temp = 0.125 * (2 * self.gyro[-1, :] + self.gyro[-2, :] - self.gyro[-4, :] - 2 * self.gyro[-5, :])
        self.gyro_diff = np.delete(self.gyro_diff, 0, axis=0)
        self.gyro_diff = np.row_stack((self.gyro_diff, temp))

    def correlation(self, window_length):
        for delay in range(0, self.correlation_length):
            for i in range(0, self.data_width):
                if (delay + window_length) >= self.data_length:
                    break
                self.acc_correlation[delay, i] = np.corrcoef(self.acc[0:window_length, i],
                                                             self.acc[delay:delay + window_length, i])[0, 1]
                self.gyro_correlation[delay, i] = np.corrcoef(self.gyro[0:window_length, i],
                                                              self.gyro[delay:delay + window_length, i])[0, 1]

    def slope_current(self, threshold):
        temp = np.zeros(self.data_width)
        for i in range(0, self.data_width):
            if self.acc_diff[-1, i] > threshold:
                temp[i] = 1
            elif self.acc_diff[-1, i] < -threshold:
                temp[i] = -1
        self.slope = np.delete(self.slope, 0, axis=0)
        self.slope = np.row_stack((self.slope, temp))

        t = 0
        if self.gait_status == 0:
            if self.slope[-1, 0] == 1:
                self.gait_status = 1
                t = 1
            else:
                self.gait_status = 0
        elif self.gait_status == 1:
            if self.slope[-1, 0] == 1:
                self.gait_status = 1
            elif self.slope[-1, 0] == -1:
                self.gait_status = 2
            else:
                self.gait_status = 3
        elif self.gait_status == 2:
            if self.slope[-1, 0] == -1:
                self.gait_status = 2
            elif self.slope[-1, 0] == 0:
                self.gait_status = 0
                t = -1
            else:
                # 马上遇到正值，此步欠考虑
                self.gait_status = 1
                t = 1
                self.step_mark[-1] = -1
        else:
            if self.slope[-1, 0] == 0:
                self.gait_status = 3
            elif self.slope[-1, 0] == 1:
                self.gait_status = 1
            else:
                self.gait_status = 2

        self.step_mark = np.delete(self.step_mark, 0, axis=0)
        self.step_mark = np.append(self.step_mark, t)

    def slope_step_mark(self, threshold):
        for i in range(0, self.data_length):
            for j in range(0, self.data_width):
                if self.acc_diff[i, j] > threshold:
                    self.slope[i, j] = 1
                elif self.acc_diff[i, j] < -threshold:
                    self.slope[i, j] = -1
        # 判定Step
        status = 0
        for i in range(0, self.data_length):
            if status == 0:
                if self.slope[i, 0] == 1:
                    status = 1
                    self.step_mark[i] = 1
                else:  # 需后续加入考虑
                    status = 0
            elif status == 1:
                if self.slope[i, 0] == 1:
                    status = 1
                elif self.slope[i, 0] == -1:
                    status = 2
                else:
                    status = 3
            elif status == 2:
                if self.slope[i, 0] == -1:
                    status = 2
                elif self.slope[i, 0] == 0:
                    status = 0
                    self.step_mark[i] = -1
                else:
                    # 马上遇到正值，此步欠考虑
                    status = 1
                    self.step_mark[i] = 1
                    self.step_mark[i - 1] = -1
            else:
                if self.slope[i, 0] == 0:
                    status = 3
                elif self.slope[i, 0] == 1:
                    status = 1
                else:
                    status = 2

    def gait_detect(self):
        cor_window_length = 20
        if cor_window_length > self.correlation_length:
            cor_window_length = self.correlation_length

        self.derivative_current()
        self.correlation(cor_window_length)
        self.slope_current(0.3)

        step_count = 0
        for i in range(0, self.data_length):
            if self.step_mark[i] == 1 and step_count % 2 == 0:
                step_count += 1
            elif self.step_mark[i] == -1 and step_count % 2 == 1:
                step_count += 1

        step_count /= 2
        if step_count >= 1:
            self.gait_flag = True
        else:
            self.gait_flag = False


if __name__ == '__main__':
    pass
