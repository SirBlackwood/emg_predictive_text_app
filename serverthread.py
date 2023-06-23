from PyQt6.QtCore import QThread, pyqtSignal
import time
import random
from keras.models import load_model
import numpy as np
import socket
import pickle
import warnings
from sklearn.exceptions import DataConversionWarning
warnings.filterwarnings(action='ignore', category=DataConversionWarning)


class ServerThread(QThread):
    data_received = pyqtSignal(str)  # Сигнал для передачи полученных данных

    def __init__(self):
        super().__init__()
        self.model = load_model('model.h5')
        self.PORT = 3000
        self.HOST = '192.168.31.91'
        self.coe = np.loadtxt('filter.txt')
        self.TRANSPORT_BLOCK_HEADER_SIZE = 16
        self.SAMPLES_PER_TRANSPORT_BLOCK = 64
        self.TCP_PACKET_SIZE = (self.TRANSPORT_BLOCK_HEADER_SIZE // 4 + self.SAMPLES_PER_TRANSPORT_BLOCK) * 4
        self.samp = np.zeros(2000)
        self.k = 0.0000228
        self.temp = np.zeros(2000)
        self.dataframes = 0
        self.data = bytearray(2048)
        self.samples = np.array([])

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.HOST, self.PORT))
            while True:
                data = s.recv(272)
                # если данные не получены, завершаем цикл
                if not data:
                    break
                for sample in range(16, 272, 4):
                    ins = np.array([int.from_bytes(data[sample:sample + 4], byteorder='little', signed=True)])
                    self.samples = np.append(self.samples, ins)
                    if len(self.samples) == 2001:
                        self.samples = np.delete(self.samples, 0)

                if len(self.samples) == 2000:
                    for i in range(2000):
                        self.temp[i] = self.samples[i]
                    mean = np.mean(self.samples)
                    self.temp -= mean
                    self.temp *= self.k
                    self.temp = np.convolve(self.temp, self.coe, "same")
                    maxid = np.argmax(self.temp)
                    if 1 >= self.temp[maxid] >= 0.05:
                        if 968 <= maxid <= 1032:
                            for i in range(2000):
                                self.samp[i] = self.temp[i]
                            self.data_received.emit(self.predict(
                                self.temp.reshape(1, 2000)
                            ))
            # Получение данных с сервера

            # data = self.get_data_from_server()
            #
            # # Отправка данных через сигнал
            # self.data_received.emit(data)
            #
            # # Пауза между запросами к серверу
            # time.sleep(1)

    def predict(self, signal):
        result = self.model.predict(signal.reshape(1, 2000))
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            lb = pickle.loads(open("lb.pickle", "rb").read())
            result = result.argmax(axis=1)[0]
            res = lb.classes_[result]
            print(res)
            return res

    # def get_data_from_server(self):
    #     return str(random.randint(0, 2))
