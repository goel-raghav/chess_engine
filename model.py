#  # -*- coding: utf-8 -*-
# """
# Created on Sat Feb  3 19:02:21 2024

# @author: 898796
# """
from keras import models
from keras import layers
from keras import callbacks
from keras import regularizers
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn import preprocessing

physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)

with np.load("data_elo_transform_board.npz") as data:
    x = data['x'][:200_000]
    y = data['y'][:200_000].reshape(-1, 1)


y = preprocessing.normalize(y)
print(len(x))




X_train, X_test, y_train, y_test = train_test_split(x, y, test_size= .1)

callback = callbacks.EarlyStopping(monitor='val_mae',
                              min_delta=0,
                              patience=5,
                              verbose=0, mode='auto', restore_best_weights=True)


network = models.Sequential()

# network.add(layers.Conv2D(256, (3, 3), activation="relu", input_shape=(8, 8, 1), padding="same"))
# network.add(layers.BatchNormalization())
# network.add(layers.Dropout(.1))

# network.add(layers.Conv2D(256, (3, 3), activation="relu", padding="same"))
# network.add(layers.BatchNormalization())
# network.add(layers.Dropout(.1))

# network.add(layers.Conv2D(256, (5, 5), activation="relu"))
# network.add(layers.BatchNormalization())
# network.add(layers.Dropout(.1))

network.add(layers.Flatten(input_shape=(8, 8, 1)))

network.add(layers.Dense(128, activation="relu"))
network.add(layers.BatchNormalization())
network.add(layers.Dropout(.5))

network.add(layers.Dense(128, activation="relu"))
network.add(layers.BatchNormalization())
network.add(layers.Dropout(.5))

network.add(layers.Dense(1, activation='tanh'))
network.compile(optimizer = 'adam',
loss='mse',
metrics=['mse', 'mae'])


network.fit(X_train, y_train, epochs=10
                , batch_size=256, validation_data=(X_test, y_test), callbacks=[callback])



network.save("tan_h.keras")
