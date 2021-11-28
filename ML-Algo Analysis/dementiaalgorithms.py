# -*- coding: utf-8 -*-
"""DementiaAlgorithms.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vxR6eQ9ycxZEOyIPqg4uAYQmAElV677a

## Dataset and Analysis

Import all the necessary libraries and modules for machine learning and deep learning
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler, StandardScaler 
from sklearn.model_selection import cross_val_score

import tensorflow as tf
from keras.models import Model, Sequential
from keras.layers import Input,Dense

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, recall_score, roc_curve, auc

# %matplotlib inline

sns.set()

"""Read the .csv file for our data"""

df = pd.read_csv('oasis_longitudinal.csv')

"""Filter all the patients according to their visits and show patients whose visit input == 1"""

df = df.loc[df['Visit']==1]

"""Reset the index values so that they are in sequence"""

df = df.reset_index(drop=True)

"""Drop unnecessary columns and replace the data which cannot be read"""

df['M/F'] = df['M/F'].replace(['F','M'], [0,1]) # M/F column
df['Group'] = df['Group'].replace(['Converted'], ['Demented']) # Target variable
df['Group'] = df['Group'].replace(['Demented', 'Nondemented'], [1,0]) # Target variable
df = df.drop(['MRI ID', 'Visit', 'Hand'], axis=1) # Drop unnecessary columns

"""## Data Preprocessing

Identify fields which have unreadable datatypes
"""

pd.isnull(df).sum() 
#df["SES"].fillna(df.groupby("EDUC")["SES"].transform("median"), inplace=True)

"""Drop fields which have unreadable datatypes"""

df_dropna = df.dropna(axis=0, how='any')
pd.isnull(df_dropna).sum()
#pd.isnull(df).sum()

"""Differentiate patients as to demented and nondemented"""

df_dropna['Group'].value_counts()

"""Reset indexes in sequential order"""

df = df_dropna.reset_index(drop=True)
df

"""Set x and y inputs for Training and Validation Data"""

Y = df['Group'].values # Target for the model
X = df[['M/F', 'Age', 'EDUC', 'SES', 'MMSE', 'eTIV', 'nWBV', 'ASF']] # Features we use

# splitting into three sets
X_trainval, X_test, Y_trainval, Y_test = train_test_split(
    X, Y, random_state=10,stratify=df['Group'].values)

# Feature scaling
scaler = StandardScaler().fit(X_trainval)
X_trainval_scaled = scaler.transform(X_trainval)
X_test_scaled = scaler.transform(X_test)

"""Print the Data"""

print('Number of demented samples in training data:',(np.asarray(Y_trainval)==1).sum())
print('Number of non-demented samples in training data:',(np.asarray(Y_trainval)==0).sum())
print('Traning data features:',X_trainval.shape)
print('Training data labels:',Y_trainval.shape)

print('Testing data features:',X_test_scaled.shape)
print('Testing data labels:',Y_test.shape)

"""The above section of the code included fetching the file and filtering and modifying the data according to our use.

## Simple Feed-Forward Neural Network

Initialising the model
"""

# model = Sequential()
# model.add(Dense(12,activation='relu',input_dim=X_train.shape[0]))
# model.add(Dense(8,activation='relu'))
# model.add(Dense(1,activation='sigmoid'))
input_shape = (X_trainval_scaled.shape[-1])
i = Input(shape = input_shape)
x = Dense(12,activation='relu',kernel_initializer='he_normal')(i)
x = Dense(8,activation='relu',kernel_initializer='he_normal')(x)
x = Dense(1, activation='sigmoid')(x)
model = Model(i,x)
model.summary()

"""Compiling the model"""

model.compile(loss='binary_crossentropy',optimizer='adam',metrics='accuracy')
model.fit(X_trainval_scaled,Y_trainval,epochs=75,batch_size=4,validation_data=(X_test_scaled,Y_test))

"""Printing the Output"""

loss,acc = model.evaluate(X_test_scaled,Y_test)
PredictedOutput = (model.predict(X_test_scaled) > 0.5).astype("int32")
print(PredictedOutput)
test_recall = recall_score(Y_test, PredictedOutput, pos_label=1)
fpr, tpr, thresholds = roc_curve(Y_test, PredictedOutput, pos_label=1)
test_auc = auc(fpr, tpr)
print("Test accuracy is", acc)
confusion_matrix(Y_test, PredictedOutput)

"""## SVM

Building a SVM model
"""

best_score = 0
kfolds = 5
for c_paramter in [0.001, 0.01, 0.1, 1, 10, 100, 1000]: #iterate over the values we need to try for the parameter C
    for gamma_paramter in [0.001, 0.01, 0.1, 1, 10, 100, 1000]: #iterate over the values we need to try for the parameter gamma
        for k_parameter in ['rbf', 'linear', 'poly', 'sigmoid']: # iterate over the values we need to try for the kernel parameter
            svmModel = SVC(kernel=k_parameter, C=c_paramter, gamma=gamma_paramter) #define the model
            # perform cross-validation
            scores = cross_val_score(svmModel, X_trainval_scaled, Y_trainval, cv=kfolds, scoring='accuracy')
            # the training set will be split internally into training and cross validation

            # compute mean cross-validation accuracy
            score = np.mean(scores)
            # if we got a better score, store the score and parameters
            if score > best_score:
                best_score = score #store the score 
                best_parameter_c = c_paramter #store the parameter c
                best_parameter_gamma = gamma_paramter #store the parameter gamma
                best_parameter_k = k_parameter
            

# rebuild a model with best parameters to get score 
SelectedSVMmodel = SVC(C=best_parameter_c, gamma=best_parameter_gamma, kernel=best_parameter_k).fit(X_trainval_scaled, Y_trainval)

"""Printing output"""

test_score = SelectedSVMmodel.score(X_test_scaled, Y_test)
PredictedOutput = SelectedSVMmodel.predict(X_test_scaled)
print(PredictedOutput)
test_recall = recall_score(Y_test, PredictedOutput, pos_label=1)
fpr, tpr, thresholds = roc_curve(Y_test, PredictedOutput, pos_label=1)
test_auc = auc(fpr, tpr)
print("Best accuracy on cross validation set is:", best_score)
print("Best parameter for c is: ", best_parameter_c)
print("Best parameter for gamma is: ", best_parameter_gamma)
print("Best parameter for kernel is: ", best_parameter_k)
print("Test accuracy with the best parameters is", test_score)
confusion_matrix(Y_test, PredictedOutput)

"""## Decision Tree Classification

Building a Decision Tree Classification Model
"""

best_score = 0

for md in range(1, 9): # iterate different maximum depth values
    # train the model
    treeModel = DecisionTreeClassifier(random_state=0, max_depth=md, criterion='gini')
    # perform cross-validation
    scores = cross_val_score(treeModel, X_trainval_scaled, Y_trainval, cv=kfolds, scoring='accuracy')
    
    # compute mean cross-validation accuracy
    score = np.mean(scores)
    
    # if we got a better score, store the score and parameters
    if score > best_score:
        best_score = score
        best_parameter = md

# Rebuild a model on the combined training and validation set        
SelectedDTModel = DecisionTreeClassifier(max_depth=best_parameter).fit(X_trainval_scaled, Y_trainval )

"""Printing Output"""

test_score = SelectedDTModel.score(X_test_scaled, Y_test)
PredictedOutput = SelectedDTModel.predict(X_test_scaled)
print(PredictedOutput)
test_recall = recall_score(Y_test, PredictedOutput, pos_label=1)
fpr, tpr, thresholds = roc_curve(Y_test, PredictedOutput, pos_label=1)
test_auc = auc(fpr, tpr)
print("Best accuracy on validation set is:", best_score)
print("Best parameter for the maximum depth is: ", best_parameter)
print("Test accuracy with best parameter is ", test_score)
confusion_matrix(Y_test, PredictedOutput)

"""## Random Forest Classification

Building a random forest classification model
"""

best_score = 0

for M in range(2, 15, 2): # combines M trees
    for d in range(1, 9): # maximum number of features considered at each split
        for m in range(1, 9): # maximum depth of the tree
            # train the model
            # n_jobs(4) is the number of parallel computing
            forestModel = RandomForestClassifier(n_estimators=M, max_features=d, n_jobs=4,
                                          max_depth=m, random_state=0)
        
            # perform cross-validation
            scores = cross_val_score(forestModel, X_trainval_scaled, Y_trainval, cv=kfolds, scoring='accuracy')

            # compute mean cross-validation accuracy
            score = np.mean(scores)

            # if we got a better score, store the score and parameters
            if score > best_score:
                best_score = score
                best_M = M
                best_d = d
                best_m = m

# Rebuild a model on the combined training and validation set        
SelectedRFModel = RandomForestClassifier(n_estimators=M, max_features=d,
                                          max_depth=m, random_state=0).fit(X_trainval_scaled, Y_trainval )

"""Printing Output"""

PredictedOutput = SelectedRFModel.predict(X_test_scaled)
print(PredictedOutput)
test_score = SelectedRFModel.score(X_test_scaled, Y_test)
test_recall = recall_score(Y_test, PredictedOutput, pos_label=1)
fpr, tpr, thresholds = roc_curve(Y_test, PredictedOutput, pos_label=1)
test_auc = auc(fpr, tpr)
print("Best accuracy on validation set is:", best_score)
print("Best parameters of M, d, m are: ", best_M, best_d, best_m)
print("Test accuracy with the best parameters is", test_score)
confusion_matrix(Y_test, PredictedOutput)

"""## AdaBoost Classification

Building AdaBoost classification Model
"""

best_score = 0

for M in range(2, 15, 2): # combines M trees
    for lr in [0.0001, 0.001, 0.01, 0.1, 1]:
        # train the model
        boostModel = AdaBoostClassifier(n_estimators=M, learning_rate=lr, random_state=0)

        # perform cross-validation
        scores = cross_val_score(boostModel, X_trainval_scaled, Y_trainval, cv=kfolds, scoring='accuracy')

        # compute mean cross-validation accuracy
        score = np.mean(scores)

        # if we got a better score, store the score and parameters
        if score > best_score:
            best_score = score
            best_M = M
            best_lr = lr

# Rebuild a model on the combined training and validation set        
SelectedBoostModel = AdaBoostClassifier(n_estimators=M, learning_rate=lr, random_state=0).fit(X_trainval_scaled, Y_trainval )

"""Printing Output"""

PredictedOutput = SelectedBoostModel.predict(X_test_scaled)
print(PredictedOutput)
test_score = SelectedRFModel.score(X_test_scaled, Y_test)
test_recall = recall_score(Y_test, PredictedOutput, pos_label=1)
fpr, tpr, thresholds = roc_curve(Y_test, PredictedOutput, pos_label=1)
test_auc = auc(fpr, tpr)
print("Best accuracy on validation set is:", best_score)
print("Best parameter of M is: ", best_M)
print("best parameter of LR is: ", best_lr)
print("Test accuracy with the best parameter is", test_score)
confusion_matrix(Y_test, PredictedOutput)

"""## Logistic Regression

Building a Logisting Regression Model
"""

best_score=0
kfolds=5 # set the number of folds

for c in [0.001, 0.1, 1, 10, 100]:
    logRegModel = LogisticRegression(C=c)
    # perform cross-validation
    scores = cross_val_score(logRegModel, X_trainval_scaled, Y_trainval, cv=kfolds, scoring='accuracy')
    
    # compute mean cross-validation accuracy
    score = np.mean(scores)
    
    # Find the best parameters and score
    if score > best_score:
        best_score = score
        best_parameters = c

# rebuild a model on the combined training and validation set
SelectedLogRegModel = LogisticRegression(C=best_parameters).fit(X_trainval_scaled, Y_trainval)

"""Printing output"""

test_score = SelectedLogRegModel.score(X_test_scaled, Y_test)
PredictedOutput = SelectedLogRegModel.predict(X_test_scaled)
print(PredictedOutput)
test_recall = recall_score(Y_test, PredictedOutput, pos_label=1)
fpr, tpr, thresholds = roc_curve(Y_test, PredictedOutput, pos_label=1)
test_auc = auc(fpr, tpr)
print("Best accuracy on validation set is:", best_score)
print("Best parameter for regularization (C) is: ", best_parameters)
print("Test accuracy with best C parameter is", test_score)        
confusion_matrix(Y_test, PredictedOutput)