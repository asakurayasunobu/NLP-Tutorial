#usr/bin/python
#--*--coding:utf-8--*--
import sys
from collections import defaultdict
import numpy as np

def create_features(x,ids):#辞書に１行の文を単語に分割し頻度を数える
    phi = np.zeros(len(ids))
    if x == "":
        return phi
    words = x.strip().split(' ')
    for word in words:
        phi[ids['UNI:'+word]] += 1
    return phi

def predict_one(w,phi):#辞書と単語の重み辞書を受け取って、
    score = np.dot(w,phi)
    return (1 if score >= 0 else -1)#?????

def update_weight(w,phi,y):
    for key,value in enumerate(phi):
        w[key] += value * y

if __name__ == '__main__':
   inputfile = open(sys.argv[1],'r')
   ids = defaultdict(lambda: len(ids))
   for line in inputfile:
       x = line.strip().split('\t')[1]
       for word in x.strip().split(' '):
           ids['UNI:'+word]
   w = np.zeros(len(ids))
   inputfile.close()
   inputfile = open(sys.argv[1],'r')
   for iter_ in range(1):
       for line in inputfile:  #入力ファイル
           value,key = line.strip().split('\t')
           y = int(value)
           x = key
           phi = create_features(x,ids) #一文の単語の頻度のdict
           ydash = predict_one(w,phi)
           if ydash != y:
               update_weight(w,phi,y)
   for line in open(sys.argv[2],'r'):
       phi_list=list()
       for word in line.strip().split():
           if 'UNI:'+word in ids:
               phi_list.append(word)
       phi = create_features(' '.join(phi_list),ids)
       print(predict_one(w,phi))
