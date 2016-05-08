#usr/bin/python
#--*--coding:utf-8--*--
import sys
from collections import defaultdict
import numpy as np
import random


def make_id(in_list):
    ids = defaultdict(lambda:len(ids))
    for line in in_list:
        x = line.strip().split('\t')[1]
        for word in x.split():
            ids['UNI:{}'.format(word)]
    return ids

def create_features(x,ids):
    phi = np.zeros(len(ids))
    words = x.strip().split()
    for word in words:
        phi[ids['UNI:'+word]] += 1
    return phi

def predict_one(weight,phi):
    score = np.dot(weight,phi)
    return (1 if score >= 0 else -1)

def update_weight(weight,phi,y):
    weight += phi * y
    #for key,value in enumerate(phi):
    #    weight[key] += value * y

def predict_all(weight, ids, test_file):
    for line in test_file:
        phi = np.zeros(len(ids))
        words = line.strip().split()
        for word in words:
            if 'UNI:{}'.format(word) in ids:
                phi[ids['UNI:{}'.format(word)]] += 1
        pred_y = predict_one(weight, phi)
        print(pred_y)
if __name__ == '__main__':
   train_file = open('../nlptutorial/data/titles-en-train.labeled')
   test_file = open('../nlptutorial/data/titles-en-test.word')
   train_list = list(train_file)
   #--train--
   ids = make_id(train_list)
   weight = np.zeros(len(ids))
   iteration = 1
   for iter_ in range(iteration):
       random.shuffle(train_list)
       for line in train_list:
           y, x = line.strip().split('\t')
           y = int(y)
           phi = create_features(x,ids)
           ydash = predict_one(weight,phi)
           if ydash != y:
               update_weight(weight,phi,y)
   predict_all(weight, ids, test_file)
