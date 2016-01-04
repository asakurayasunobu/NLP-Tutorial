#!usr/bin/python
#-*-coding:utf-8-*-


import sys
from collections import defaultdict


class Perceptron():
    def __init__(self):
        self.w     = defaultdict(lambda:0) 
    def pred_one(w,phi):
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
            w[word] += freq *y


