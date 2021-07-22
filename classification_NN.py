                               # -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 16:22:44 2021

@author: Johanna

NN Classification 

In the first step some fine tuning is made. The results are already applied in the models later on
so that can be skipped upon running

2 runs are made:
    1 uses the normal create_classification_df
    2 uses the create_classification_all_df
    
    The difference is the prior calculation of the thoughtleader score that defines the applied labels of
    1 a Thoughtleader
    0 no Thoughtleader
    
    first run calculated and normalized the score just for the separated datasets
    second run calculates the score upon the combined data and then separates the datasets again later 
    
    keep in mind that for the second run that is currently applied the normalization of Wikipedia and Twitter
    are in comments right now. If you want to run the first, separated data you have to uncomment those first.
    Also use the correct import in this file. 
    Also keep in mind that models keep training for multiple runs, so either restart kernel or program again
    before running it multiple times.
"""

from create_classification_df import get_class_original_SW
from create_classification_df import get_class_original_DE

#from create_classification_all_df import get_class_original_SW
#from create_classification_all_df import get_class_original_DE

import pandas as pd
from keras.models import Sequential
from sklearn.model_selection import GridSearchCV
from keras.wrappers.scikit_learn import KerasClassifier
from keras.layers import Dense
import tensorflow as tf

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


data_SW = get_class_original_SW()
data_DE = get_class_original_DE()

train = data_SW.drop(columns=['m/w', 'Bereich', 'Wikipedia', 'id', 'Twitter Verifiziert?', 'Unnamed: 7','Wikipedia_name', 'Twitter_score', 'Wikipedia_score_x',  'Wikipedia_score_y', 'GSR_score', 'Thoughtleader_Score'])
predict_DE = data_DE.drop(columns=['m/w', 'Bereich', 'Wikipedia', 'id', 'Twitter Verifiziert?','Wikipedia_name', 'Twitter_score', 'Wikipedia_score_x',  'Wikipedia_score_y', 'GSR_score', 'Thoughtleader_Score'])
predict_SW = data_SW.drop(columns=['m/w', 'Bereich', 'Wikipedia', 'id', 'Twitter Verifiziert?', 'Unnamed: 7','Wikipedia_name', 'Twitter_score', 'Wikipedia_score_x',  'Wikipedia_score_y', 'GSR_score', 'Thoughtleader_Score'])


labels=train['class_labels']
features = train.iloc[:,1:20]

X=features

y=np.ravel(labels)

# split into 30% and 70% training and testing data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# normalize data 
scaler = StandardScaler().fit(X_train)

X_train = scaler.transform(X_train)

X_test = scaler.transform(X_test)

####################################################################################################
# FINE TUNING
####################################################################################################
# before using the actual prediction fine tune the activation function, optimizer, batch size, epochs
# fine tuning was just done with the first Swiss people dataset
# the results from that were used for all predictions 
# the actual models for prediction further below 

def create_model():
    model = Sequential()
    
    model.add(Dense(8, activation='relu', input_shape=(19,)))
    
    model.add(Dense(8, activation='relu'))
    
    model.add(Dense(1, activation='sigmoid'))
    
    
    model.compile(loss='binary_crossentropy',
                  optimizer='Nadam',
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
batch_size = [1, 3, 4, 5, 7]
epochs = [5, 10, 20, 30, 40, 50, 60]
param_grid = dict(batch_size=batch_size, epochs=epochs)
grid = GridSearchCV(estimator=model, param_grid=param_grid, n_jobs=-1, cv=3)
grid_result = grid.fit(X_train, y_train)
print_summary(grid_result)

# define grid search for the best optimizer

def create_model_opt(optimizer='sgd'):
    model = Sequential()
    
    model.add(Dense(8, activation='tanh', input_shape=(19,)))
    
    model.add(Dense(8, activation='tanh'))
    
    model.add(Dense(1, activation='sigmoid'))
    
    
    model.compile(loss='binary_crossentropy',
                  optimizer=optimizer,
                  metrics=['accuracy'])
    
    return model

model_opt = KerasClassifier(build_fn=create_model_opt, epochs=40, batch_size=1, verbose=0)

# define the grid search parameters
optimizer = ['SGD', 'RMSprop', 'Adagrad', 'Adadelta', 'Adam', 'Adamax', 'Nadam']
param_grid = dict(optimizer=optimizer)
grid = GridSearchCV(estimator=model_opt, param_grid=param_grid, n_jobs=-1, cv=3)
grid_result = grid.fit(X_train, y_train)
print_summary(grid_result)

# Function to create model to improve activation function
def create_model_act(activation='relu'):
    model = Sequential()
    
    model.add(Dense(8, activation=activation, input_shape=(19,)))
    
    model.add(Dense(8, activation=activation))
    
    model.add(Dense(1, activation='sigmoid'))
    
    
    model.compile(loss='binary_crossentropy',
                  optimizer='Adamax',
                  metrics=['accuracy'])
    
    return model


# create model
model_act = KerasClassifier(build_fn=create_model_act, epochs=40, batch_size=1, verbose=0)
activation = ['softmax', 'softplus', 'softsign', 'relu', 'tanh', 'sigmoid', 'hard_sigmoid', 'linear']
param_grid = dict(activation=activation)
grid = GridSearchCV(estimator=model_act, param_grid=param_grid, n_jobs=-1, cv=3)
grid_result = grid.fit(X_train, y_train)
print_summary(grid_result)

#################################################################################################################
# train the model with fine tuned parameters on the swiss dataset and predict the German thoughtleaders

def create_model_tuned():
    model = Sequential()
    
    model.add(Dense(8, activation='relu', input_shape=(19,)))
    
    model.add(Dense(8, activation='relu'))
    
    model.add(Dense(8, activation='relu'))
    
    model.add(Dense(1, activation='sigmoid'))
    
    
    model.compile(loss='binary_crossentropy',
                  optimizer='Adamax',
                  metrics=['accuracy'])
    
    return model

#create model
model_SW = KerasClassifier(build_fn=create_model_tuned, epochs=10, batch_size=1, verbose=0)

model_SW.fit(X_train, y_train,epochs=10, batch_size=1, verbose=1)

y_pred = model_SW.predict(X_test)

score_SW = model_SW.score(X_test, y_test,verbose=1)
print("Accuracy on Test Set:")
print(score_SW)

predict_features = predict_DE.iloc[:,1:20]

predict_labels=predict_DE['class_labels']

Q = predict_features

Q_test = scaler.transform(Q)

q_pred = model_SW.predict(Q_test)

score_pred_DE = model_SW.score(Q_test, predict_labels,verbose=1)
print("Accuracy on German Prediction Set:")
print(score_pred_DE)
predict_DE['prediction'] = q_pred

test_de_prediction = predict_DE[['GSR', 'prediction']].groupby('prediction').count()
test_de_prediction = test_de_prediction.rename(columns={'GSR': 'Amount of Germans'})
print("Amount of German people predicted to be part of the Thoughtleader Tribe or not:")
print("")
print(test_de_prediction)
print("")
print("")

#################################################################################################################
# train the model with fine tuned parameters on the German dataset and predict the Swiss thoughtleaders

def create_model_tuned_SW():
    model_SW = Sequential()
    
    model_SW.add(Dense(8, activation='relu', input_shape=(19,)))
    
    model_SW.add(Dense(8, activation='relu'))
    
    model_SW.add(Dense(8, activation='relu'))
    
    model_SW.add(Dense(1, activation='sigmoid'))
    
    
    model_SW.compile(loss='binary_crossentropy',
                  optimizer='Adamax',
                  metrics=['accuracy'])
    
    return model_SW

train = data_DE.drop(columns=['m/w', 'Bereich', 'Wikipedia', 'id', 'Twitter Verifiziert?','Wikipedia_name', 'Twitter_score', 'Wikipedia_score_x',  'Wikipedia_score_y', 'GSR_score', 'Thoughtleader_Score'])

labels=train['class_labels']
features = train.iloc[:,1:20]

X=features

y=np.ravel(labels)

# split into 30% and 70% training and testing data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# normalize data 
scaler = StandardScaler().fit(X_train)

X_train = scaler.transform(X_train)

X_test = scaler.transform(X_test)

# create model 
model_DE = KerasClassifier(build_fn=create_model_tuned_SW, epochs=10, batch_size=1, verbose=0)

model_DE.fit(X_train, y_train,epochs=10, batch_size=1, verbose=1)

y_pred = model_DE.predict(X_test)

score_DE = model_DE.score(X_test, y_test,verbose=1)
print("Accuracy on Test Set:")
print(score_DE)

predict_features = predict_SW.iloc[:,1:20]

predict_labels=data_SW['class_labels']

Q = predict_features

Q_test = scaler.transform(Q)

q_pred = model_DE.predict(Q_test)

score_pred_SW = model_DE.score(Q_test, predict_labels,verbose=1)
print("Accuracy on Swiss Prediction Set:")
print(score_pred_SW)
predict_SW['prediction'] = q_pred

test_de_prediction = predict_SW[['GSR', 'prediction']].groupby('prediction').count()
test_de_prediction = test_de_prediction.rename(columns={'GSR': 'Amount of Swiss'})
print("Amount of Swiss people predicted to be part of the Thoughtleader Tribe or not:")
print("")
print(test_de_prediction)
print("")
print("")

















