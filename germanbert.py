# -*- coding: utf-8 -*-
"""
Created on Sun Jun 20 13:41:18 2021

@author: Johanna

"""

from simpletransformers.classification import ClassificationModel
from sklearn.metrics import f1_score, accuracy_score
import pandas as pd
import os 
import tarfile
from add_sentiment import process_summary
 

#loading the datasets
data_train = pd.read_excel('authors_train.xlsx', index_col=0, dtype=str)
data_test = pd.read_excel('authors_test.xlsx', index_col=0, dtype=str)

#drop unused columns
data_train = data_train.drop(columns=['title', 'media', 'weight', 'date', 'desc', 'summary', 'link', 'flag'])
data_test = data_test.drop(columns=['title', 'media', 'weight', 'date', 'desc', 'summary', 'link', 'flag'])

#drop nan values
data_train= data_train.dropna()
data_test= data_test.dropna()

#labels
labels = ['Negativ', 'Neutral', 'Positiv']
data_train['pred_class'] = data_train.apply(lambda x:  labels.index(x['sentiment']),axis=1)
#drop the sentiment column for later classification
data_train = data_train.drop(columns=['sentiment'])

print(data_train)

#do the same for the test model 
data_test['pred_class'] = data_test.apply(lambda x:  labels.index(x['sentiment']),axis=1)
#drop the sentiment column for later classification
data_test = data_test.drop(columns=['sentiment'])

print(data_test)

#load pretrained model 
 
 # define hyperparameter
train_args ={"reprocess_input_data": True,
              "fp16":False,
              "num_train_epochs": 4}
 
 # Create a ClassificationModel
model = ClassificationModel(
     "bert", "bert-base-german-cased",
     use_cuda=False,
     num_labels=3,
     args=train_args
 )
 #train model
model.train_model(data_train)

def f1_multiclass(labels, preds):
     return f1_score(labels, preds, average='micro')
 
#test model and put out f1_score 
result, model_outputs, wrong_predictions = model.eval_model(data_test, f1=f1_multiclass, acc=accuracy_score)

print(result)
    
#save the trained model 
def pack_model(model_path='',file_name=''):
   files = [files for root, dirs, files in os.walk(model_path)][0]
   with tarfile.open(file_name+ '.tar.gz', 'w:gz') as f:
     for file in files:
       f.add(f'{model_path}/{file}')
 
# run the function
pack_model('outputs','german_bert')    
 
#unpack the model again to predict something 
def unpack_model(model_name=''):
   tar = tarfile.open(f"{model_name}.tar.gz", "r:gz")
   tar.extractall()
   tar.close()
   
unpack_model('german_bert')
 
# get the saved model with the right path
# Create a ClassificationModel with our trained model

# define hyperparameter
train_args ={"reprocess_input_data": True,
             "overwrite_output_dir": True,
             "fp16":False,
             "num_train_epochs": 4}

# create model
model_saved = ClassificationModel(
     'bert', 'outputs/',
     use_cuda=False,
     num_labels=3,
     args=train_args
 )
 
# load the data to get predicted by our trained model the same way as in the
# other BERT prediction code 
data = pd.read_excel('Muschg_all_2021.xlsx', index_col=0, dtype=str)
process_summary(data)
data = data[data.Processed_summary != 'nan']
data = data.drop(columns=['title', 'media', 'date', 'desc', 'summary', 'link', 'flag'])
data = data.Processed_summary.tolist()
print(data)

# predict the data and print labels
prediction = []
raw_output = []
for text in data: 
    predictions, raw_outputs = model_saved.predict([text])
    prediction.append(predictions)
    raw_output.append(raw_outputs)
    
print(prediction)

