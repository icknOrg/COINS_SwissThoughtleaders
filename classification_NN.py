# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 16:22:44 2021

@author: Johanna
"""

from create_classification_df import get_class_original_SW
import pandas as pd
from keras.models import Sequential
from sklearn.model_selection import GridSearchCV
from keras.wrappers.scikit_learn import KerasClassifier
from keras.layers import Dense
import tensorflow as tf

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


data = get_class_original_SW()

train = data.drop(columns=['m/w', 'Bereich', 'Wikipedia', 'id', 'Twitter Verifiziert?', 'Unnamed: 7','Wikipedia_name', 'Twitter_score', 'Wikipedia_score_x',  'Wikipedia_score_y', 'GSR_score', 'Thoughtleader_Score'])

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

def create_model():
    model = Sequential()
    
    model.add(Dense(8, activation='relu', input_shape=(19,)))
    
    model.add(Dense(8, activation='relu'))
    
    model.add(Dense(1, activation='sigmoid'))
    
    
    model.compile(loss='binary_crossentropy',
                  optimizer='sgd',
                  metrics=['accuracy'])
    
    return model

#create model
model = KerasClassifier(build_fn=create_model, verbose=0)

# summarize results
def print_summary(grid_result):
    print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
    means = grid_result.cv_results_['mean_test_score']
    stds = grid_result.cv_results_['std_test_score']
    params = grid_result.cv_results_['params']
    for mean, stdev, param in zip(means, stds, params):
        print("%f (%f) with: %r" % (mean, stdev, param))

# define the grid search parameters
batch_size = [1, 3, 5, 7, 9, 12]
epochs = [5, 10, 20]
param_grid = dict(batch_size=batch_size, epochs=epochs)
grid = GridSearchCV(estimator=model, param_grid=param_grid, n_jobs=-1, cv=3)
grid_result = grid.fit(X_train, y_train)
print_summary(grid_result)

# define grid search for the best optimizer

def create_model_opt(optimizer='sgd'):
    model = Sequential()
    
    model.add(Dense(8, activation='relu', input_shape=(19,)))
    
    model.add(Dense(8, activation='relu'))
    
    model.add(Dense(1, activation='sigmoid'))
    
    
    model.compile(loss='binary_crossentropy',
                  optimizer=optimizer,
                  metrics=['accuracy'])
    
    return model

model_opt = KerasClassifier(build_fn=create_model_opt, epochs=20, batch_size=1, verbose=0)

# define the grid search parameters
optimizer = ['SGD', 'RMSprop', 'Adagrad', 'Adadelta', 'Adam', 'Adamax', 'Nadam']
param_grid = dict(optimizer=optimizer)
grid = GridSearchCV(estimator=model_opt, param_grid=param_grid, n_jobs=-1, cv=3)
grid_result = grid.fit(X_train, y_train)
print_summary(grid_result)












# model.fit(X_train, y_train,epochs=6, batch_size=1, verbose=1)

# # evaluate the model on original loaded data 
# y_pred = model.predict(X_test)

# score = model.evaluate(X_test, y_test,verbose=1)

# print(score)

# load data from German persons for prediction

# test = get_Test_DE();

# test = test.drop(columns=['m/w', 'Bereich', 'Wikipedia', 'id', 'Twitter Verifiziert?', 'Wikipedia_name'])

# test_features = test.iloc[:,1:20]

# Q = test_features

# Q_test = scaler.transform(Q)

# q_pred = model.predict(Q_test)

























