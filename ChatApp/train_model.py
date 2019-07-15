# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 09:49:33 2019

@author: Irene
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.metrics import accuracy_score

import random
import pandas as pd
import numpy as np
import time
import re


import spacy
nlp= spacy.load('de_core_news_sm')

#change words to lemma
def cleantext(text):
    text= text.replace('?','')
    result=[]
    text=nlp(text)
    for token in text:
        result.append(token.lemma_)
    return result


#clean text
def tokenizer(text):
    if text:
        result = re.findall('[a-z]{2,}', text.lower())
    else:
        result = []
    return result

#load file chat
import json
with open('/Users/saturn/Documents/GitHub/chatbotAI/intent.json') as json_data:
    intents = json.load(json_data)
    
#load list of german stopwords
import json
with open('/Users/saturn/Desktop/stopwords-de.json') as stop_word:
    stop = json.load(stop_word)


dicte={}    
classes=[]

#convert json data to a dict
for intent in intents['intents']:
    for pattern in intent['patterns']:
        dicte[pattern]=intent['tag']
        #get classes(tag)
        if intent['tag'] not in classes:
            classes.append(intent['tag'])
    
#convert dict to a dataframe
df = pd.DataFrame.from_dict(dicte, orient='index').reset_index()
df.columns=['pattern','tag']

X= df['pattern']
y= df['tag']

#convert sentences to vector 
vect = TfidfVectorizer(tokenizer=cleantext, stop_words=stop)
X_train_vect = vect.fit_transform(X)

#convert text to numerical type
lb = LabelEncoder()
y_train_label = lb.fit_transform(y)



#build model with SGDClassifier
sgd = SGDClassifier(loss='modified_huber', max_iter=100)
sgd.fit(X_train_vect,y_train_label)
sgd.score(X_train_vect,y_train_label)

##with SVM and Onevsrestclassifier
#classifier = SVC(C=100, # penalty parameter
#                  kernel='linear', # kernel type, rbf working fine here
#                  degree=3, # default value
#                  gamma=1, # kernel coefficient
#                  coef0=1, # change to 1 from default value of 0.0
#                  shrinking=True, # using shrinking heuristics
#                  tol=0.001, # stopping criterion tolerance 
#                   probability=True, # no need to enable probability estimates
#                   cache_size=200, # 200 MB cache size
#                   class_weight=None, # all classes are treated equally 
#                   verbose=False, # print the logs 
#                   max_iter=-1, # no limit, let it run
#                   decision_function_shape=None, # will use one vs rest explicitly 
#                   random_state=None)
#model = OneVsRestClassifier(classifier, n_jobs=4)
#model.fit(X_train_vect, y_train_label)
#model.score(X_train_vect,y_train_label)

#
#
#
#test1=(['Ziel'])
#
#
#def test(model, text):
#    test= vect.transform(text)
#    pred_test=model.predict_proba(test)    
##create dataframe for test result
#    prob=pd.DataFrame(columns=['id','tag'])
#    for i,pred in enumerate(pred_test):
#        prob[i]=pred_test[i,:]
#    prob['id']=prob.index.tolist()
#    prob['tag']=lb.inverse_transform(prob['id'])
#    prob.rename(columns={0: 'accuracy'}, inplace=True)
#    prob= prob.sort_values(by=['accuracy'], ascending=False)
#    prob=prob.reset_index(drop=True)
#    return prob
#
#predict_lr= test(lr,test1)
#predict_nb= test(nb,test1)
#predict_sgd = test(sgd,test1)
#
#predict_svm = test(model,test1)

 
def predict(text):
    data=([text])
    test= vect.transform(data)
    pred_test= sgd.predict_proba(test)    
    if len(str(test))==0:
        for intent in intents['intents']:
            if intent['tag']=='noanswer':
                reply=random.choice(intent['responses'])
        return reply
        print(reply)
    else:
        #create dataframe for test result
        prob=pd.DataFrame(columns=['id','tag'])
        for i,pred in enumerate(pred_test):
            prob[i]= pred_test[i,:]
            prob['id']= prob.index.tolist()
            prob['tag']=lb.inverse_transform(prob['id'])
            prob.rename(columns={0: 'accuracy'}, inplace=True)
            prob= prob.sort_values(by=['accuracy'], ascending=False)
            prob=prob.reset_index(drop=True)
            print(prob['accuracy'][0])
            print(prob['tag'][0])
            print(prob['accuracy'][1])
            print(prob['tag'][1])
            if (prob['accuracy'][0] - prob['accuracy'][1])< 0.4:
                replies=[]
                for intent in intents['intents']:
                    if intent['tag']== prob['tag'][0] or intent['tag']== prob['tag'][1] :
                        replies.append(random.choice(intent['patterns']))
                return replies
            else:
                tag=prob['tag'][0]
                for intent in intents['intents']:
                    if intent['tag']== tag:
                        reply= random.choice(intent['responses'])
                        return reply
                        print(reply)
    
        
