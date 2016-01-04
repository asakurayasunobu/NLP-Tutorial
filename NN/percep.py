#usr/bin/python
#coding:utf-8


import sys
from collections import defaultdict

def create_features(x):
    #phi = defaultdict(lambda:len(phi))
    phi = defaultdict(lambda:0)
    words = []
    words = x.strip().split(' ')
    for word in words:
        phi['UNI:'+word] += 1
    return phi

def predict_one(w,phi):
    score = 0
    for word, freq in phi.items():
        if word in w:
            score += freq *w[word]
    if score >= 0:
        return 1
    else:
        return -1

def update_weight(w,phi,y):
    for word, freq in phi.items():
        w[word] += freq*y

if __name__ == '__main__':
    input_file = open('../../../Downloads/nlp-programming/data/titles-en-train.labeled','r')
    w = defaultdict(lambda:0)
    for iter_ in range(5):
        for line in input_file:
            label,sent = line.strip().split('\t')
            y = int(label)
            x = sent
            phi = create_features(x)
            pred_label = predict_one(w,phi)
            if pred_label != y:
                update_weight(w,phi,y)
    for key, value in sorted(w.items(), key = lambda x:x[1]):
        print(key, value)
