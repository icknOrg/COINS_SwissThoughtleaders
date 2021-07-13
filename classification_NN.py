# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 16:22:44 2021

@author: Johanna
"""

from create_class_dataframe import get_class_original
from create_class_dataframe_DE import get_Test_DE
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
import tensorflow as tf

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


data = get_class_original()

train = data.drop(columns=['m/w', 'Bereich', 'Wikipedia', 'id', 'Twitter Verifiziert?', 'Wikipedia_name', 'Twitter_score', 'Wikipedia_score', 'GSR_score', 'Thoughtleader_Score'])

labels=train['class_labels']
features = train.iloc[:,1:20]

X=features

y=np.ravel(labels)

# split into 40% and 60% training and testing data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)

# normalize data 
scaler = StandardScaler().fit(X_train)

X_train = scaler.transform(X_train)

X_test = scaler.transform(X_test)

# first implementation is with
# loss function: binary crossentropy 
# activation function: relu and sigmoid 
# optimizer: Stochastic Gradient Descent 

model = Sequential()

model.add(Dense(8, activation='relu', input_shape=(19,)))

model.add(Dense(8, activation='relu'))

model.add(Dense(1, activation='sigmoid'))


model.compile(loss='binary_crossentropy',
              optimizer='sgd',
              metrics=['accuracy'])
                   
model.fit(X_train, y_train,epochs=6, batch_size=1, verbose=1)

# evaluate the model on original loaded data 
y_pred = model.predict(X_test)

score = model.evaluate(X_test, y_test,verbose=1)

print(score)

# load data from German persons for prediction

test = get_Test_DE();

test = test.drop(columns=['m/w', 'Bereich', 'Wikipedia', 'id', 'Twitter Verifiziert?', 'Wikipedia_name'])

test_features = test.iloc[:,1:20]

Q = test_features

Q_test = scaler.transform(Q)

q_pred = model.predict(Q_test)

























