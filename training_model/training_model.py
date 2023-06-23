import matplotlib.pyplot as plt
import random
import numpy as np
import math
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
from sklearn.metrics import classification_report, confusion_matrix
from keras.models import Sequential
from keras.layers import Dense, Conv1D, MaxPooling1D, Dropout, GlobalAveragePooling1D, Reshape, Conv2D, MaxPooling2D, GlobalAveragePooling2D, Flatten
from keras.optimizers import SGD, Adam
import seaborn as sn
import tensorflow as tf
import pickle
import os

def get_dataset(dataset_path="/content/emg_datasets/full_dataset"):
  data = []
  labels = []
  muap_paths = []
  for folder in os.listdir(dataset_path):
      for muap_path in os.listdir("{}/{}".format(dataset_path, folder)):
          path = "{}/{}/{}".format(dataset_path, folder, muap_path)
          muap_paths.append(path)
  random.seed(42)
  random.shuffle(muap_paths)
  for muap_path in muap_paths:
      muap = np.loadtxt(muap_path)
      data.append(muap)
      label = muap_path.split(os.path.sep)[-2]
      labels.append(label)
  data = np.asarray(data, dtype=np.float32)
  labels = np.asarray(labels)
  return data, labels

signals, actions = get_dataset("/content/emg_datasets/moves")
signals, actions = signals[:,:], actions[:]

tmp = np.sum(np.abs(signals), axis=1)
signals = np.delete(signals, tmp > 50, axis=0)
actions = np.delete(actions, tmp > 50, axis=0)

(trainX, testX, trainY, testY) = train_test_split(signals, actions, test_size=0.25, random_state=42)
lb = LabelBinarizer()
trainY = lb.fit_transform(trainY)
testY = lb.transform(testY)
num_classes = 4
num_sensors = 1
print(trainY)
input_size = trainX.shape[1]
model = Sequential()
model.add(Reshape((input_size, num_sensors), input_shape=(input_size,)))
model.add(Conv1D(40, 200, activation='relu', input_shape=(input_size, num_sensors)))
model.add(Conv1D(25, 10, activation='relu'))
model.add(MaxPooling1D(4))
model.add(Conv1D(100, 10, activation='relu'))
model.add(Conv1D(50, 10, activation='relu'))
model.add(MaxPooling1D(4))
model.add(Dropout(0.5))
model.add(Conv1D(100, 10, activation='relu'))
model.add(GlobalAveragePooling1D())
model.add(Dense(num_classes, activation='softmax'))

EPOCHS = 500

print(model.summary())

model.compile(loss='categorical_crossentropy',
              optimizer=Adam(5e-5), metrics=['accuracy'])
H = model.fit(trainX, trainY,
                    epochs=EPOCHS,
                    validation_data=(testX, testY),
                    )
