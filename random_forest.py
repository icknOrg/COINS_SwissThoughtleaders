# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 22:55:52 2021

@author: vikto

Train and use Random Forest Models to predict both 
the German people's and the Swiss people's membership of the Thoughtleader Tribe
"""

import warnings
warnings.filterwarnings("ignore")

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

#Select here which classification should be done:
from create_classification_df import get_class_original_SW
from create_classification_df import get_class_original_DE
#from create_classification_all_df import get_class_original_SW
#from create_classification_all_df import get_class_original_DE
from sklearn.model_selection import GridSearchCV

# Get whole data of Swiss and German people
data_sw = get_class_original_SW()
data_de = get_class_original_DE()


###############################################################################
###############################################################################
#1. Train model with Swiss Thoughtleaders and predict the German Thoughtleaders
print("")
print("------------------------------------------------------------------------------------------------------------------------------")
print("1. Random Forest trained on the Swiss people and used for predicting the German people's membership of the Thoughtleader Tribe")
print("")

# X contains the features and y the prediction variable
X=data_sw[['GSR', 'verified', 'followers_count', 'degree', 'betweenness', 'contribution_index', 'sentiment_avg', 
           'emotionality_avg','ego_art', 'ego_nudges', 'alter_art','alter_nudges', 'complexity_avg', 
           'Backlinks', 'Links', 'Awards', 'Publications', 'Sentiment_score']]
y=data_sw[['class_labels']]

# Split into 30% testing and 70% training data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Normalize data 
scaler = StandardScaler().fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

###########################################################
#Fine tuning of hyperparameters of random forest classifier
###########################################################

# Create the parameter grid based on the results of random search 
#param_grid = {
#    'n_estimators' : [100, 300, 500, 800, 1200],
#    'max_depth' : [5, 8, 15, 25, 30],
#    'min_samples_split' : [2, 5, 10, 15, 100],
#    'min_samples_leaf' : [1, 2, 5, 10]
#}

# Create a based model
#clf = RandomForestClassifier()
# Instantiate the grid search model
#grid_search = GridSearchCV(estimator = clf, param_grid = param_grid, 
                           #cv = 3, n_jobs = -1, verbose = 2)

# Fit the grid search to the data
#grid_search.fit(X_train, y_train)
#print(grid_search.best_params_)

##########################################################################################################################
#Hyperparameter fine tuning results:
# 1. Classification based on the separate datasets: max_depth=5, min_samples_leaf=1, min_samples_split=2, n_estimators=100
# 2. Classification based on the whole dataset: max_depth=30, min_samples_leaf=1, min_samples_split=2, n_estimators=100
##########################################################################################################################

clf = RandomForestClassifier(max_depth=5, min_samples_leaf=1, min_samples_split=2, n_estimators=100)

# Create Random Forest model and train it with the training data
clf.fit(X_train, y_train)

# Predict the classification using the test data
y_pred = clf.predict(X_test)

# Calculate accuracy of the model for training and test data
print("Accuracy of training data: ", clf.score(X_train, y_train))
print("Accuracy of test data: ", clf.score(X_test, y_test))
print("")

# Now we use the list of the German Thoughtleaders and predict their classification with the trained Random Forest model

# Select relevant columns
test_de=data_de[['GSR', 'verified', 'followers_count', 'degree', 'betweenness', 'contribution_index', 'sentiment_avg', 
           'emotionality_avg','ego_art', 'ego_nudges', 'alter_art','alter_nudges', 'complexity_avg', 
           'Backlinks', 'Links', 'Awards', 'Publications', 'Sentiment_score']]

test_de_labels=data_de[['class_labels']] 
print("Accuracy of DE data: ", clf.score(test_de, test_de_labels))
test_de['prediction'] = clf.predict(test_de)

test_de_prediction = test_de[['GSR', 'prediction']].groupby('prediction').count()
test_de_prediction = test_de_prediction.rename(columns={'GSR': 'Amount of Germans'})
print("Amount of German people predicted to be part of the Thoughtleader Tribe or not:")
print("")
print(test_de_prediction)
print("")
print("")


#######################################################################################
#######################################################################################
#2. Train the model with the German Thoughtleaders and predict the Swiss Thoughtleaders
print("------------------------------------------------------------------------------------------------------------------------------")
print("2. Random Forest trained on the German people and used for predicting the Swiss people's membership of the Thoughtleader Tribe")
print("")

# X contains the features and y the prediction variable
X=data_de[['GSR', 'verified', 'followers_count', 'degree', 'betweenness', 'contribution_index', 'sentiment_avg', 
           'emotionality_avg','ego_art', 'ego_nudges', 'alter_art','alter_nudges', 'complexity_avg', 
           'Backlinks', 'Links', 'Awards', 'Publications', 'Sentiment_score']]

y=data_de[['class_labels']]

# split into 40% test and 60% training data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Normalize data 
scaler = StandardScaler().fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

# Create Random Forest model and train it with the training data
clf_2 = RandomForestClassifier(max_depth=5, min_samples_leaf=1, min_samples_split=2, n_estimators=100)
clf_2.fit(X_train, y_train)

# Predict the classification using the test data
y_pred = clf_2.predict(X_test)

# Calculate accuracy of the model for training and test data
print("Accuracy of training data: ", clf_2.score(X_train, y_train))
print("Accuracy of test data: ", clf_2.score(X_test, y_test))
print("")

# Now we use the list of the Swiss Thoughtleaders and predict their classification with the trained Random Forest model

# Select relevant columns
test_sw=data_sw[['GSR', 'verified', 'followers_count', 'degree', 'betweenness', 'contribution_index', 'sentiment_avg', 
                    'emotionality_avg','ego_art', 'ego_nudges', 'alter_art','alter_nudges', 'complexity_avg', 
                    'Backlinks', 'Links', 'Awards', 'Publications', 'Sentiment_score']]

test_sw_labels=data_sw[['class_labels']]
print("Accuracy of SW data: ", clf_2.score(test_sw, test_sw_labels))
test_sw['prediction'] = clf_2.predict(test_sw)

test_sw_prediction = test_sw[['GSR', 'prediction']].groupby('prediction').count()
test_sw_prediction = test_sw_prediction.rename(columns={'GSR': 'Amount of Swiss'})
print("Amount of Swiss people predicted to be part of the Thoughtleader Tribe or not:")
print("")
print(test_sw_prediction)
#print(test_sw[['GSR', 'prediction']].groupby('prediction').count())