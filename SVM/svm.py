#!usr/bin/python
#coding:utf-8

from collections import defaultdict
import math


def create_features(x):
    phi = defaultdict(lambda: 0)
    words = []
    words = x.strip().split()
    for word in words:
        phi['UNI:' + word] += 1
    return phi


def updata_weights(w,phi,y):
    for name, value in w.items():
        if abs(value) < c:
            w[name] = 0
        else:
            w[name] -= math.copysign(1,value)*c
    for name, value in phi.items():
        w[name] += value*y


def predict_one(w,phi):
    val = 0
    for word,freq in phi.items():
        val += freq*w[word]
    return predict


def make_model_file(w):
    f = open('svm_model_file','w')
    for word,weight in w.items():
        f.write(word+'\t'+str(weight)+'\n')
    f.close()


def main():
    w = defaultdict(lambda: 0)
    for iter_ in range(5):
        for line in open('../../data/titles-en-train.labeled'):
            y, x = line.strip().split('\t')
            y = int(y)
            phi = create_features(x)
            predict = y*predict_one(w,phi)#weight of word と word frequency(feature)　の内積 * label 
            if predict < margin:
                updata_weights(w,phi,y)#marginは定数,c = 0.0001(正則化係数)
    make_model_file(w)


"""
def getw(w,name,c,iter_,last):
    if iter_ != last[name]:
        c_size = margin*(iter_-last[name])
        if math.fabs(w[name]) <= c_size:
            w[name] = 0
        else:
            w[name] -= math.copysign(value)*margin
        for name, value in phi.items():
            w[name] += value*y
"""

if __name__ == '__main__':
    c = 0.0001
    margin = 0.1
    main()


